# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""

# Abstract method import

from abc import ABC, abstractmethod


# Abstract class



class grantEstimation_config(ABC):
    def __init__(self, perc_grant, grant_scope, grant_limit):
        self.perc_grant = perc_grant/100
        self.grant_scope = grant_scope
        self.grant_limit = grant_limit
    @abstractmethod
    def grantCalculation(self):
        pass

# Calculation of the investment with CMH data as a cost input
class grantEstimation(grantEstimation_config):
    """
    Parameters:
        
        perc_grant (float -> %) -- Percentage of subsidy on the eligible cost      
        grant_scope (int -> 1 or 2) -- 1 with dwelling grant limitation or 2 with grant building limitation
        grant_limit (float) -- Grant limitation according to grant_scope       
    """
    def __init__(self, perc_grant, grant_scope, grant_limit):
        super().__init__(perc_grant, grant_scope, grant_limit)
    def grantCalculation(self, eligible_cost, n_dwellings):
        
        """
        Inputs:            
            eligible_cost (float) -- Eligible cost      
            n_dwellings (int) -- number of dwellings
      
        """
        limitation = False
        if str(self.grant_scope) == "1":            
            grant_output = eligible_cost/n_dwellings*self.perc_grant
            if grant_output >= self.grant_limit:
                grant_output = self.grant_limit
                limitation = True
            else:
                grant_output = grant_output * n_dwellings    
            cost_without_grant = eligible_cost - grant_output    
            
        if str(self.grant_scope) == "2":
            grant_output = eligible_cost*self.perc_grant
            if grant_output >= self.grant_limit:
                grant_output = self.grant_limit
                limitation = True
            cost_without_grant = eligible_cost - grant_output        
            
        return grant_output, cost_without_grant, limitation 

    
    
    
if __name__ == '__main__':
    patronat_excel = grantEstimation(perc_grant = 35, grant_scope = 1, grant_limit = 5000)
    grant_output, cost_without_grant, limitation = patronat_excel.grantCalculation(eligible_cost = 2202774,n_dwellings = 350)


    