# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:51:06 2022

@author: avaquero
"""

from abc import ABC, abstractmethod
from utils import meanCalculation

class currencyOutput(ABC):

    @abstractmethod
    def calculation(self, PE_ht, PE_cl, PE_lig,PE_dev ,PE_dhw, PE_ht_rt, PE_cl_rt, PE_lig_rt,PE_dev_rt ,PE_dhw_rt, name,PV_estimation):
        pass


class ARV_Scenarios(currencyOutput):
    def calculation(self,PE_ht,PE_cl,PE_lig, PE_dev, PE_dhw, PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt, PE_dhw_rt, name, PV_estimation):
        Msplit = [1, 1, 1, 1, 0, 0, 0, 0]
        PV = [1, 1, 0, 0, 1, 1, 0, 0]
        BC = [1, 0, 1, 0, 1, 0, 1, 0]

        project = meanCalculation.ARV_dwellings()
        output = meanCalculation.calculo(project, PE_ht, PE_cl, PE_lig, PE_dev, PE_dhw, name)
        PE_ht_mean, PE_cl_mean, PE_lig_mean, PE_dev_mean, PE_dhw_mean = output.start()

        project = meanCalculation.ARV_dwellings()
        output = meanCalculation.calculo(project, PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt, PE_dhw_rt, name)
        PE_ht_rt_mean, PE_cl_rt_mean, PE_lig_rt_mean, PE_dev_rt_mean, PE_dhw_rt_mean = output.start()
        
        """
        Cálculo de energía primaria en función del escenario de medidas activas (electricidad - gas natural - butano) 
            1) Se introduce la energía primaria de todos los escenarios posibles (rehabilitado o no)
            2) Bucle que recorre todas las combinaciones posibles de instalaciones
            3) Se suma el valor correspondiente
        EJEMPLO -> en el caso del sistema de climatización
            IF YES -> Se suma la energía primaria en cooling y heating rehabilitado
            IF NOT -> Se suma la energía primaria de cooling y heating sin rehabilitar
        """

        output_scenarios = {}
        for k in PE_ht_rt_mean:
            output_scenarios.setdefault(k, {})
            for i in range(0, len(Msplit)):
                key = []
                value = []
                if Msplit[i] == 1:
                    key.append('Split_rf+')
                    value.append(PE_cl_rt_mean[k] + PE_ht_rt_mean[k])
                else:
                    key.append('Split_nrf+')
                    value.append(PE_cl_mean[k] + PE_ht_mean[k])
                if PV[i] == 1:
                    key.append('PV_yes+')
                    if Msplit[i] == 0 and BC[i] == 0:
                        value.append(-PV_estimation[k]['Split_nrf+PV_yes+BC_no'] * 2.968)
                    elif Msplit[i] == 0 and BC[i] == 1:
                        value.append(-PV_estimation[k]['Split_nrf+PV_yes+BC_yes'] * 2.968)
                    elif Msplit[i] == 1 and BC[i] == 0:
                        value.append(-PV_estimation[k]['Split_rf+PV_yes+BC_no'] * 2.968)
                    elif Msplit[i] == 1 and BC[i] == 1:
                        value.append(-PV_estimation[k]['Split_rf+PV_yes+BC_yes'] * 2.968)
                else:
                    key.append('PV_no+')
                    value.append(0)
                if BC[i] == 1:
                    key.append('BC_yes')
                    value.append(PE_dhw_rt_mean[k])

                else:
                    key.append('BC_no')
                    value.append(PE_dhw_mean[k])

                output_scenarios[k].setdefault(("".join(key)), sum(value))

        return output_scenarios
 
    
class calculo:
    def __init__(self, project: currencyOutput, PE_ht, PE_cl, PE_lig,PE_dev, PE_dhw, PE_ht_rt, PE_cl_rt, PE_lig_rt,PE_dev_rt ,PE_dhw_rt, PV_estimation, name):
        self.project= project
        self.PE_ht= PE_ht
        self.PE_cl= PE_cl
        self.PE_lig= PE_lig
        self.PE_dev = PE_dev
        self.PE_dhw= PE_dhw
        self.PE_ht_rt= PE_ht_rt
        self.PE_cl_rt= PE_cl_rt
        self.PE_lig_rt= PE_lig_rt
        self.PE_dev_rt = PE_dev_rt
        self.PE_dhw_rt= PE_dhw_rt
        self.PV_estimation = PV_estimation
        self.name = name

    def start(self):
        return self.project.calculation(self.PE_ht, self.PE_cl, self.PE_lig,self.PE_dev, self.PE_dhw, self.PE_ht_rt, self.PE_cl_rt, self.PE_lig_rt,self.PE_dev_rt ,self.PE_dhw_rt, PV_estimation = self.PV_estimation, name = self.name)
