# -*- coding: utf-8 -*-
"""

@author: srabadan
"""

from abc import ABC, abstractmethod


class currencyProject(ABC):
    @abstractmethod
    def calculation(self,pasiveInvestment,Investment_inst,Maintenance_inst,Replacement_inst,output_scenarios_Cons,PV_exp):
        pass              
      
    
        
class costARV(currencyProject): # 50 años
    def calculation(self,pasiveInvestment,Investment_inst,Maintenance_inst,Replacement_inst,output_scenarios_Cons,PV_exp):

        # COSTE GLOBAL ES INVESTMENT + ENERGY COST + MAINTENANCE + REPLACEMENT
        precio_ele = 0.2     # €/kWh
        precio_gas = 0.06    # €/kWh
        precio_butano = 0.13 # €/kWh
        tasa_inflacion = 2.5   # 3% anual
        print(pasiveInvestment)
        globalCost = {}
        for i in output_scenarios_Cons:
            globalCost.setdefault(i,{})
            for j in output_scenarios_Cons:
                pass
                
            
        


    
        
        
        
        
        
        
        t = 1
        return t

        

        
class calculo:
    def __init__(self, project : currencyProject,pasiveInvestment,Investment_inst,Maintenance_inst,Replacement_inst,output_scenarios_Cons,PV_exp):
        self.project = project
        self.pasiveInvestment = pasiveInvestment
        self.Investment_inst = Investment_inst
        self.Maintenance_inst = Maintenance_inst
        self.Replacement_inst = Replacement_inst
        self.output_scenarios_Cons = output_scenarios_Cons
        self.PV_exp = PV_exp
        
         
    def start(self):        
        return self.project.calculation(self.pasiveInvestment,self.Investment_inst,self.Maintenance_inst,self.Replacement_inst,self.output_scenarios_Cons,self.PV_exp)
    
    




# materials.setdefault(i[0],{'espesor':,'€_m2':0,'A1-3_CO2':0,'A4_CO2':0,'A5_CO2':0,'A1-3_EPNR':0,'A4_EPNR':0,'A5_EPNR':0}) # kgCO2/m2 - MJ/m2 (PENRT)
    
    
    
    
    
