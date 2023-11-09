# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:51:06 2022

@author: srabadan
"""

from abc import ABC, abstractmethod
from interactors import estimationPV

class currencyOutput(ABC):
    def __init__(self, output_scenarios_cons, precio_ele, precio_gas, precio_butano, degradacion_inst_i, tasa_inflacion_i, years, surface):
        self.output_scenarios_cons = output_scenarios_cons
        self.precio_ele = precio_ele 
        self.precio_gas = precio_gas 
        self.precio_butano = precio_butano 
        self.degradacion_inst_i = degradacion_inst_i
        self.tasa_inflacion_i = tasa_inflacion_i
        self.years = years
        self.surface = surface
    @abstractmethod
    def calculation(self, Maintenance_BC, Replacement_BC, Maintenance_inst, Replacement_inst, PV_estimation):
        pass


class globalCost_ARV(currencyOutput):
    """
    Parameters:
        
        output_scenarios_cons (dict) -- Diccionario con los consumos según escenario de medidas activas
        precio_ele (float) -- Precio de la electricidad inicial
        precio_gas (float) -- Precio del gas inicial
        precio_butano (float) -- Precio del butano inicial
        degradacion_inst_i (float)  -- % de degradación de eficiencia en instalaciones anual
        tasa_inflacion_i (float) -- % de inflación anual de los precios
        years (int) -- años del estudio    
        surface (float)  -- Superficie en m2 de la vivienda        
        
    """
    def __init__(self, output_scenarios_cons, precio_ele, precio_gas, precio_butano, degradacion_inst_i, tasa_inflacion_i, years, surface):
        currencyOutput.__init__(self, output_scenarios_cons, precio_ele, precio_gas, precio_butano, degradacion_inst_i, tasa_inflacion_i, years, surface)

    def calculation(self, Maintenance_BC, Replacement_BC, Maintenance_inst, Replacement_inst, PV_estimation):

        energyCost = {}
        maintenanceCost = {}
        replaceCost = {}
        degradacion_inst =  -0.005
        tasa_inflacion = -0.01        
        Msplit = [1, 1, 1, 1, 0, 0, 0, 0]
        PV = [1, 1, 0, 0, 1, 1, 0, 0]
        BC = [1, 0, 1, 0, 1, 0, 1, 0]
        for self.year in range(1, self.years):  # Actualización anual de coeficientes
            degradacion_inst = degradacion_inst + self.degradacion_inst_i  
            tasa_inflacion = tasa_inflacion +  self.tasa_inflacion_i
            self.precio_butano = self.precio_butano/(1-self.tasa_inflacion_i)
            self.precio_ele = self.precio_ele/(1-self.tasa_inflacion_i)
            self.precio_gas = self.precio_gas/(1-self.tasa_inflacion_i)
            if  self.year == 25: # Renovación de instalciones y vuelta a la degradación 0
                degradacion_inst =  self.degradacion_inst_i
            for i in self.output_scenarios_cons:
                energyCost.setdefault(i, {})
                for j in self.output_scenarios_cons[i]: 
                    # Para el cálculo del coste de energía se tiene en cuenta el autoconsumo
                    consumption_GN = (self.output_scenarios_cons[i][j]['GN']/(1-self.degradacion_inst_i))*self.precio_gas
                    consumption_ele = (self.output_scenarios_cons[i][j]['Ele']/(1-self.degradacion_inst_i)+PV_estimation[i][j])*self.precio_ele - PV_estimation[i][j]*(1-self.degradacion_inst_i)*self.precio_ele
                    consumption_but = self.output_scenarios_cons[i][j]['Butano']/(1-self.degradacion_inst_i)*self.precio_butano
                    if self.year == 1:
                        energyCost[i].setdefault(j, (consumption_GN + consumption_ele + consumption_but)*self.surface)
                    else:
                        energyCost[i][j] = energyCost[i][j] + (consumption_GN + consumption_ele + consumption_but)*self.surface

                        
            for i in self.output_scenarios_cons: # Asignación de los costes de mantenimiento y replacement según el escenario
                count = -1
                maintenanceCost.setdefault(i, {})
                replaceCost.setdefault(i, {})
                for j in self.output_scenarios_cons[i]:
                    price_sum_main = 0
                    price_sum_repl = 0
                    count = count + 1           
                    if Msplit[count] == 1:
                        price_sum_main = price_sum_main + Maintenance_inst[2]
                        price_sum_repl = price_sum_repl + Replacement_inst[2]
                    else:
                        price_sum_main = price_sum_main + Maintenance_BC[2]
                        price_sum_repl = price_sum_repl + Replacement_BC[2]                        
                    if PV[count] == 1:
                        price_sum_main = price_sum_main + Maintenance_inst[0]
                        price_sum_repl = price_sum_repl + Replacement_inst[0]
                    else:
                        price_sum_main = price_sum_main + Maintenance_BC[0]
                        price_sum_repl = price_sum_repl + Replacement_BC[0] 
                    if BC[count] == 1:
                        price_sum_main = price_sum_main + Maintenance_inst[1]
                        price_sum_repl = price_sum_repl + Replacement_inst[1]
                    else:
                        price_sum_main = price_sum_main + Maintenance_BC[1]
                        price_sum_repl = price_sum_repl + Replacement_BC[1] 

                    if self.year == 1:
                        maintenanceCost[i].setdefault(j, 0)
                        replaceCost[i].setdefault(j, 0)
                    else:
                        maintenanceCost[i][j] = maintenanceCost[i][j] + price_sum_main
                        replaceCost[i][j] = replaceCost[i][j] + price_sum_repl
        return energyCost, maintenanceCost, replaceCost



   
class calculo:
    def __init__(self, project: currencyOutput, Maintenance_BC, Replacement_BC, Maintenance_inst, Replacement_inst, PV_estimation):
        self.project = project
        self.Maintenance_BC = Maintenance_BC
        self.Replacement_BC = Replacement_BC
        self.Maintenance_inst = Maintenance_inst
        self.Replacement_inst = Replacement_inst
        self.PV_estimation = PV_estimation


    def start(self):
        return self.project.calculation(self.Maintenance_BC, self.Replacement_BC, self.Maintenance_inst, self.Replacement_inst, self.PV_estimation)
