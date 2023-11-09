# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:51:06 2022

@author: srabadan
"""

import pandas as pd
from abc import ABC, abstractmethod
import pytz
import math

BXL = pytz.timezone('Europe/Brussels')


class typeBalance(ABC):
    def __init__(self,dataframe_consumption, number_of_buildings, dataframe_PV):       
        self.dr_cons = dataframe_consumption
        self.n_buildings = number_of_buildings
        self.ds_FV = dataframe_PV
    @abstractmethod
    def calculation(self):
        pass


class balancePropio(typeBalance):
    def __init__(self, dataframe_consumption, number_of_buildings, dataframe_PV):
        typeBalance.__init__(self, dataframe_consumption, number_of_buildings, dataframe_PV)
    def calculation(self):
        self.ds_FV['Med_cp'] = self.dr_cons['Med'] * self.n_buildings
        self.ds_FV['Sc'] = [min(x) for x in (zip(self.ds_FV.Pv_base, self.ds_FV.Med_cp))]
        self.ds_FV['Dt'] = self.ds_FV['Med_cp'] - self.ds_FV['Sc']
        self.ds_FV['Et'] = self.ds_FV['Pv_base'] - self.ds_FV['Sc']  # CP
        self.ds_FV['Net'] = self.ds_FV['Dt'] - self.ds_FV['Et']  # CP
        if self.ds_FV.Med_cp.sum() !=0:
            LoCov = (self.ds_FV.Sc.sum() / self.ds_FV.Med_cp.sum()) * 100  # CP
        else:
            LoCov = 0
        return self.ds_FV, LoCov


class balanceCEL(typeBalance):
    def __init__(self, dataframe_consumption, number_of_buildings, dataframe_PV):
        typeBalance.__init__(self, dataframe_consumption, number_of_buildings, dataframe_PV)    
    def calculation(self):
        self.ds_FV['Med_cel'] = self.dr_cons['Med'] * self.n_buildings
        self.ds_FV['Sc_cel'] = [min(x) for x in (zip(self.ds_FV.Pv_cel, self.ds_FV.Med_cel))]
        self.ds_FV['Dt_cel'] = self.ds_FV['Med_cel'] - self.ds_FV['Sc_cel']
        self.ds_FV['Et_cel'] = self.ds_FV['Pv_cel'] - self.ds_FV['Sc_cel']  # CP
        self.ds_FV['Net_cel'] = self.ds_FV['Dt_cel'] - self.ds_FV['Et_cel']  # CP
        if self.ds_FV.Med_cel.sum() != 0:
            LoCov = (self.ds_FV.Sc_cel.sum() / self.ds_FV.Med_cel.sum()) * 100  # CP
        else:
            LoCov = 0            
        return self.ds_FV, LoCov


class balanceCombinado(typeBalance):
    def __init__(self, dataframe_consumption, number_of_buildings, dataframe_PV,dataframe_consumption_CEL,number_of_buildings_CEL,dataframe_PV_CEL): 
        self.dr_cons = []
        self.n_buildings = []
        self.dr_cons.append(dataframe_consumption)
        self.dr_cons.append(dataframe_consumption_CEL)
        self.n_buildings.append(number_of_buildings)
        self.n_buildings.append(number_of_buildings_CEL)
        self.df_FV_propio = dataframe_PV
        self.df_FV_CEL = dataframe_PV_CEL
    def calculation(self): 
        ds_FV_propio, LoCov = balancePropio(self.dr_cons[0], self.n_buildings[0], self.df_FV_propio).calculation()
        ds_FV_cel, LoCov_cel = balanceCEL(self.dr_cons[1], self.n_buildings[1], self.df_FV_CEL).calculation()
        ds_FV = pd.concat([ds_FV_propio,ds_FV_cel], axis = 1)
        cons_combinado = pd.DataFrame()
        cons_combinado['Cons'] = ds_FV['Med_cp'] + ds_FV['Med_cel']
        ds_FV['PvT_cp_cel'] = ds_FV['Pv_base'] + ds_FV['Pv_cel']
        ds_FV['Sc_cp_cel'] = [min(x) for x in zip(ds_FV.PvT_cp_cel, cons_combinado.Cons)]
        ds_FV['Dt_cp_cel'] = cons_combinado['Cons'] - ds_FV['Sc_cp_cel']  # CP + CEL
        ds_FV['Et_cp_cel'] = ds_FV['PvT_cp_cel'] - ds_FV['Sc_cp_cel']  # CP + CEL
        ds_FV['Net_cp_cel'] = ds_FV['Dt_cp_cel'] - ds_FV['Et_cp_cel']  # CP + CEL  
        
        if  ds_FV.Med_cel.sum() != 0:
            LoCov_viv = (ds_FV.Sc_cp_cel.sum()-ds_FV.Sc.sum())/ds_FV.Med_cel.sum() * 100  
        else:
            LoCov_viv = 0
        if cons_combinado.Cons.sum() != 0:  
            LoCov_cp_cel = (ds_FV.Sc_cp_cel.sum() /cons_combinado.Cons.sum()) * 100  # CEL
        else:
            LoCov_cp_cel = 0
        LoCov = [LoCov, LoCov_cel,LoCov_viv ,LoCov_cp_cel]
        return ds_FV, LoCov
    
    
class balanceCombinadoCoef(typeBalance):
    def __init__(self, dataframe_consumption, number_of_buildings, dataframe_PV,dataframe_consumption_CEL,number_of_buildings_CEL,dataframe_PV_CEL,coef): 
        self.dr_cons = []
        self.n_buildings = []
        self.dr_cons.append(dataframe_consumption)
        self.dr_cons.append(dataframe_consumption_CEL)
        self.n_buildings.append(number_of_buildings)
        self.n_buildings.append(number_of_buildings_CEL)
        self.df_FV_propio_copy = dataframe_PV.copy(deep = True)
        self.df_FV_CEL = dataframe_PV_CEL
        self.coef = coef
    def calculation(self): 
        
        self.df_FV_propio_copy['Pv_base'] = self.df_FV_propio_copy['Pv_base'].apply(lambda x: x * self.coef)
        ds_FV_propio, LoCov = balancePropio(self.dr_cons[0], self.n_buildings[0], self.df_FV_propio_copy).calculation()
        ds_FV_cel, LoCov_cel = balanceCEL(self.dr_cons[1], self.n_buildings[1], self.df_FV_CEL).calculation()
        ds_FV = pd.concat([ds_FV_propio,ds_FV_cel], axis = 1)
        ds_FV['Cons_total'] = ds_FV['Med_cp'] + ds_FV['Med_cel']
        
        ds_FV['Pv_base_cel'] = self.df_FV_propio_copy['Pv_base'].apply(lambda x: x/self.coef * (1-self.coef))
        ds_FV['Sc_cel_2'] =  [min(x) for x in zip(ds_FV['Pv_base_cel'], ds_FV.Med_cel)]   
        ds_FV['Pv_base'] = ds_FV['Pv_base'].apply(lambda x: x / self.coef)
        ds_FV['PvT_cp_cel'] = ds_FV['Pv_base'] + ds_FV['Pv_cel']
        
        ds_FV['Sc_cp_cel'] = ds_FV.Sc + ds_FV.Sc_cel_2

        
        ds_FV['Dt_cp_cel'] = ds_FV['Cons_total'] - ds_FV['Sc_cp_cel']  # CP + CEL
        ds_FV['Et_cp_cel'] = ds_FV['PvT_cp_cel'] - ds_FV['Sc_cp_cel']  # CP + CEL
        ds_FV['Net_cp_cel'] = ds_FV['Dt_cp_cel'] - ds_FV['Et_cp_cel']  # CP + CEL  
        
        if  ds_FV.Med_cel.sum() != 0:
            LoCov_viv = (ds_FV.Sc_cp_cel.sum()-ds_FV.Sc.sum())/ds_FV.Med_cel.sum() * 100  
        else:
            LoCov_viv = 0
        if ds_FV.Cons_total.sum() != 0:  
            LoCov_cp_cel = (ds_FV.Sc_cp_cel.sum() /ds_FV.Cons_total.sum()) * 100  # CEL
        else:
            LoCov_cp_cel = 0
        LoCov = [LoCov, LoCov_cel,LoCov_viv ,LoCov_cp_cel]
        return ds_FV, LoCov    

# Obsoleto
# class balanceCombinado_IBE(typeBalance):
#     def calculation(self, dr_cons, n_viv, ds_FV):
#         coef_propio = 0.6
#         ds_FV['Med_cp'] = dr_cons[0]['Med'] * n_viv[0]
#         ds_FV['Sc'] = [min(x) for x in (
#             zip(ds_FV.Pv_base*coef_propio, ds_FV.Med_cp))]
#         ds_FV['Dt'] = ds_FV['Med_cp'] - ds_FV['Sc']
#         ds_FV['Et'] = ds_FV['Pv_base']*coef_propio - ds_FV['Sc']  # CP
#         ds_FV['Net'] = ds_FV['Dt'] - ds_FV['Et']  # CP
#         LoCov = (ds_FV.Sc.sum() / ds_FV.Med_cp.sum()) * 100  # CP
#         ds_FV, LoCov_cel = balanceCEL.calculation(self, dr_cons[1], n_viv[1], ds_FV)
#         cons_combinado = pd.DataFrame()
#         cons_combinado['Cons'] = ds_FV['Med_cp'] + ds_FV['Med_cel']
#         ds_temp = pd.DataFrame()
#         ds_temp['propio'] = [min(x) for x in zip(
#             ds_FV.Pv_base*coef_propio, ds_FV['Med_cp'])]
#         ds_temp['comunidad'] = [min(y) for y in zip(
#             ds_FV.Pv_base*(1-coef_propio), ds_FV['Med_cel'])]
#         ds_FV['Sc_cp_cel'] = ds_temp['propio'] + ds_temp['comunidad']
#         ds_FV['Dt_cp_cel'] = cons_combinado['Cons'] - ds_FV['Sc_cp_cel']  # CP + CEL
#         ds_FV['Et_cp_cel'] = ds_FV['PvT_cp_cel'] - ds_FV['Sc_cp_cel']  # CP + CEL
#         ds_FV['Net_cp_cel'] = ds_FV['Dt_cp_cel'] - ds_FV['Et_cp_cel']  # CP + CEL
#         if ds_FV.Med_cel.sum() != 0:
#             LoCov_viv = (ds_FV.Sc_cp_cel.sum()-ds_FV.Sc.sum())/ds_FV.Med_cel.sum()  * 100  
#         else:
#             LoCov_viv = 0
#         if cons_combinado.Cons.sum() != 0:
#             LoCov_cp_cel = (ds_FV.Sc_cp_cel.sum() /cons_combinado.Cons.sum()) * 100  # CEL
#         else:
#             LoCov_cp_cel = 0
#         LoCov = [LoCov, LoCov_cel, LoCov_viv,LoCov_cp_cel]
#         return ds_FV, LoCov


class calculo:
    def __init__(self, outputType: typeBalance):
        self.outputType = outputType

    def start(self):
        return self.outputType.calculation()
