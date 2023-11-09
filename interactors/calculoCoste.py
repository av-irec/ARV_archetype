# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: avaquero
"""

#Abstract method import

from abc import ABC, abstractmethod

# Interactors

from interactors import executionCost, userType, executionCost
from utils import financialCost, grantsEstimation, operationalCost, economicBalance


# Abstract class

class currencySource(ABC):
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
        ref_cat_analysis (str) -- Referencia catastral    
        deltaEPNR (float) -- Reducción de energía primaria para el cálculo de la subvención      
    """
    def __init__(self, windows, common_facilities, facilities, Pfees, DF, tender_down, ref_cat_analysis, deltaEPNR):
        self.windows = windows
        self.common_facilities = common_facilities
        self.facilities = facilities
        self.Pfees = Pfees
        self.DF = DF
        self.tender_down = tender_down
        self.ref_cat_analysis = ref_cat_analysis
        self.deltaEPNR = deltaEPNR
    def executeCommonCode(self, ref_cat_analysis, buildingCost, dwellingCost, distributionRatio):
        """
        Método que ejecuta la parte del modelo económico que es comun independientemente de los precios
        """
                
        # User type
        scenario_usertype = userType.propertyKnown({'UT1': 15, 'UT2':  50, 'UT3': 10, 'UT4': 15, 'UT5': 10})
        dict_owners, dict_owners_output,  output_usertype = scenario_usertype.userTypeInsert(ref_cat_analysis)
        
        
        # Operational Cost       
        n_dwellings = 0
        
        for i in buildingCost:
            n_dwellings = n_dwellings + buildingCost[i]['nDwellings']
        
        distribution_config = {"Public": [1, 1, 0.2, 0.2, 0.2], "Private": [0, 0, 0.8, 0.8, 0.8]}
        distribution_cost_phases_conf = {"Pre-initial" : 0.1, "Initial" : 0.3, "Project" : 0.35, "Execution" : 0.15, "Financial support" : 0.1}
        escenario_1_oper = operationalCost.operationalCost(fix_cost = 10000, variable_cost=400, n_dwellings=n_dwellings, distribution_cost=distribution_config, distribution_cost_phases = distribution_cost_phases_conf)
        public_works, private_works_noVAT, private_works_VAT = escenario_1_oper.operationalCalculation()       
              
         # Financial Cost
        loan_perc = 0.3
        loan = buildingCost[ref_cat_analysis]['building_total_noVAT']*loan_perc
        escenario_1_financial = financialCost.financialCost(loan)
        years_amortization = 5
        interest_rate_AR = 5
        financial_cost, monthly_payment, monthly_interest, monthly_capital, capital_amortization, interest_yearly = escenario_1_financial.financialCalculation(
            interest_rate_AR, years_amortization)
       
        # Grant Estimation PROGRAMA 3 DE SUBVENCIONES NEXT GENERATION
        if self.deltaEPNR < 30:
            grant_estimated = 0
            grant_limit = 10000000
        if 30 <= self.deltaEPNR and self.deltaEPNR < 45:  
            grant_estimated = 40
            grant_limit = 6300
        if 45 <= self.deltaEPNR and self.deltaEPNR < 60:  
            grant_estimated = 65
            grant_limit = 11600
        if self.deltaEPNR >= 60:  
            grant_estimated = 80
            grant_limit = 18800            
        
        project_grant = grantsEstimation.grantEstimation(grant_estimated, 2, grant_limit*n_dwellings)
        material_grant = grantsEstimation.grantEstimation(grant_estimated, 2, grant_limit*n_dwellings)
        operational_grant = grantsEstimation.grantEstimation(grant_estimated, 2, grant_limit*n_dwellings)
        
        grant_building_proj = {}
        grant_building_mat = {}
       
        for i in buildingCost:
            grant_building_proj.setdefault(i, 0)
            grant_building_mat.setdefault(i, 0)

            grant_output_proj, cost_without_grant_proj, limitation_proj = project_grant.grantCalculation(buildingCost[i]['Pfees']+buildingCost[i]['DF'], buildingCost[i]['nDwellings'])
            grant_output_mat, cost_without_grant_mat, limitation_mat = material_grant.grantCalculation(buildingCost[i]['building_total_noVAT'], buildingCost[i]['nDwellings'])
            grant_building_proj[i] = grant_output_proj
            grant_building_mat[i] = grant_output_mat
            grant_output_ope, cost_without_grant_ope, limitation_ope = operational_grant.grantCalculation(private_works_noVAT['Total_costs']-private_works_noVAT['Financial support'], n_dwellings=n_dwellings)    
            
                
            if  grant_limit <= (grant_building_mat[i] + grant_building_proj[i])/buildingCost[i]['nDwellings'] + grant_output_ope/n_dwellings:
                coef = grant_limit/((grant_building_mat[i] + grant_building_proj[i])/buildingCost[i]['nDwellings'] + grant_output_ope/n_dwellings)
                grant_building_mat[i] = grant_building_mat[i]*coef
                grant_output_ope = grant_output_ope*coef
                grant_building_proj[i] = grant_building_proj[i] * coef

                
            building_grants = {'Project': grant_building_proj,'Material': grant_building_mat, 'Operational': grant_output_ope}            
           
        building_grants = {'Project': grant_building_proj,'Material': grant_building_mat, 'Operational': grant_output_ope}
         # Economic balance

        economic_scenario = economicBalance.economic_Balance({'Pre-initial': 3, 'Initial': 3, 'Project': 6, 'Execution': 12}, fee_start=7, grant_start={
                                                             14: 30, 20: 20, 25: 50}, loan_start={'get_loan':13,'start_payment':25,'loan':loan}, public_payment=100000, financial_cost = False, defaulter_risk = False, UT5_payment = True)
        distribution_ratio_input = {key: value for key, value in distributionRatio.items() if key in ref_cat_analysis}
        economic_balance_detailed, economic_balance_summary, economic_balance_VAT, cash_flow, dwellings_fees = economic_scenario.cashflow_calculation(
            buildingCost, dwellingCost, dict_owners_output, private_works_noVAT, private_works_VAT, monthly_payment, years_amortization, building_grants, interest_rate_UT2=5, interest_rate_UT3=5, over_head = 20, benefit_expected = 20, distribution_ratio = distribution_ratio_input)
        
        return buildingCost, dwellingCost, dwellings_fees, building_grants       
           
    @abstractmethod
    def calculo_Cuota(self):
        pass

class calculoCuota_CMH(currencySource):  # Calculation of the investment with CMH data as a cost input
    def __init__(self, windows, common_facilities, facilities, Pfees, DF, tender_down, ref_cat_analysis, deltaEPNR):
        currencySource.__init__(self, windows, common_facilities, facilities, Pfees, DF, tender_down, ref_cat_analysis, deltaEPNR)
    def calculo_Cuota(self): 

        
        # Execution Cost      
        escenario_1_exe = executionCost.detailedPEMcalculation(self.windows, self.common_facilities, self.facilities, self.Pfees, self.DF, self.tender_down)
        rawData, areabyCadastralcode, distributionRatio, buildingCost, dwellingCost = escenario_1_exe.PEMcalculation(ref_cat=self.ref_cat_analysis)
                  
        buildingCost, dwellingCost, dwellings_fees, buildingGrants = super().executeCommonCode(self.ref_cat_analysis, buildingCost, dwellingCost, distributionRatio)
         
    

        return buildingCost, dwellingCost, dwellings_fees, buildingGrants


class calculoCuota_Palma(currencySource): 
    """
    Para la programación de ARV se propone realizar la programación:
        1) Leer el excel "AllCombinedResults" como en csvTRNSYS
        2) Identificar las columnas donde salen los materiales utilizados -> 1 por simulación
        3) Cruzar esos valores con otro excel o base de datos SQL donde esté la relación de los nombres de las columnas del punto (2))
           y los precios por m2.
    De esta forma para añadir nuevas opciones solo habría que modificar los excels externos, no el código en Python. Los excels externos 
    ponerlos siempre en la carpeta ..\resources\data\.. para que el filePath siempre sea el mismo.
    """
    def __init__(self, windows, common_facilities, facilities, Pfees, DF, tender_down, ref_cat_analysis, deltaEPNR, materials, areabyCadastralcode,distributionRatio, ref_use, config ):
        super().__init__(windows, common_facilities, facilities, Pfees, DF, tender_down, ref_cat_analysis, deltaEPNR)
        self.materials = materials
        self.areabyCadastralcode = areabyCadastralcode
        self.distributionRatio = distributionRatio
        self.ref_use = ref_use
        self.config = config
    def calculo_Cuota(self):  
        # Execution Cost      
        escenario_1_exe = executionCost.detailedPEMcalculationPalma(self.windows, self.common_facilities, self.facilities, self.Pfees, self.DF, self.tender_down)
        rawData, areabyCadastralcode, distributionRatio, buildingCost, dwellingCost = escenario_1_exe.PEMcalculation(refcat=self.ref_cat_analysis, materials = self.materials, config = self.config,areabyCadastralcode= self.areabyCadastralcode, distributionRatio = self.distributionRatio, ref_use = self.ref_use)

        buildingCost, dwellingCost, dwellings_fees, building_grants   = super().executeCommonCode(self.ref_cat_analysis, buildingCost, dwellingCost, distributionRatio)
              
        return buildingCost, dwellingCost, dwellings_fees, building_grants
              

        
class calculationCuote :
    def __init__(self, calculation : currencySource):
        self.calculation = calculation    
    def start(self):    
        return self.calculation.calculo_Cuota()

if __name__ == '__main__':
    from interactor import getSurfaces
    from repository import CMH
    # from interactor import replace
    outputType = calculoCuota_CMH()
    transformation = calculationCuote(outputType)
    CMH_data, areabyCadastralcode, distributionRatio, costDwelling_const, costDwelling_inst, costBuilding_PEM, costBuilding_total = transformation.start()