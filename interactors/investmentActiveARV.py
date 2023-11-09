# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""

#Abstract method import

from abc import ABC, abstractmethod

# Interactors

from interactors import calculoCoste, calculoCoste
from SQL_statements import database_connection, getSurfacesTemp
from sqlalchemy import text
import pandas as pd

# Abstract class

class currencyProject(ABC):
    def __init__(self, output_scenarios, ref_cat_analysis, name):
        self.output_scenarios = output_scenarios
        self.ref_cat_analysis = ref_cat_analysis
        self.name = name
    @abstractmethod
    def calculationInvestment(self):
        pass

class investmentActive_ARV(currencyProject):  # Calculation of the investment with CMH data as a cost input
    def __init__(self, output_scenarios, ref_cat_analysis, name):
        currencyProject.__init__(self,  output_scenarios, ref_cat_analysis, name)
    def calculationInvestment(self):

        engine = database_connection.engine

        with open('SQL_statements/materials.sql', 'r') as file:
            materials_query = file.read()

            # Execute the query with the parcela variable
        with engine.connect() as connection:
            query = text(materials_query)
            materials = pd.read_sql_query(query, connection, params={"Arquetipo": self.name})
            materials[['convecional_eco', 'opcion']] = materials[['convecional_eco', 'opcion']].astype('int')

        engine2 = database_connection.engine
        data_processor = getSurfacesTemp.DataProcessor(engine)
        areabyCadastralcode, distributionRatio, ref_use = data_processor.get_data(self.ref_cat_analysis)

        buildingCost_active = {}
        dwellingCost_active = {}
        dwellings_fees_active = {}
        buildingGrants_active = {}
        deltaEPNR_active = {}
        PE_active= {}
        EPNR_BC = {}
        for i in self.output_scenarios:
            buildingCost_active.setdefault(str(i),{})
            dwellingCost_active.setdefault(str(i),{})
            dwellings_fees_active.setdefault(str(i),{})
            buildingGrants_active.setdefault(str(i),{})
            deltaEPNR_active.setdefault(str(i),{})
            for j in self.output_scenarios[i]:
                facilities = {'HVAC' : False, 'PV' : False, 'DHW' : False}
                if 'Split_rf' in j:
                    facilities['HVAC'] = True
                if 'PV_yes'in j:
                    facilities['PV'] = True
                if 'BC_yes' in j:
                    facilities['DHW'] = True
                    windows = False
                    PE_active.setdefault(i,0)
                    i_aux = i.split('_') # Identificación de los parámetros de la simulación (ver "detallesinputs")
                    i_aux_2 = list(i_aux[0])    # Identificación de los parámetros de la simulación (ver "detallesinputs")
                if 'BC' in i:
                    EPNR_BC.setdefault(i,self.output_scenarios[i]['Split_nrf+PV_no+BC_no']) 
                    deltaEPNR_active[i][str(j)] = 0 
                    PE_active[i] = EPNR_BC[i]             
                if not 'BC' in i:
                    if i_aux_2[1] == str(1): # Identificación de los parámetros de la simulación (ver "detallesinputs")
                        windows = False
                    else:
                        windows = True
                    PE_active[i] = self.output_scenarios[i][j]
                    if i_aux[1] == str(0): # Identificación de los parámetros de la simulación (ver "detallesinputs")
                        EPNR_BC_aux =  EPNR_BC['BC0_'+str(0)]              
                    if i_aux[1] == str(90):
                        EPNR_BC_aux =  EPNR_BC['BC0_'+str(90)]  
                    if i_aux[1] == str(180):
                        EPNR_BC_aux =  EPNR_BC['BC0_'+str(180)]  
                    if i_aux[1] == str(270):
                        EPNR_BC_aux =  EPNR_BC['BC0_'+str(270)]  
                    deltaEPNR_active[i][str(j)] = (1-(PE_active[i]/EPNR_BC_aux))*100


                """
                Llamada al modelo económico
                *** El método calculoCuota_CMH utilza los datos de un Excel, en el caso de ARV se debe cambiar y programar.
                La subvención predefinida es el programa 3 de rehabilitación de edificios (limites y % de subveción)
                """

                #cuotaCalc = calculoCoste.calculoCuota_CMH(windows = windows, common_facilities = False, facilities = facilities, Pfees = 0.02, DF = 0.03, tender_down = 0.1, deltaEPNR = deltaEPNR_active[i][str(j)], ref_cat_analysis = self.ref_cat_analysis)
                fin_calculation = calculoCoste.calculoCuota_Palma(windows = windows, common_facilities = False,facilities= facilities, deltaEPNR = deltaEPNR_active[i][str(j)] ,Pfees = 0.02,  DF = 0.03,tender_down = 0.1,  ref_cat_analysis = self.ref_cat_analysis, materials= materials,areabyCadastralcode=areabyCadastralcode, distributionRatio=distributionRatio, ref_use=ref_use, config=i)
                calc = calculoCoste.calculationCuote(fin_calculation)
                buildingCost_aux, dwellingCost_aux, dwellings_fees_aux, buildingGrants_aux = calc.start()
                buildingCost_active[i][str(j)]= buildingCost_aux
                dwellingCost_active[i][str(j)]= dwellingCost_aux
                dwellings_fees_active[i][str(j)]= dwellings_fees_aux 
                buildingGrants_active[i][str(j)]= buildingGrants_aux

        return buildingCost_active, dwellingCost_active, dwellings_fees_active, buildingGrants_active, deltaEPNR_active


    

        
class calculation:
    def __init__(self, project : currencyProject):
        self.project = project    
    def start(self):    
        return self.project.calculationInvestment()


