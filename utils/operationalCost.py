# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""

# Abstract method import

from abc import ABC, abstractmethod


# Abstract class



class operationalCost_config(ABC):
    def __init__(self, fix_cost, variable_cost, n_dwellings, distribution_cost, distribution_cost_phases):
        self.fix_cost = fix_cost
        self.variable_cost = variable_cost
        self.n_dwellings = n_dwellings
        self.distribution_cost = distribution_cost
        self.distribution_cost_phases = distribution_cost_phases
    @abstractmethod
    def operationalCalculation(self):
        pass



class operationalCost(operationalCost_config):
    """
    Parameters:
        
        fix_cost (float) -- Fix cost of all retrofitting process        
        variable_cost (float) -- Variable cost related to number of dwellings  
        n_dwellings (int) -- Number of dwellings
        distribution_cost (dict) -- Dict with distibution cost between public sector and private company
        distribution_cost_phases (dict)  -- Dict with distibution cost according to 5 phases of the retroffiting process 
    """
    def __init__(self, fix_cost, variable_cost, n_dwellings, distribution_cost = {"Public": [1,0.3,0.3,0.2,0.2],"Private": [0,0.7,0.7,0.8,0.8]}, distribution_cost_phases = {"Pre-initial" : 0.1, "Initial" : 0.3, "Project" : 0.2, "Execution" : 0.15, "Financial support" : 0.25}):
        super().__init__(fix_cost, variable_cost, n_dwellings, distribution_cost, distribution_cost_phases)
    def operationalCalculation(self):
        public_works = {"Pre-initial" : 0, "Initial" : 0, "Project" : 0, "Execution" : 0, "Financial support" : 0}
        private_works_noVAT = {"Pre-initial" : 0, "Initial" : 0, "Project" : 0, "Execution" : 0, "Financial support" : 0}  
        private_works_VAT = {"Pre-initial" : 0, "Initial" : 0, "Project" : 0, "Execution" : 0, "Financial support" : 0} 
        total_operational_cost = self.fix_cost + self.variable_cost*self.n_dwellings
        count = -1
        VAT = 0.21
        for i in public_works:
            count = count + 1
            public_works[i] = public_works[i] + (self.distribution_cost['Public'][count])*total_operational_cost*self.distribution_cost_phases[i]
            private_works_noVAT[i] = private_works_noVAT[i] + self.distribution_cost['Private'][count]*total_operational_cost*self.distribution_cost_phases[i]
            private_works_VAT[i] = private_works_noVAT[i] + private_works_noVAT[i]*VAT

        public_works.setdefault("Total_costs",public_works['Pre-initial']+public_works['Initial']+public_works['Project']+public_works['Execution']+public_works['Financial support'])
        private_works_noVAT.setdefault("Total_costs",private_works_noVAT['Pre-initial']+private_works_noVAT['Initial']+private_works_noVAT['Project']+private_works_noVAT['Execution']+private_works_noVAT['Financial support'])
        private_works_VAT.setdefault("Total_costs",private_works_VAT['Pre-initial']+private_works_VAT['Initial']+private_works_VAT['Project']+private_works_VAT['Execution']+private_works_VAT['Financial support'])

        return public_works, private_works_noVAT, private_works_VAT

    
    
    
if __name__ == '__main__':
    distribution_config = {"Public": [1,0.3,0.3,0.2,0.2],"Private": [0,0.7,0.7,0.8,0.8]}
    escenario_1 = operationalCost(fix_cost = 75000, variable_cost = 385, n_dwellings = 350, distribution_cost = distribution_config)
    public_works, private_works_noVAT, private_works_VAT = escenario_1.operationalCalculation()

    