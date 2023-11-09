 # -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""

# Abstract method import

from abc import ABC, abstractmethod

# Interactors

from interactors import getDataARV
from repositories import CMH
from SQL_statements import database_connection, getSurfacesTemp
import pandas as pd
from SQL_statements import database_connection, getSurfacesTemp
from sqlalchemy import text
from repositories import csvTRNSYS, CMH
import sys
# Abstract class



class detailedPEMcalculation_config(ABC):
    def __init__(self, windows, common_facilities, facilities, Pfees, iBen, gCost, DF,
          tender_down, VAT_material, VAT_project):
        self.windows = windows
        self.common_facilities = common_facilities
        self.facilities = facilities
        self.Pfees = Pfees
        self.iBen = iBen
        self.gCost = gCost
        self.DF = DF
        self.tender_down = tender_down
        self.VAT_material = VAT_material
        self.VAT_project = VAT_project


    @abstractmethod
    def PEMcalculation(self):
        pass


# Calculation of the investment with CMH data as a cost input
class detailedPEMcalculation(detailedPEMcalculation_config):
    """
    Parameters:
        
        windows (bool) -- Include windows in the budget         
        common_facilities (bool) -- common facilities renovation
        facilities (dict) -- Include facilities in the budget via dictionary with 3 booleans for 'DHW' domestic hot water, 'PV' photovoltaic, 'HVAC' air conditioning        
        Pfees (float) -- Project Fees
        iBen (float) -- Industrial Benefit
        gCost (float) -- General Costs
        DF (float) -- Project Management DF        
        tender_down (float) -- Price reduction during tender        
        VAT_material (float) -- Material taxes        
        VAT_project (floar) -- Project taxes        
    """
    def __init__(self, windows, common_facilities = False, facilities = {'DWH' : False, 'PV' : False, 'HVAC' : False}, Pfees = 0.09, iBen = 0.06, gCost = 0.03, DF=0.04, tender_down=0.11, VAT_material=0.1, VAT_project=0.21,):
        super().__init__(windows, common_facilities, facilities, Pfees, iBen, gCost, DF,
              tender_down, VAT_material, VAT_project)
    def PEMcalculation(self, ref_cat):
        """
        Inputs:
            ref_cat (string) -- Write ref_cat to analyse specific building or 'all' to analyse all the buildings in the DDBB    
        """
        import sys
        #if not isinstance(ref_cat,list):
         #   ref_cat = [ref_cat]

        direct = sys.path[0]  # Work path
        dir_2 = r'/resources/data/input_Prices.csv'
        direction = direct + dir_2      # Full path with input .csv
        typeFile = CMH.CMH_data()      # Repository to use
        get_data = CMH.getData_CMH(typeFile, direction)   # Prices from CMH
        CMH_data = get_data.start()        # Reposity Outputs -> Dict with €/m2 prices
        #sourceData = getDataARV.SQL_surfaceARV(ref_cat = ref_cat[0])    # SQL_statments ARV
        #get_data = getDataARV.getData_ARV(sourceData)   # Surfaces of each building
        # Reposity Outputs dicts -> 1) Area of each building (floor-roof-wall) with cadastral referece + 2) Partition ratio with cadastral referece
        #areabyCadastralcode, distributionRatio, ref_use = get_data.start()
        engine = database_connection.engine
        data_processor = getSurfacesTemp.DataProcessor(engine)
        areabyCadastralcode, distributionRatio, ref_use = data_processor.get_data(ref_cat)

        buildingCost = {}
        ww_ratio = 0.8
        for i in areabyCadastralcode:
            if i in ref_cat or ref_cat == 'all':
                buildingCost.setdefault(i, {})
                # cost_floor = (areabyCadastralcode[i]['floor']*float(CMH_data['Façanes (amb aïllament)']))  Cost of floor if necessary
                # Cost_wall · Area_wall ; Coeficiente 0.6 ventanas (40%) -> Variable number with real input value
                cost_wall = (
                    areabyCadastralcode[i]['wall']*ww_ratio*float(CMH_data['Façanes (amb aïllament)']))
                # Cost_roof · Area_roof
                cost_roof = (
                    areabyCadastralcode[i]['roof']*float(CMH_data['Cobertes (amb aïllament)']))
                # areabyCadastralcode[i]['floor_cost'] = cost_floor
                if self.windows == True:
                    cost_window = (
                        areabyCadastralcode[i]['wall']*(1-ww_ratio)*float(CMH_data['Substitució de finestres']))
                else:
                    cost_window = 0
                if self.facilities['DHW'] == True or self.facilities['DHW'] == 1:
                    cost_facilities_DHW = float(CMH_data['BC_DHW']) * \
                        len(distributionRatio[i])
                else:
                    cost_facilities_DHW = 0
                if self.facilities['PV'] == True or self.facilities['PV'] == 1:
                    cost_facilities_PV = float(CMH_data['PV']) * \
                        areabyCadastralcode[i]['roof']*0.25
                else:
                    cost_facilities_PV = 0
                if self.facilities['HVAC'] == True or self.facilities['DHW'] == 1:
                    cost_facilities_HVAC = float(CMH_data['HVAC']) * \
                        len(distributionRatio[i])
                else:
                    cost_facilities_HVAC = 0
                cost_common_facilities = 0
                if self.common_facilities == True:
                    for k in distributionRatio[i]:
                        if ref_use[i][k] == 'V':         
                            cost_common_facilities = cost_common_facilities + float(CMH_data['Total d’instal·lacions (aigua, sanejament, ventilació, electricitat i contra incendis)'])             
                else:
                    cost_common_facilities = 0
                    
                buildingCost[i].setdefault(
                    'wall_PEC', cost_wall*(1-self.tender_down))
                buildingCost[i].setdefault(
                    'roof_PEC', cost_roof*(1-self.tender_down))
                buildingCost[i].setdefault(
                    'windows_PEC', cost_window*(1-self.tender_down))
                buildingCost[i].setdefault(
                    'envelope_total_PEC', buildingCost[i]['wall_PEC'] + buildingCost[i]['roof_PEC'] + buildingCost[i]['windows_PEC'])               
                buildingCost[i].setdefault(
                    'common_facilities', cost_common_facilities*(1-self.tender_down))                        
                buildingCost[i].setdefault(
                    'facilities_DHW_PEC', cost_facilities_DHW*(1-self.tender_down))
                buildingCost[i].setdefault(
                    'facilities_PV_PEC', cost_facilities_PV*(1-self.tender_down))
                buildingCost[i].setdefault(
                    'facilities_HVAC_PEC', cost_facilities_HVAC*(1-self.tender_down))
                buildingCost[i].setdefault('facilities_total_PEC', (
                    buildingCost[i]['common_facilities'] + buildingCost[i]['facilities_PV_PEC'] + buildingCost[i]['facilities_HVAC_PEC'] + buildingCost[i]['facilities_DHW_PEC']))
                buildingCost[i].setdefault(
                    'Pfees', (buildingCost[i]['envelope_total_PEC']+buildingCost[i]['facilities_total_PEC']+buildingCost[i]['common_facilities'])*self.Pfees)
                buildingCost[i].setdefault(
                    'iBen', (buildingCost[i]['envelope_total_PEC']+buildingCost[i]['facilities_total_PEC']+buildingCost[i]['common_facilities'])*self.iBen)                
                buildingCost[i].setdefault(
                    'gCost', (buildingCost[i]['envelope_total_PEC']+buildingCost[i]['facilities_total_PEC']+buildingCost[i]['common_facilities'])*self.gCost)                
                buildingCost[i].setdefault(
                    'DF', (buildingCost[i]['envelope_total_PEC']+buildingCost[i]['facilities_total_PEC']+buildingCost[i]['common_facilities'])*self.DF)
                buildingCost[i].setdefault(
                    'Pfees_VAT', buildingCost[i]['Pfees']+buildingCost[i]['Pfees']*self.VAT_project)
                buildingCost[i].setdefault(
                    'iBen_VAT', buildingCost[i]['iBen']+buildingCost[i]['iBen']*self.VAT_project)                
                buildingCost[i].setdefault(
                    'gCost_VAT', buildingCost[i]['gCost']+buildingCost[i]['gCost']*self.VAT_project) 
                buildingCost[i].setdefault(
                    'DF_VAT', buildingCost[i]['DF']+buildingCost[i]['DF']*self.VAT_project) 
                buildingCost[i].setdefault('building_total_PEC_noVAT', buildingCost[i]['envelope_total_PEC']+buildingCost[i]['facilities_total_PEC'])                   
                buildingCost[i].setdefault('building_total_noVAT', buildingCost[i]['envelope_total_PEC'] +
                                              buildingCost[i]['facilities_total_PEC']+buildingCost[i]['Pfees']+buildingCost[i]['iBen']+buildingCost[i]['gCost']+buildingCost[i]['DF'])
                
                vatmtl = buildingCost[i]['envelope_total_PEC']+buildingCost[i]['facilities_total_PEC']
                vatgg =  buildingCost[i]['Pfees']+buildingCost[i]['iBen']+buildingCost[i]['gCost']+buildingCost[i]['DF']
                
                buildingCost[i].setdefault('building_total_VAT',(vatmtl*self.VAT_material+vatmtl)+(vatgg*self.VAT_project+vatgg))



        dwellingCost = {}

        for i in distributionRatio:
            

            if i in ref_cat or ref_cat == 'all':
                dwellingCost.setdefault(i,{})
                dwellings_count = 0
                for j in distributionRatio[i]:
                    dwellingCost[i].setdefault(j,{})
                    # The partition coefficient depends on the number of staircase. It is possible to have SUM(partition_coeffient) > 100 for the same building cadastral reference (14). With this line we correct it
    
                    # Avoid applying installation costs to non-dwelling references. It might be adjusted
                    if ref_use[i][j] == 'V':
                        dwellings_count = dwellings_count + 1
                        coef_escaleras=sum(list(distributionRatio[i].values()))/100
                        dwellingCost[i][j].setdefault('envelope_total_PEC',((distributionRatio[i][j])/(coef_escaleras*100)*buildingCost[i]['envelope_total_PEC']))  # Investment cost per dwelling
                        dwellingCost[i][j].setdefault('facilities_total_PEC',((distributionRatio[i][j])/(coef_escaleras*100)*buildingCost[i]['facilities_total_PEC']))
                        dwellingCost[i][j].setdefault('common_facilities',((distributionRatio[i][j])/(coef_escaleras*100)*buildingCost[i]['common_facilities']))                        
                        dwellingCost[i][j].setdefault('dwelling_total_noVAT',((distributionRatio[i][j])/(coef_escaleras*100)*buildingCost[i]['building_total_noVAT']))
                        dwellingCost[i][j].setdefault('dwelling_total_VAT',((distributionRatio[i][j])/(coef_escaleras*100)*buildingCost[i]['building_total_VAT']))
                    else:
                        dwellingCost[i][j].setdefault('envelope_total_PEC', 0)  
                        dwellingCost[i][j].setdefault('facilities_total_PEC', 0)
                        dwellingCost[i][j].setdefault('common_facilities', 0)
                        dwellingCost[i][j].setdefault('dwelling_total_noVAT', 0)
                        dwellingCost[i][j].setdefault('dwelling_total_VAT', 0)      
                buildingCost[i].setdefault('nDwellings',dwellings_count)


        return CMH_data, areabyCadastralcode, distributionRatio, buildingCost, dwellingCost

class detailedPEMcalculationPalma(detailedPEMcalculation_config):

    def __init__(self, windows, common_facilities = False, facilities = {'DWH' : False, 'PV' : False, 'HVAC' : False}, Pfees = 0.09, iBen = 0.06, gCost = 0.03, DF=0.04, tender_down=0.11, VAT_material=0.1, VAT_project=0.21):
        super().__init__(windows, common_facilities, facilities, Pfees, iBen, gCost, DF,tender_down, VAT_material, VAT_project)
    def PEMcalculation(self, refcat, materials, config,areabyCadastralcode, distributionRatio, ref_use):

        direct = sys.path[0]  # Work path
        dir_2 = r'/resources/data/input_Prices.csv'
        direction = direct + dir_2
        typeFile = CMH.CMH_data()
        get_data = CMH.getData_CMH(typeFile, direction)
        CMH_data = get_data.start()


        buildingCost = {}
        if not config.startswith('BC0'):
            wall_type = config.split("_")[2]
            roof_type = config.split("_")[3]
            pattern = config.split("_")[0]
        else:
            wall_type = None
            roof_type = None
            pattern = None

        if not config.startswith('BC0'):

            cost_wall = materials.loc[(materials['tipus'] == 'mur')&(materials['espesor']==wall_type)&(materials['convecional_eco']==int(pattern[2]))&(materials['opcion']==int(pattern[3]))]['cost'].iloc[0]
            cost_roof = materials.loc[(materials['tipus'] == 'coberta') & (materials['espesor'] == roof_type) & (materials['convecional_eco'] == int(pattern[2])) & (materials['opcion'] == int(pattern[3]))]['cost'].iloc[0]

            if int(config[1]) == 1:
                cost_window = 0
            else:
                cost_window = materials.loc[(materials['tipus'] == 'finestra') & (materials['convecional_eco'] == int(pattern[2]))]['cost'].iloc[0]

            if 'forjat' not in set(materials['tipus']):
                cost_slab = 0
            else:
                cost_slab = materials.loc[(materials['tipus'] == 'forjat') & (materials['convecional_eco'] == int(config[2])) & (materials['espesor_mm'].astype('int') == 60)]['cost'].iloc[0]

            if self.facilities['DHW'] == True or self.facilities['DHW'] == 1:
                cost_facilities_DHW = float(CMH_data['BC_DHW']) * len(distributionRatio[refcat])
            else:
                cost_facilities_DHW = 0

            if self.facilities['PV'] == True or self.facilities['PV'] == 1:
                cost_facilities_PV = float(CMH_data['PV']) * (areabyCadastralcode[refcat]['roof'] * 0.8) * 0.25
            else:
                cost_facilities_PV = 0

            if self.facilities['HVAC'] == True or self.facilities['DHW'] == 1:
                cost_facilities_HVAC = float(CMH_data['HVAC']) * len(distributionRatio[refcat])
            else:
                cost_facilities_HVAC = 0
                cost_common_facilities = 0

            if self.common_facilities == True:
                for k in distributionRatio[refcat]:
                    if ref_use[refcat][k] == 'V':
                         cost_common_facilities = cost_common_facilities + float(CMH_data['Total d’instal·lacions (aigua, sanejament, ventilació, electricitat i contra incendis)'])
            else:
                cost_common_facilities = 0
        else:
            cost_wall = 0
            cost_roof = 0
            cost_window = 0
            cost_slab = 0
            cost_facilities_DHW = 0
            cost_facilities_HVAC = 0
            cost_facilities_PV = 0
            cost_common_facilities = 0

        buildingCost.setdefault(refcat, {}).setdefault('wall_PEC', cost_wall * (1 - self.tender_down))
        buildingCost.setdefault(refcat, {}).setdefault('roof_PEC', cost_roof * (1 - self.tender_down))
        buildingCost.setdefault(refcat, {}).setdefault('windows_PEC', cost_window * (1 - self.tender_down))
        buildingCost.setdefault(refcat, {}).setdefault('slab_PEC', cost_slab * (1 - self.tender_down))
        envelope_total_PEC = buildingCost[refcat]['wall_PEC'] + buildingCost[refcat]['roof_PEC'] + buildingCost[refcat]['windows_PEC'] + buildingCost[refcat]['slab_PEC']
        buildingCost.setdefault(refcat, {}).setdefault('envelope_total_PEC', envelope_total_PEC)
        buildingCost.setdefault(refcat, {}).setdefault('common_facilities',cost_common_facilities * (1 - self.tender_down))
        buildingCost.setdefault(refcat, {}).setdefault('facilities_DHW_PEC',cost_facilities_DHW * (1 - self.tender_down))
        buildingCost.setdefault(refcat, {}).setdefault('facilities_PV_PEC', cost_facilities_PV * (1 - self.tender_down))
        buildingCost.setdefault(refcat, {}).setdefault('facilities_HVAC_PEC',cost_facilities_HVAC * (1 - self.tender_down))
        facilities_total_PEC = buildingCost[refcat]['common_facilities'] + buildingCost[refcat]['facilities_PV_PEC'] + buildingCost[refcat]['facilities_HVAC_PEC'] + buildingCost[refcat]['facilities_DHW_PEC']
        buildingCost.setdefault(refcat, {}).setdefault('facilities_total_PEC', facilities_total_PEC)
        building_total_PEC_noVAT = envelope_total_PEC + facilities_total_PEC

        buildingCost.setdefault(refcat, {}).setdefault('Pfees', building_total_PEC_noVAT * self.Pfees)
        buildingCost.setdefault(refcat, {}).setdefault('iBen', building_total_PEC_noVAT * self.iBen)
        buildingCost.setdefault(refcat, {}).setdefault('gCost', building_total_PEC_noVAT * self.gCost)
        buildingCost.setdefault(refcat, {}).setdefault('DF', building_total_PEC_noVAT * self.DF)

        Pfees_VAT = buildingCost[refcat]['Pfees'] + buildingCost[refcat]['Pfees'] * self.VAT_project
        iBen_VAT = buildingCost[refcat]['iBen'] + buildingCost[refcat]['iBen'] * self.VAT_project
        gCost_VAT = buildingCost[refcat]['gCost'] + buildingCost[refcat]['gCost'] * self.VAT_project
        DF_VAT = buildingCost[refcat]['DF'] + buildingCost[refcat]['DF'] * self.VAT_project

        building_total_noVAT = envelope_total_PEC + facilities_total_PEC + buildingCost[refcat]['Pfees'] + buildingCost[refcat]['iBen'] + buildingCost[refcat]['gCost'] + buildingCost[refcat]['DF']
        buildingCost.setdefault(refcat, {}).setdefault('building_total_noVAT', building_total_noVAT)
        buildingCost.setdefault(refcat, {}).setdefault('Pfees_VAT', Pfees_VAT)
        buildingCost.setdefault(refcat, {}).setdefault('iBen_VAT', iBen_VAT)
        buildingCost.setdefault(refcat, {}).setdefault('gCost_VAT', gCost_VAT)
        buildingCost.setdefault(refcat, {}).setdefault('DF_VAT', DF_VAT)
        buildingCost.setdefault(refcat, {}).setdefault('building_total_PEC_noVAT', building_total_PEC_noVAT)

        vatmtl = envelope_total_PEC + facilities_total_PEC
        vatgg = buildingCost[refcat]['Pfees'] + buildingCost[refcat]['iBen'] + buildingCost[refcat]['gCost'] + buildingCost[refcat]['DF']

        building_total_VAT = (vatmtl * self.VAT_material + vatmtl) + (vatgg * self.VAT_project + vatgg)

        buildingCost.setdefault(refcat, {}).setdefault('building_total_VAT', building_total_VAT)

        dwellingCost = {}

        for i in distributionRatio:

            dwellingCost.setdefault(i, {})
            dwellings_count = 0

            for j in distributionRatio[i]:
                dwellingCost[i].setdefault(j, {})
                # The partition coefficient depends on the number of staircase. It is possible to have SUM(partition_coeffient) > 100 for the same building cadastral reference (14). With this line we correct it

                # Avoid applying installation costs to non-dwelling references. It might be adjusted
                if ref_use[i][j] == 'V':
                    dwellings_count = dwellings_count + 1
                    coef_escaleras = sum(list(distributionRatio[i].values())) / 100
                    dwellingCost[i][j].setdefault('envelope_total_PEC', ((distributionRatio[i][j]) / (coef_escaleras * 100) * buildingCost[refcat]['envelope_total_PEC']))  # Investment cost per dwelling
                    dwellingCost[i][j].setdefault('facilities_total_PEC', ((distributionRatio[i][j]) / (coef_escaleras * 100) * buildingCost[refcat]['facilities_total_PEC']))
                    dwellingCost[i][j].setdefault('common_facilities', ((distributionRatio[i][j]) / (coef_escaleras * 100) * buildingCost[refcat]['common_facilities']))
                    dwellingCost[i][j].setdefault('dwelling_total_noVAT', ((distributionRatio[i][j]) / (coef_escaleras * 100) * buildingCost[refcat]['building_total_noVAT']))
                    dwellingCost[i][j].setdefault('dwelling_total_VAT', ((distributionRatio[i][j]) / (coef_escaleras * 100) * buildingCost[refcat]['building_total_VAT']))
                else:
                    dwellingCost[i][j].setdefault('envelope_total_PEC', 0)
                    dwellingCost[i][j].setdefault('facilities_total_PEC', 0)
                    dwellingCost[i][j].setdefault('common_facilities', 0)
                    dwellingCost[i][j].setdefault('dwelling_total_noVAT', 0)
                    dwellingCost[i][j].setdefault('dwelling_total_VAT', 0)
            buildingCost[refcat].setdefault('nDwellings', dwellings_count)

        return CMH_data, areabyCadastralcode, distributionRatio, buildingCost, dwellingCost
    
    
    
if __name__ == '__main__':

    escenario_1 = detailedPEMcalculation(windows = True, facilities = {'DHW' : False, 'PV' : False, 'HVAC' : False})
    CMH_data, areabyCadastralcode, distributionRatio, buildingCost, dwellingCost = escenario_1.PEMcalculation(ref_cat = '1502002DD7810B')
    