# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 18:18:31 2021

@author: Samuel Rabadán - IREC
"""

# Import libraries and packages

import pandas as pd
import os          
import sys


# Path

direct  = os.getcwd()
sys.path[0] = direct

# Interactors

from interactors import dataFV,dataWeather, resourceConsumption
from interactors import getDataARV

# Calculations

from utils import radiationFV, energyBalance_FV

#%% Get data for PV calculation <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# >>> Angles 
def estimationPV(area, P_ele):
    
    #sourceData = getDataARV.SQL_surfaceARV(ref_cat = ref_cat)    # SQL_statments ARV
    #get_data = getDataARV.getData_ARV(sourceData)   # Surfaces of each building
    # Reposity Outputs dicts -> 1) Area of each building (floor-roof-wall) with cadastral referece + 2) Partition ratio with cadastral referece
    #areabyCadastralcode, distributionRatio, ref_use = get_data.start()
    
    cubiertas = ['Cubierta_1']
    gamma = [0]
    beta = [30]
    #area = [((areabyCadastralcode[ref_cat]['roof']*0.25)*0.8)/len(distributionRatio[ref_cat])]
    
    
    
    # >>> Weather
    
    weather = dataWeather.outputTRNSYS(clima = 8)
    getWeatherdata = dataWeather.select(weather)
    
    df_clima = getWeatherdata.start()
    
    
    # Calculate radation <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    
    b_output = radiationFV.dataframe()
    
    PV_dict = {}
    PV_dict_cel = {}
    df_PV_total = pd.DataFrame({'Pv_base': [0] * 8760}, index = df_clima.index)
    df_PV_cel =  pd.DataFrame({'Pv_cel': [0] * 8760}, index = df_clima.index)
    for i in range(0,len(cubiertas)):
        cubierta = dataFV.manualInputs(0, 39.569739942363285, 2.671081012824496, gamma[i], beta[i], area[i])
        getPVdata = dataFV.insert(cubierta)
        parameters, df_PV= getPVdata.start()
        
        b = radiationFV.calculo(b_output, df_clima, df_PV, parameters, 'Pv_base')
        df_PV = b.start()    
        if cubiertas[i] == 'Viviendas':
            PV_dict_cel.setdefault(cubiertas[i],df_PV)
        else:
            PV_dict.setdefault(cubiertas[i],df_PV)
    
        
        
    
    cubiertas_analizar = ['Cubierta_1']
    
    
    for i in cubiertas_analizar:
        if i == 'Viviendas':
            df_PV_cel['Pv_cel'] = df_PV_cel['Pv_cel'] + PV_dict_cel[i]['Pv_base']
            # print(i)
            # print(PV_dict_cel[i]['Pv_base'].sum())
        else:    
            df_PV_total['Pv_base'] = df_PV_total['Pv_base'] + PV_dict[i]['Pv_base']
            # print(i)
            # print(PV_dict[i]['Pv_base'].sum())
        
            
    
    
    
    
    #%% Consumption of dwellings in postcode 07006 "Residencial_3years.csv" in Resoures folder + energy price (example)  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
     
    inicio = pd.Timestamp('2021-01-01')
    fin = pd.Timestamp('2021-12-31 23:00:00')  # Hasta el 1 de enero de 2022 (para incluir la última hora del año)
    rango_horas = pd.date_range(start=inicio, end=fin, freq='H')
    
    # Crear el DataFrame con los índices generados
    data_out = pd.DataFrame(index=rango_horas)
    count = -1
    for i in rango_horas:
        count = count + 1
        data_out.at[i,'Med'] = P_ele[count]*90


    #%% Energy balance
    
    # Energy Balance n building with production (example) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
     
    ebal_out = energyBalance_FV.balancePropio(dataframe_consumption = data_out , number_of_buildings = 1, dataframe_PV = df_PV_total.loc[:,['Pv_base']])
    energy_balance = energyBalance_FV.calculo(ebal_out)
    d_energybalance, LoCov = energy_balance.start()


    return d_energybalance['Sc'].sum()/90
 


