# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""

import numpy_financial as npf

# Abstract method import

from abc import ABC, abstractmethod


# Abstract class



class economicBalance_config(ABC):
    def __init__(self, phases_definition, fee_start, grant_start, loan_start, public_payment, financial_cost, defaulter_risk, UT5_payment, VAT_material, VAT_project):
        self.phases_definition = phases_definition
        self.fee_start = fee_start
        self.grant_start = grant_start 
        self.loan_start = loan_start
        self.public_payment = public_payment
        self.VAT_material = VAT_material
        self.VAT_project = VAT_project
        self.UT5_payment = UT5_payment
        self.financial_cost = financial_cost
        self.defaulter_risk = defaulter_risk
    @abstractmethod
    def cashflow_calculation(self):
        pass


class economic_Balance(economicBalance_config):
    """
    Parameters:            
        phases_definition (dict -> str : int) -- duration months -- Pre-initial phase / Initial phase / Project phase / Execution phase           
        fee_start (int) -- month start
        grant_start (dict -> int : %) -- month start : quantity
        loan_start (dict) -- month of funding + payment start + loan 
        public_payment (float) -- public € payment
        financial_cost (bool) -- Include financial cost in fees
        defaulter_risk (bool) -- Include defaulters risk in fees
        UT5_payment (bool) -- True if public sector will pay UT5 users
        VAT_material (float) -- VAT material
        VAT_project (float) -- VAT project
     """    
    def __init__(self, phases_definition, fee_start, grant_start, loan_start, public_payment, financial_cost, defaulter_risk, UT5_payment, VAT_material=0.1, VAT_project=0.21):
        super().__init__(phases_definition, fee_start, grant_start, loan_start, public_payment, financial_cost, defaulter_risk, UT5_payment, VAT_material, VAT_project)
    def cashflow_calculation(self, buildingCost, dwellingCost, dict_owners_output ,private_works_noVAT, private_works_VAT, monthly_payment, years_amortization, building_grants, interest_rate_UT2, interest_rate_UT3, over_head, benefit_expected, distribution_ratio):               
        """
        Inputs: 
            buildingCost (dict) -- gCost + iBen + Pfees + DF + n_dwellings
            dwellingCost (dict) -- PEM cost dwelling level
            dict_owners_output (dict) -- Dwellings with userType distribution
            private_works_noVAT (dict) -- Retrofitting Agent costs without VAT
            private_works_VAT (dict) -- Retrofitting Agent costs with VAT 
            monthly_payment (int) -- Monthly loan payment
            years_amortization (int) -- Years return loan
            building_grants (dict{dict}) -- Building grands
            interest_rate_UT2 (%) -- Interest rate UT2 user 
            interest_rate_UT3 (%) -- Interest rate UT3 user          
            overhead (%) -- Company general costs
            benefic expected (%) -- benfit expected by the company
            distribution_ratio (dict - %) -- distribution ratio
        """
        scope_months = self.fee_start + 180   # 180 months UT3 180 quotes   
        economic_balance_detailed = {}
        economic_balance_summary= {} 
        economic_balance_VAT= {} 
        cash_flow = {}
        dwellings_fees = {}
        # Calculation the cost distribution

        monthly_pre_initial = round(private_works_noVAT['Pre-initial']/self.phases_definition['Pre-initial'])
        monthly_initial = round(private_works_noVAT['Initial']/self.phases_definition['Initial'])
        monthly_project = round(private_works_noVAT['Project']/self.phases_definition['Project'])
        monthly_execution = round(private_works_noVAT['Execution']/self.phases_definition['Execution'])
        monthly_financial= round(private_works_noVAT['Financial support']/scope_months)

    
        
        # monthly_pre_initial_VAT = (private_works_VAT['Pre-initial']-private_works_noVAT['Pre-initial'])/self.phases_definition['Pre-initial']
        # monthly_initial_VAT = (private_works_VAT['Initial']-private_works_noVAT['Initial'])/self.phases_definition['Initial']
        # monthly_project_VAT = (private_works_VAT['Project']-private_works_noVAT['Project'])/self.phases_definition['Project']
        # monthly_execution_VAT = (private_works_VAT['Execution']-private_works_noVAT['Execution'])/self.phases_definition['Execution']
        # monthly_financial_VAT = (private_works_VAT['Financial support']-private_works_noVAT['Financial support'])/scope_months       
        
        # Grant distribution
        global_grant = sum(list(building_grants['Material'].values()))+building_grants['Operational']+sum(list(building_grants['Project'].values()))
        for i in self.grant_start:
            self.grant_start[i] = round(self.grant_start[i]/100*global_grant)
        
        # Cash_flow outputs
        outputs_detailed = ['Op_Pre-initial', 'Op_Initial', 'Op_Project', 'Op_Execution', 'Op_Financial','Pfees_prev','Pfees_project', 'Pfees_DF_iBen_gCost', 'Ex_PEC', 'Pay_UT1', 'Pay_UT2', 'Pay_UT3', 'Pay_UT4', 'Pay_UT5', 'Prev_grant', 'Inter_grant', 'Final_grant', 'public_payment', 'Get_loan', 'Loan_payment']
        outputs_summary = ['Incomes', 'Costs', 'EBIDTA']
        outputs_VAT = ['VAT_project', 'VAT_exe', 'VAT_private', 'VAT_balance', 'VAT_3month', 'VAT_acc', 'VAT_payment']
        outputs_cashflow = ['Cash_flow', 'Acc. Cash_flow']
        
        for i in outputs_detailed:
            economic_balance_detailed.setdefault(i,[])
        for i in outputs_summary:
            economic_balance_summary.setdefault(i,[])
        for i in outputs_VAT:
            economic_balance_VAT.setdefault(i,[])            
        for i in outputs_cashflow:
            cash_flow.setdefault(i,[])    
            
            
        # def fee_calculation(building_cost, operational_cost, financial_cost,  grant_available, financial_cost, defaulter_risk:
        #     fee = buildCost_total - grant_available['']                
                
        #     return fee
            
        def EBIDTA_balance(values_list, economic_balance_summary, monthly_count):
            
            economic_balance_summary['Incomes'].append(0)
            economic_balance_summary['Costs'].append(0)
            economic_balance_summary['EBIDTA'].append(0)
            
            for j in values_list:
                if j > 0:
                    economic_balance_summary['Incomes'][monthly_count-1] = economic_balance_summary['Incomes'][monthly_count-1] + j
                if j < 0:
                    economic_balance_summary['Costs'][monthly_count-1] = economic_balance_summary['Costs'][monthly_count-1] + j
                economic_balance_summary['EBIDTA'][monthly_count-1] = economic_balance_summary['Incomes'][monthly_count-1]+economic_balance_summary['Costs'][monthly_count-1]

            return economic_balance_summary
        
        
        def VAT_balance(self, economic_balance_VAT, economic_balance_detailed, monthly_count, VAT_users):
            
            economic_balance_VAT['VAT_project'].append((economic_balance_detailed['Pfees_prev'][monthly_count-1]+ economic_balance_detailed['Pfees_project'][monthly_count-1] + economic_balance_detailed['Pfees_DF_iBen_gCost'][monthly_count-1])*self.VAT_project)
            economic_balance_VAT['VAT_exe'].append(round(economic_balance_detailed['Ex_PEC'][monthly_count-1]*self.VAT_material))
            economic_balance_VAT['VAT_private'].append((economic_balance_detailed['Pay_UT1'][monthly_count-1]+economic_balance_detailed['Pay_UT2'][monthly_count-1]+economic_balance_detailed['Pay_UT3'][monthly_count-1]+economic_balance_detailed['Pay_UT4'][monthly_count-1]+economic_balance_detailed['Pay_UT5'][monthly_count-1])*VAT_users) 
            
            #Public payment
            
            if monthly_count == self.phases_definition['Pre-initial']+self.phases_definition['Initial']+1:
                economic_balance_VAT['VAT_balance'].append(economic_balance_VAT['VAT_project'][monthly_count-1]+economic_balance_VAT['VAT_exe'][monthly_count-1]+economic_balance_VAT['VAT_private'][monthly_count-1]+self.public_payment*self.VAT_project) 
            else:    
                economic_balance_VAT['VAT_balance'].append(economic_balance_VAT['VAT_project'][monthly_count-1]+economic_balance_VAT['VAT_exe'][monthly_count-1]+economic_balance_VAT['VAT_private'][monthly_count-1]) 
            
            if monthly_count % 3 == 0:
                economic_balance_VAT['VAT_3month'].append(economic_balance_VAT['VAT_balance'][monthly_count-3]+economic_balance_VAT['VAT_balance'][monthly_count-2]+economic_balance_VAT['VAT_balance'][monthly_count-1])
            else:
                economic_balance_VAT['VAT_3month'].append(0)  
            if monthly_count % 3 == 0: 
                               
                economic_balance_VAT['VAT_acc'].append(economic_balance_VAT['VAT_acc'][monthly_count-2]+economic_balance_VAT['VAT_balance'][monthly_count-1])
                
                if economic_balance_VAT['VAT_acc'][monthly_count-1] > 0:                   
                    economic_balance_VAT['VAT_payment'].append(-economic_balance_VAT['VAT_acc'][monthly_count-1])
                    
                elif economic_balance_VAT['VAT_acc'][monthly_count-1] < 0 and monthly_count % 12 == 0:
                    economic_balance_VAT['VAT_payment'].append(-economic_balance_VAT['VAT_acc'][monthly_count-1])
                else:
                    economic_balance_VAT['VAT_payment'].append(0)
            else:
                economic_balance_VAT['VAT_acc'].append(economic_balance_VAT['VAT_acc'][monthly_count-2]+economic_balance_VAT['VAT_balance'][monthly_count-1]+economic_balance_VAT['VAT_payment'][monthly_count-2])
                economic_balance_VAT['VAT_payment'].append(0)
                
            return economic_balance_VAT
            
    
        def cashflow_balance(cash_flow, economic_balance_summary, economic_balance_VAT, monthly_count):   

            cash_flow['Cash_flow'].append(economic_balance_summary['EBIDTA'][monthly_count-1]+economic_balance_VAT['VAT_balance'][monthly_count-1]+economic_balance_VAT['VAT_payment'][monthly_count-1])              
            
            if monthly_count == 1:
                cash_flow['Acc. Cash_flow'].append(cash_flow['Cash_flow'][monthly_count-1])  
            else:                    
                cash_flow['Acc. Cash_flow'].append(cash_flow['Acc. Cash_flow'][monthly_count-2]+cash_flow['Cash_flow'][monthly_count-1])
            
            return cash_flow

        # User VAT
        global_PEC = 0
        global_proj = 0
        global_grant_mat = 0
        global_grant_exe = 0
        for i in buildingCost:
            global_PEC = global_PEC + buildingCost[i]['building_total_PEC_noVAT']
            global_proj = global_proj + buildingCost[i]['Pfees'] + buildingCost[i]['DF']
            global_grant_mat = global_grant_mat + building_grants['Material'][i]            
            global_grant_proj = global_grant_exe + building_grants['Project'][i]
            
        global_grant_ope = building_grants['Operational']   
        global_ope =  (private_works_noVAT['Total_costs']-private_works_noVAT['Financial support']) - global_grant_ope
        global_exe = global_PEC - global_grant_exe
        global_project = global_proj - global_grant_proj
        global_total = global_ope + global_exe + global_project
        global_VAT_project = global_project*self.VAT_project
        global_VAT_ope = global_ope*self.VAT_project
        global_VAT_exe = global_exe*self.VAT_material
        global_VAT_total = global_VAT_project+global_VAT_ope+global_VAT_exe
        VAT_users = (global_VAT_total)/(global_total)    
        total_dw = 0
        for i in buildingCost:
            total_dw = total_dw + buildingCost[i]['nDwellings']
            
        global_ope_dw = private_works_noVAT['Total_costs']/total_dw
        global_proj_dw = global_proj/total_dw
        global_financial_dw = ((monthly_payment*years_amortization*12)-self.loan_start['loan'])/total_dw
        count_def = 0        
        for i in dict_owners_output:
            for j in dict_owners_output[i]:
                if dict_owners_output[i][j]['userType'] == 'UT5':
                    count_def = count_def + 1           
        perct_default = count_def/total_dw
        global_df_dw = (global_PEC*perct_default)/total_dw
        global_grant_ope_dw = building_grants['Operational']/total_dw
        
        def fee_calc(buildingCost, operationalCost, financialCost, defaulterCost, grantMaterial, grantOp, grantProj, financial_cost, defaulter_risk, overhead, benefit_expected):
            operationalCost_corrected = operationalCost + operationalCost*overhead/100 + operationalCost*benefit_expected/100
            base_fee = (buildingCost + operationalCost_corrected) - grantMaterial - grantProj - grantOp          
            if financial_cost == True:
                base_fee = base_fee + financialCost
            if defaulter_risk == True:
                base_fee = base_fee + defaulterCost
            return base_fee
            
        #%% Monthly fees calculation
        
        for i in distribution_ratio:
            dwellings_fees.setdefault(str(i),{})
            cuota_general = fee_calc(buildingCost[i]['building_total_noVAT'],global_ope_dw*buildingCost[i]['nDwellings'],global_financial_dw*buildingCost[i]['nDwellings'],global_df_dw*buildingCost[i]['nDwellings'],building_grants['Material'][i],global_grant_ope_dw*buildingCost[i]['nDwellings'],building_grants['Project'][i],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
            coef_escaleras = sum(list(distribution_ratio[i].values()))/100
            for j in distribution_ratio[i]:
                dwellings_fees[i].setdefault(str(j),[])            
                cuota_general_UT2 = npf.pmt(rate = (interest_rate_UT2/100)/12, nper = 12*10, pv = -cuota_general*(distribution_ratio[i][j]/(coef_escaleras*100)))
                cuota_general_UT3 = npf.pmt(rate = (interest_rate_UT3/100)/12, nper = 12*15, pv = -cuota_general*(distribution_ratio[i][j]/(coef_escaleras*100)))
                dwellings_fees[i][j].append(round(min(cuota_general_UT2 + cuota_general_UT2*VAT_users,cuota_general_UT3 + cuota_general_UT3*VAT_users)))
                dwellings_fees[i][j].append(round(max(cuota_general_UT2 + cuota_general_UT2*VAT_users,cuota_general_UT3 + cuota_general_UT3*VAT_users)))          

        #%% Pre-initial Phase calculation
        
        monthly_count = 1
        for i in range(0,self.phases_definition['Pre-initial']):
            values_list = []
            for j in outputs_detailed:
                if j == 'Op_Financial':
                    economic_balance_detailed[j].append(-monthly_financial)
                    values_list.append(-monthly_financial)
                elif j =='Op_Pre-initial':
                    economic_balance_detailed[j].append(-monthly_pre_initial)
                    values_list.append(-monthly_pre_initial)                    
                else:
                    economic_balance_detailed[j].append(0)
                    values_list.append(0)
                    
            economic_balance_summary = EBIDTA_balance(values_list, economic_balance_summary, monthly_count)
           
            for j in outputs_VAT:                  
                economic_balance_VAT[j].append(0)   
                
            cash_flow = cashflow_balance(cash_flow, economic_balance_summary, economic_balance_VAT, monthly_count) 
            
            monthly_count = monthly_count + 1  
            
        #%% Initial Phase calculation
        

        for i in range(0,self.phases_definition['Initial']):
            values_list = []
            for j in outputs_detailed:
                if j == 'Op_Financial':
                    economic_balance_detailed[j].append(-monthly_financial)
                    values_list.append(-monthly_financial)                    
                elif j == 'Op_Initial':
                    economic_balance_detailed[j].append(-monthly_initial)
                    values_list.append(-monthly_initial)     
                else:
                    economic_balance_detailed[j].append(0)
                    values_list.append(0)           
                    
  

       
            economic_balance_summary = EBIDTA_balance(values_list, economic_balance_summary, monthly_count)
           
            for j in outputs_VAT:                  
                economic_balance_VAT[j].append(0)   
                
            cash_flow = cashflow_balance(cash_flow, economic_balance_summary, economic_balance_VAT, monthly_count) 
            
            monthly_count = monthly_count + 1              
            
        #%% Project Phase calculation
        

        
        loan_control = 0
        fee_control_UT2 = 0
        fee_control_UT3 = 0
        quotes_UT2 = 0
        quotes_UT3 = 0
        quotes_loan = 0
        

        for i in range(0,self.phases_definition['Project']): 
            if self.fee_start == monthly_count:
                fee_control_UT2 = 1
                fee_control_UT3 = 1
                
            if self.loan_start['start_payment'] == monthly_count: 
                loan_control = 1
                
            values_list = []
            for j in outputs_detailed:
                if j == 'Op_Financial':
                    economic_balance_detailed[j].append(-monthly_financial)
                    values_list.append(-monthly_financial)
                    
                elif j == 'Op_Project':
                    economic_balance_detailed[j].append(-monthly_project)
                    values_list.append(-monthly_project)      
                               
                elif j == 'Pfees_prev' and monthly_count == self.phases_definition['Pre-initial']+self.phases_definition['Initial']+2:
                    total_cost = 0
                    for k in buildingCost:
                        total_cost = round(total_cost + buildingCost[k]['Pfees'])
                    economic_balance_detailed[j].append(-total_cost*0.2 + -total_cost*0.2*self.VAT_project)
                    values_list.append(-total_cost*0.2 + -total_cost*0.2*self.VAT_project) 
                elif j == 'public_payment' and monthly_count == self.phases_definition['Pre-initial']+self.phases_definition['Initial']+1:                    
                    economic_balance_detailed[j].append(self.public_payment)
                    values_list.append(self.public_payment)                    
                elif j == 'Pay_UT1' and monthly_count == self.phases_definition['Pre-initial']+self.phases_definition['Initial']+2:
                    total_cost = 0
                    for k in dict_owners_output:     
                        cuotas_UT1 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT1':
                                cuota = npf.pmt(rate = 0, nper = 2, pv = -cuotas_UT1/buildingCost[k]['nDwellings'])

                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)                                    

                elif j == 'Pay_UT2' and fee_control_UT2 == 1 and quotes_UT2 <= 120:
                    total_cost = 0
                    quotes_UT2 = quotes_UT2 + 1
                    for k in dict_owners_output:
                        cuotas_UT2 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT2':
                                cuota = npf.pmt(rate = (interest_rate_UT2/100)/12, nper = 12*10, pv = -cuotas_UT2/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)    
                          
                elif j == 'Pay_UT3' and fee_control_UT3 == 1 and quotes_UT3 <= 180:
                    total_cost = 0
                    quotes_UT3 = quotes_UT3 + 1
                    for k in dict_owners_output:
                        cuotas_UT3 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT3':
                                cuota = npf.pmt(rate = (interest_rate_UT3/100)/12, nper = 12*15, pv = -cuotas_UT3/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)  

                elif j == 'Get_loan' and monthly_count == self.loan_start['get_loan']:                    
                    economic_balance_detailed[j].append(self.loan_start['loan'])
                    values_list.append(self.loan_start['loan'])
                    
                elif j == 'Loan_payment' and loan_control == 1 and quotes_loan < years_amortization*12 :                  
                    economic_balance_detailed[j].append(-monthly_payment)
                    values_list.append(-monthly_payment)
                    quotes_loan = quotes_loan + 1

                        
                    
 
                elif j == 'Prev_grant' and monthly_count == list(self.grant_start.keys())[0]:                    
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[0]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1]) 
                elif j == 'Inter_grant' and monthly_count == list(self.grant_start.keys())[1]:
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[1]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1])
                elif j == 'Final_grant' and monthly_count == list(self.grant_start.keys())[2]:
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[2]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1])                                     
                else:
                    economic_balance_detailed[j].append(0)
                    values_list.append(0)  
                    
            economic_balance_summary = EBIDTA_balance(values_list, economic_balance_summary, monthly_count)          
            economic_balance_VAT = VAT_balance(self, economic_balance_VAT, economic_balance_detailed, monthly_count, VAT_users)
            cash_flow = cashflow_balance(cash_flow, economic_balance_summary, economic_balance_VAT, monthly_count)            

            monthly_count = monthly_count + 1
                       
        #%% Execution Phase calculation
        
        monthly_PEC = round(global_PEC/self.phases_definition['Execution'])
        for i in range(0,self.phases_definition['Execution']): 
            if self.fee_start == monthly_count:
                fee_control_UT2 = 1
                fee_control_UT3 = 1
                
            if self.loan_start['start_payment'] == monthly_count: 
                loan_control = 1                
            values_list = []
            for j in outputs_detailed:
                if j == 'Op_Financial':
                    economic_balance_detailed[j].append(-monthly_financial)
                    values_list.append(-monthly_financial)
                    
                elif j == 'Op_Execution':
                    economic_balance_detailed[j].append(-monthly_execution)
                    values_list.append(-monthly_execution)
                    
                elif j == 'Ex_PEC':
                    economic_balance_detailed[j].append(-monthly_PEC + -monthly_PEC*self.VAT_material)
                    values_list.append(-monthly_PEC + -monthly_PEC*self.VAT_material) 
                               
                elif j == 'Pfees_project' and monthly_count == self.phases_definition['Pre-initial']+self.phases_definition['Initial']+self.phases_definition['Project']+1:
                    total_cost = 0
                    for k in buildingCost:
                        total_cost = round(total_cost + buildingCost[k]['Pfees'])
                    economic_balance_detailed[j].append(round(-total_cost*0.8 + -total_cost*0.8*self.VAT_project))
                    values_list.append(round(-total_cost*0.8 + -total_cost*0.8*self.VAT_project))
                                       
                elif j == 'Pfees_DF_iBen_gCost' and monthly_count == self.phases_definition['Pre-initial']+self.phases_definition['Initial']+self.phases_definition['Project']+self.phases_definition['Execution']/2:
                    total_cost = 0
                    for k in buildingCost:
                        total_cost = round(total_cost + buildingCost[k]['DF']+ buildingCost[k]['iBen']+ buildingCost[k]['gCost'])
                    economic_balance_detailed[j].append(round(-total_cost*0.5 + -total_cost*0.5*self.VAT_project))
                    values_list.append(round(-total_cost*0.35 + -total_cost*0.35*self.VAT_project)) 
                                      
                elif j == 'Pfees_DF_iBen_gCost' and monthly_count == self.phases_definition['Pre-initial']+self.phases_definition['Initial']+self.phases_definition['Project']+self.phases_definition['Execution']:
                    total_cost = 0
                    for k in buildingCost:
                        total_cost = round(total_cost + buildingCost[k]['DF']+ buildingCost[k]['iBen']+ buildingCost[k]['gCost'])
                    economic_balance_detailed[j].append(round(-total_cost*0.5 + -total_cost*0.5*self.VAT_project))
                    values_list.append(round(-total_cost*0.65 + -total_cost*0.65*self.VAT_project))                                     
                                        

                elif j == 'Pay_UT2' and fee_control_UT2 == 1 and quotes_UT2 <= 120:
                    quotes_UT2 = quotes_UT2 + 1
                    total_cost = 0
                    for k in dict_owners_output:
                        cuotas_UT2 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT2':
                                cuota = npf.pmt(rate = (interest_rate_UT2/100)/12, nper = 12*10, pv = -cuotas_UT2/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)    
                          
                elif j == 'Pay_UT3' and fee_control_UT3 == 1 and quotes_UT3 <= 180:
                    quotes_UT3 = quotes_UT3 + 1
                    total_cost = 0
                    for k in dict_owners_output:
                        cuotas_UT3 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT3':
                                cuota = npf.pmt(rate = (interest_rate_UT3/100)/12, nper = 12*15, pv = -cuotas_UT3/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)
                    
                elif j == 'Pay_UT4' and monthly_count == self.phases_definition['Pre-initial']+self.phases_definition['Initial']+self.phases_definition['Project']+3:
                    total_cost = 0
                    for k in dict_owners_output:
                        cuotas_UT4 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT4':
                                cuota = npf.pmt(rate = 0, nper = 2, pv = -cuotas_UT4/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)         
                    
                elif j == 'Get_loan' and monthly_count == self.loan_start['get_loan']:                    
                    economic_balance_detailed[j].append(self.loan_start['loan'])
                    values_list.append(self.loan_start['loan'])
                    
                elif j == 'Loan_payment' and loan_control == 1 and quotes_loan < years_amortization*12 :                  
                    economic_balance_detailed[j].append(-monthly_payment)
                    values_list.append(-monthly_payment)
                    quotes_loan = quotes_loan + 1
                    
                elif j == 'Prev_grant' and monthly_count == list(self.grant_start.keys())[0]:
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[0]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1]) 
                elif j == 'Inter_grant' and monthly_count == list(self.grant_start.keys())[1]:
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[1]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1])
                elif j == 'Final_grant' and monthly_count == list(self.grant_start.keys())[2]:
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[2]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1])                                                      
                else:
                    economic_balance_detailed[j].append(0)
                    values_list.append(0)  
                    
            economic_balance_summary = EBIDTA_balance(values_list, economic_balance_summary, monthly_count)          
            economic_balance_VAT = VAT_balance(self, economic_balance_VAT, economic_balance_detailed, monthly_count, VAT_users)
            cash_flow = cashflow_balance(cash_flow, economic_balance_summary, economic_balance_VAT, monthly_count)            
            monthly_count = monthly_count + 1             

        
        
        #%% Financial support Phase calculation
        
        start_financing_phase = sum(list(self.phases_definition.values()))
        for i in range(start_financing_phase,scope_months): 
            if self.fee_start == monthly_count:
                fee_control_UT2 = 1
                fee_control_UT3 = 1
                
            if self.loan_start['start_payment'] == monthly_count: 
                loan_control = 1           
                 
            values_list = []
            for j in outputs_detailed:
                if j == 'Op_Financial':
                    economic_balance_detailed[j].append(-monthly_financial)
                    values_list.append(-monthly_financial)                                                        
    
                elif j == 'Pay_UT1' and monthly_count == start_financing_phase+1:
                    total_cost = 0
                    for k in dict_owners_output:
                        cuotas_UT1 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT1':
                                cuota = npf.pmt(rate = 0, nper = 2, pv = -cuotas_UT1/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)                                    

                elif j == 'Pay_UT2' and fee_control_UT2 == 1 and quotes_UT2 <= 120:
                    quotes_UT2 = quotes_UT2 + 1
                    total_cost = 0
                    for k in dict_owners_output:
                        cuotas_UT2 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT2':
                                cuota = npf.pmt(rate = (interest_rate_UT2/100)/12, nper = 12*10, pv = -cuotas_UT2/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)    
                          
                elif j == 'Pay_UT3' and fee_control_UT3 == 1 and quotes_UT3 <= 180:
                    quotes_UT3 = quotes_UT3 + 1
                    total_cost = 0
                    for k in dict_owners_output:
                        cuotas_UT3 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT3':
                                cuota = npf.pmt(rate = (interest_rate_UT3/100)/12, nper = 12*15, pv = -cuotas_UT3/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)   

                elif j == 'Pay_UT4' and monthly_count == start_financing_phase+1:
                    total_cost = 0
                    for k in dict_owners_output:
                        cuotas_UT4 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT4':
                                cuota = npf.pmt(rate = 0, nper = 2, pv = -cuotas_UT4/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)  

                elif j == 'Pay_UT5' and monthly_count == start_financing_phase+1 and self.UT5_payment == True:
                    total_cost = 0
                    for k in dict_owners_output:
                        cuotas_UT5 = fee_calc(buildingCost[k]['building_total_noVAT'],global_ope_dw*buildingCost[k]['nDwellings'],global_financial_dw*buildingCost[k]['nDwellings'],global_df_dw*buildingCost[k]['nDwellings'],building_grants['Material'][k],global_grant_ope_dw*buildingCost[k]['nDwellings'],building_grants['Project'][k],self.financial_cost,self.defaulter_risk,over_head, benefit_expected)
                        for t in dict_owners_output[k]:
                            if dict_owners_output[k][t]['userType'] == 'UT5':
                                cuota = npf.pmt(rate = 0, nper = 1, pv = -cuotas_UT5/buildingCost[k]['nDwellings'])
                                total_cost = round(total_cost + cuota + cuota*VAT_users)
                    economic_balance_detailed[j].append(total_cost)
                    values_list.append(total_cost)  
                    
                elif j == 'Get_loan' and monthly_count == self.loan_start['get_loan']:                    
                    economic_balance_detailed[j].append(self.loan_start['loan'])
                    values_list.append(self.loan_start['loan'])
                    
                elif j == 'Loan_payment' and loan_control == 1 and quotes_loan < years_amortization*12 :                  
                    economic_balance_detailed[j].append(-monthly_payment)
                    values_list.append(-monthly_payment)
                    quotes_loan = quotes_loan + 1
                    
                elif j == 'Prev_grant' and monthly_count == list(self.grant_start.keys())[0]:
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[0]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1]) 
                elif j == 'Inter_grant' and monthly_count == list(self.grant_start.keys())[1]:
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[1]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1])
                elif j == 'Final_grant' and monthly_count == list(self.grant_start.keys())[2]:
                    economic_balance_detailed[j].append(self.grant_start[list(self.grant_start.keys())[2]])
                    values_list.append(economic_balance_detailed[j][monthly_count-1])                                                      
                else:
                    economic_balance_detailed[j].append(0)
                    values_list.append(0)  
                    
            economic_balance_summary = EBIDTA_balance(values_list, economic_balance_summary, monthly_count)          
            economic_balance_VAT = VAT_balance(self, economic_balance_VAT, economic_balance_detailed, monthly_count, VAT_users)
            cash_flow = cashflow_balance(cash_flow, economic_balance_summary, economic_balance_VAT, monthly_count)            
            monthly_count = monthly_count + 1             
        return economic_balance_detailed, economic_balance_summary, economic_balance_VAT, cash_flow, dwellings_fees 
  

# if __name__ == '__main__': 
    # economic_scenario = economic_Balance({'Pre-initial' : 3, 'Initial' : 3, 'Project' : 6, 'Execution' : 12}, fee_start = 7, grant_start = {14 : 30, 20 : 20, 25 : 50 }, financial_start = 13)
    # cash_flow = economic_scenario.cashflow_calculation(buildingCost, dwellingCost, dict_owners_output, private_works_noVAT, private_works_VAT, monthly_capital, monthly_interest, building_grants)


    