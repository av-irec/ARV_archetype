# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""


# Abstract method import

from abc import ABC, abstractmethod

# Repositories

from utils import transformation_EP_CO2
# Abstract class


class currencyProject(ABC):
    def __init__(self, passiveP_cl,passiveP_ht,passiveP_lig,passiveP_dev,passiveP_dhw):
        self.passiveP_cl = passiveP_cl
        self.passiveP_ht = passiveP_ht
        self.passiveP_lig = passiveP_lig
        self.passiveP_dev = passiveP_dev
        self.passiveP_dhw = passiveP_dhw
    @abstractmethod
    def analysisCalculation(self, grado_ht, grado_cl, grado_dhw):
        pass


class ARV_CO2_PE(currencyProject):  # Calculation of the investment with CMH data as a cost input
    """
    Los parámetros son la demanda que sale directamene de la simulaciones. 
    El cambio de nombre (passive_P_ht) es para diferenciarlo de la clase analisysTRNSYS
    Parameters:
        
        passiveP_cl (dict) -- Demanda
        passiveP_ht (dict) -- common facilities renovation
        passiveP_lig (dict) -- Include facilities in the budget via dictionary with 3 booleans for 'DHW' domestic hot water, 'PV' photovoltaic, 'HVAC' air conditioning        
        passiveP_dev (dict) -- Project Fees
        passiveP_dhw (dict) -- Industrial Benefit
          
    """
    def __init__(self,passiveP_cl,passiveP_ht,passiveP_lig,passiveP_dev,passiveP_dhw ):
        currencyProject.__init__(self,passiveP_cl, passiveP_ht, passiveP_lig, passiveP_dev, passiveP_dhw)
    def analysisCalculation(self, grado_ht, grado_cl, grado_dhw):
        
        PE_ht_rt = {}
        PE_cl_rt = {}
        PE_lig_rt = {}
        PE_dev_rt = {}
        PE_dhw_rt = {}
        project = transformation_EP_CO2.pE_ARV_demand(grado_ht, grado_cl, grado_dhw, coef_CO2={'ele': 0.833, 'GN': 0.252, 'butano': 0.254}, coef_NRPE={'ele': 2.937, 'GN': 1.190, 'butano': 1.201})
        for i in self.passiveP_ht:
            output = transformation_EP_CO2.calculo(project, self.passiveP_ht[i], self.passiveP_cl[i], self.passiveP_lig[i],self.passiveP_dev[i],self.passiveP_dhw[i], EER = 5, COP=4.6, COP_dhw= 3.17, eta_cal=0.92)
            PE_ht_aux, PE_cl_aux, PE_lig_aux,PE_dev_aux ,PE_dhw_aux = output.start()
            PE_ht_rt.setdefault(i, PE_ht_aux)
            PE_cl_rt.setdefault(i, PE_cl_aux)
            PE_lig_rt.setdefault(i, PE_lig_aux)
            PE_dev_rt.setdefault(i,PE_dev_aux)
            PE_dhw_rt.setdefault(i, PE_dhw_aux)
       
        CO2_ht_rt = {}
        CO2_cl_rt = {}
        CO2_lig_rt = {}
        CO2_dev_rt = {}
        CO2_dhw_rt = {}
            
        project = transformation_EP_CO2.CO2_ARV_demand(grado_ht, grado_cl, grado_dhw, coef_CO2={'ele': 0.833, 'GN': 0.252, 'butano': 0.254}, coef_NRPE={'ele': 2.968, 'GN': 1.190, 'butano': 1.201})
        for i in self.passiveP_ht:
            output = transformation_EP_CO2.calculo(project, self.passiveP_ht[i], self.passiveP_cl[i], self.passiveP_lig[i],self.passiveP_dev[i],self.passiveP_dhw[i], EER = 5, COP=4.6, COP_dhw= 3.17, eta_cal=0.92)
            CO2_ht_aux, CO2_cl_aux, CO2_lig_aux,CO2_dev_aux ,CO2_dhw_aux = output.start()
            CO2_ht_rt.setdefault(i, CO2_ht_aux)
            CO2_cl_rt.setdefault(i, CO2_cl_aux)
            CO2_lig_rt.setdefault(i, CO2_lig_aux)
            CO2_dev_rt.setdefault(i,CO2_dev_aux)
            CO2_dhw_rt.setdefault(i, CO2_dhw_aux)        

        return PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt , PE_dhw_rt, CO2_ht_rt, CO2_cl_rt, CO2_lig_rt, CO2_dev_rt, CO2_dhw_rt


class synikia(currencyProject):
    def __init__(self,passiveP_cl,passiveP_ht,passiveP_lig,passiveP_dev,passiveP_dhw ):
        currencyProject.__init__(passiveP_cl, passiveP_ht, passiveP_lig, passiveP_dev, passiveP_dhw)
    def analysisCalculation(self, grado_ht, grado_cl, grado_dhw):
        pass


class do_analysis:
    def __init__(self, Project: currencyProject, grado_ht, grado_cl, grado_dhw):
        self.Project = Project
        self.grado_ht = grado_ht
        self.grado_cl = grado_cl
        self.grado_dhw = grado_dhw


    def start(self):
        return self.Project.analysisCalculation(self.grado_ht, self.grado_cl, self.grado_dhw)


