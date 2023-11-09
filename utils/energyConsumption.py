# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:51:06 2022

@author: avaquero
"""

from abc import ABC, abstractmethod
from interactors import estimationPV
import pandas as pd
from utils import meanCalculation


class currencyOutput(ABC):
    def __init__(self, grado_ht, grado_cl, grado_dhw, area, name):
        self.grado_ht = grado_ht
        self.grado_cl = grado_cl
        self.grado_dhw = grado_dhw
        self.area = area
        self.name = name
    """
        El método preMedium realiza las medias entre las viviendas
    """

    def process_dweelings(self, P_ht, P_cl, P_lig, P_dev, P_dhw, name):
        kwargs = {
            'P_ht': P_ht,
            'P_cl': P_cl,
            'P_lig': P_lig,
            'P_dev': P_dev,
            'P_dhw': P_dhw
        }
        output = {}
        for key, vector in kwargs.items():
            num_rows = len(pd.DataFrame(vector))
            result_dict = {}
            for column in pd.DataFrame(vector):
                result_list = [sum(x) / num_rows for x in zip(*pd.DataFrame(vector)[column])]
                result_dict[column] = [result_list]
            new_df = pd.DataFrame(result_dict)

            if name == 'Caracas1':
                simulations = set(new_df.columns.str.rsplit("_", n=1).str[0])
            else:
                simulations = new_df.columns
            summed_results = {}
            for sim in simulations:
                relevant_columns = [col for col in new_df.columns if col.startswith(sim)]
                summed_results[sim] = []
                for index, row in new_df.iterrows():
                    sum_list = [sum(elements) for elements in zip(*[row[col] for col in relevant_columns])]
                    summed_results[sim].append(sum_list)
            output[key] = summed_results

        return output['P_ht'], output['P_cl'], output['P_lig'], output['P_dev'], output['P_dhw']
    @abstractmethod
    def calculation(*args, EER_nrt, COP_nrt, COP_DHW_nrt, eta_cal_nrt, EER_rt, COP_rt, COP_DHW_rt, eta_cal_rt):
        pass

    
class ARV_CONS(currencyOutput):
    """
    Parameters:
        
        grado_ht (dict) -- Distribución de instalaciones calefacción 
        grado_cl (dict) -- Distribución de instalaciones refrigeración 
        grado_dhw (dict) -- Distribución de instalaciones agua caliente sanitaria         
        ref_cat (str) -- Referencia catastral ** Ahora es un parámetro, pero quizá debería ser un input porque el cálculo de PV en otros proyectos
                                                puede que no se tenga los m2 de cubierta en base de datos.
    """
    def __init__(self, grado_ht, grado_cl, grado_dhw, area, name, P_ht, P_cl, P_lig, P_dev, P_dhw ):
        super().__init__(grado_ht, grado_cl, grado_dhw, area, name)
        self.P_ht = P_ht
        self.P_cl = P_cl
        self.P_lig = P_lig
        self.P_dev = P_dev
        self.P_dhw = P_dhw
    def calculation(self, *args, name, EER_nrt = 2, COP_nrt = 2, COP_DHW_nrt = 1.7, eta_cal_nrt = 0.7, EER_rt = 5, COP_rt = 4.6, COP_DHW_rt = 3.17, eta_cal_rt = 0.92):
        """
        Inputs:
            
            *args (dicts) -- args está formado por P_ht, P_cl, P_lig, P_dev, P_dhw
            EER_nrt (float) -- eficiencia de refrigeración en el caso de no reforma (predefinido a 2 -> CE3X)
            COP_nrt (float) -- eficiencia de calefacción en el caso de no reforma (predefinido a 2 -> CE3X)
            COP_DHW_nrt (float) -- eficiencia de agua caliente sanitaria por bomba de calor en el caso de no reforma (predefinido a 1.7 -> CE3X)
            eta_cal_nrt (float) -- eficiencia de caldera/butano en el caso de no reforma (predefinido a 0.7 -> Optihub)
            EER_rt (float) -- eficiencia de refrigeración en el caso de reforma (predefinido a 5 -> ficha técnica DAIKIN)
            COP_rt (float) -- eficiencia de refrigeración en el caso de reforma (predefinido a 4.6 -> ficha técnica DAIKIN)
            COP_DHW_rt (float) -- eficiencia de refrigeración en el caso de reforma (predefinido a 3.17 -> ficha técnica BAXI)
            eta_cal_rt (float) -- eficiencia de refrigeración en el caso de reforma (predefinido a 0.92 -> CTE)           
            
        """        
        # Combinaciones en instalaciones
        
        Msplit = [1, 1, 1, 1, 0, 0, 0, 0]
        PV = [1, 1, 0, 0, 1, 1, 0, 0]
        BC = [1, 0, 1, 0, 1, 0, 1, 0]
        
        # Se utiliza args para facilitar el bucle para hacer las medias entre las vivienda simuladas
        
        #args_copy = list(args)
        #for i in range(0,len(args_copy)):
        #    args_copy[i] = super().preMedium(args_copy[i])

        #P_ht_hourly, P_cl_hourly, P_lig_hourly, P_dev_hourly, P_dhw_hourly = list(args).copy()

        project = meanCalculation.ARV_dwellings()
        output = meanCalculation.calculo(project, self.P_ht, self.P_cl, self.P_lig, self.P_dev, self.P_dhw, self.name)
        P_ht_mean, P_cl_mean, P_lig_mean, P_dev_mean, P_dhw_mean = output.start()

        P_ht_hourly, P_cl_hourly, P_lig_hourly, P_dev_hourly, P_dhw_hourly = super().process_dweelings(self.P_ht, self.P_cl, self.P_lig, self.P_dev,
                                                                                               self.P_dhw, name=self.name)
        # Consumos eléctricos que servirán como input al módulo de PV

        P_ht_ele_rt = {}
        P_cl_ele_rt = {}
        P_dhw_ele_rt = {}
        P_ht_ele_nrt = {}
        P_cl_ele_nrt = {}
        P_lig_ele = {}
        P_dev_ele = {}

        for key, values in P_ht_hourly.items():
            P_ht_ele_rt[key] = [[x / COP_rt for x in lst] for lst in values]
            P_cl_ele_rt[key] = [[x / EER_rt for x in lst] for lst in values]
            P_dhw_ele_rt[key] = [[x / COP_DHW_rt for x in lst] for lst in P_dhw_hourly[key]]
            P_ht_ele_nrt[key] = [[x * (self.grado_ht['joule'] + (self.grado_ht['BC']) / COP_nrt) for x in lst] for lst in values]
            P_cl_ele_nrt[key] = [[x / EER_nrt for x in lst] for lst in values]
            P_lig_ele[key] = P_lig_hourly[key]
            P_dev_ele[key] = P_dev_hourly[key]


        output_scenarios = {}
        
        # Preparación del diccionario output_scenarios con todas las opciones posibles de instalaciones

        for i in P_ht_mean:
            output_scenarios.setdefault(i, {})
            for j in range(0, len(Msplit)):
                key = []
                if Msplit[j] == 1:
                    key.append('Split_rf+')
                else:
                    key.append('Split_nrf+')
                if PV[j] == 1:
                    key.append('PV_yes+')
                else:
                    key.append('PV_no+')
                if BC[j] == 1:
                    key.append('BC_yes')
                else:
                    key.append('BC_no')
                output_scenarios[i].setdefault(("".join(key)), {'GN': 0, 'Ele': 0,
                                                                'Butano': 0})  # Se inicializan los vectores energéticos

        PV_estimation = {}
        total_electricity = {}

        for i in output_scenarios:
            PV_estimation.setdefault(i, {})
            total_electricity.setdefault(i, {})
            for j in output_scenarios[i]:
                P_ele_total = [0] * 8760  # Generación de una lista con 8760 ceros
                if 'Split_rf' in j:
                    output_scenarios[i][j]['Ele'] = output_scenarios[i][j]['Ele'] + (P_cl_mean[i]) / EER_rt + P_ht_mean[
                        i] / COP_rt
                if 'Split_nrf' in j:
                    output_scenarios[i][j]['Ele'] = output_scenarios[i][j]['Ele'] + (P_cl_mean[i]) / EER_nrt + \
                                                    P_ht_mean[i] * (self.grado_ht['joule'] + (self.grado_ht['BC']) / COP_nrt)
                    output_scenarios[i][j]['GN'] = output_scenarios[i][j]['GN'] + P_ht_mean[i] * (
                                (self.grado_ht['caldera_GN'] + self.grado_ht['nada']) / eta_cal_nrt)
                    output_scenarios[i][j]['Butano'] = output_scenarios[i][j]['Butano'] + P_ht_mean[i] * self.grado_ht[
                        'butano'] / eta_cal_nrt
                if 'BC_yes' in j:
                    output_scenarios[i][j]['Ele'] = output_scenarios[i][j]['Ele'] + P_dhw_mean[i] / COP_DHW_rt
                if 'BC_no' in j:
                    output_scenarios[i][j]['GN'] = output_scenarios[i][j]['GN'] + P_dhw_mean[i] * (
                                self.grado_dhw['caldera_GN'] / eta_cal_nrt)
                    output_scenarios[i][j]['Butano'] = output_scenarios[i][j]['Butano'] + P_dhw_mean[i] * (
                                self.grado_dhw['butano'] / eta_cal_nrt)
                if 'PV_yes' in j:  # Lógica de control para introducir la demanda en el código de PV
                    if 'Split_rf' in j:
                        P_ele_total = [x + y for x, y in zip(P_ele_total, P_cl_ele_rt[i][0])]
                        P_ele_total = [x + y for x, y in zip(P_ele_total, P_ht_ele_rt[i][0])]
                    if 'Split_nrf' in j:
                        P_ele_total = [x + y for x, y in zip(P_ele_total, P_cl_ele_nrt[i][0])]
                        P_ele_total = [x + y for x, y in zip(P_ele_total, P_ht_ele_nrt[i][0])]
                    if 'BC_yes' in j:
                        P_ele_total = [x + y for x, y in zip(P_ele_total, P_dhw_ele_rt[i][0])]

                total_electricity[i][j] = P_ele_total
                                        
                PV_estimation_aux = estimationPV.estimationPV(self.area, P_ele_total) # Llamada a interactor "puente" para el código de PV
                PV_estimation[i].setdefault(j,PV_estimation_aux)
                output_scenarios[i][j]['Ele'] = output_scenarios[i][j]['Ele'] - PV_estimation_aux # Si existe más producción de PV que demanda se añade un 0 en consumo eléctrico
                if  output_scenarios[i][j]['Ele']  < 0 :
                       output_scenarios[i][j]['Ele']  = 0
                                              
                if 'PV_no' in j:
                    PV_estimation[i].setdefault(j,0)
                        
        return output_scenarios, total_electricity, PV_estimation
    
    
    

class calculo:
    def __init__(self, project: currencyOutput, P_ht, P_cl, P_lig, P_dev,P_dhw, name, EER_nrt = 2, COP_nrt=2, COP_dhw_nrt=1.7, eta_cal_nrt=0.7, EER_rt = 5, COP_rt=4.6, COP_dhw_rt=3.17, eta_cal_rt=0.92):
        self.project = project
        self.P_ht = P_ht
        self.P_cl = P_cl
        self.P_lig = P_lig
        self.P_dev = P_dev
        self.P_dhw = P_dhw
        self.EER_nrt = EER_nrt
        self.COP_nrt = COP_nrt
        self.COP_dhw_nrt = COP_dhw_nrt
        self.eta_cal_nrt = eta_cal_nrt
        self.EER_rt = EER_rt
        self.COP_rt = COP_rt
        self.COP_dhw_rt = COP_dhw_rt
        self.eta_cal_rt = eta_cal_rt
        self.name = name

    def start(self):
        return self.project.calculation(self.P_ht, self.P_cl, self.P_lig,self.P_dev,self.P_dhw, EER_nrt = self.EER_nrt, COP_nrt = self.COP_nrt, COP_DHW_nrt=self.COP_dhw_nrt, eta_cal_nrt=self.eta_cal_nrt, EER_rt=self.EER_rt, COP_rt=self.COP_rt, COP_DHW_rt=self.COP_dhw_rt, eta_cal_rt=self.eta_cal_rt, name=self.name)

