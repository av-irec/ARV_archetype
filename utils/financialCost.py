# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""

# Abstract method import

from abc import ABC, abstractmethod


# Abstract class



class financialCost_config(ABC):
    def __init__(self, financialNeeds):
        self.financialNeeds = financialNeeds

    @abstractmethod
    def financialCalculation(self):
        pass


# Calculation of the investment with CMH data as a cost input
class financialCost(financialCost_config):
    """
    Parameters:
        
        financialNeeds (float) -- Capital requiered to do the retrofitting process       
     
    """
    def __init__(self, financialNeeds):
        super().__init__(financialNeeds)
    def financialCalculation(self, yearly_TAE, years):
        """
        Inputs:
            
            yearly_TAE (float -> %) -- Interest rate  
            years (int) -- years of amortisation
      
        """
        import numpy_financial as npf        
        monthly_payment = npf.pmt(rate = (yearly_TAE/100)/12, nper = 12*years, pv = -self.financialNeeds)
        monthly_interest = {}
        monthly_capital = {}
        financial_cost = 0
        capital_amortization = {}
        interest_yearly = {}
        for i in range(1,years+1):
            monthly_interest.setdefault("Year " + str(i),[])
            monthly_capital.setdefault("Year " + str(i),[])
            capital_amortization.setdefault("Year " + str(i),0)
            interest_yearly.setdefault("Year " + str(i),0)
            for j in range(1,13):
                monthly_interest["Year " + str(i)].append(npf.ipmt((yearly_TAE/100)/12, 12*(i-1)+j, years*12, -self.financialNeeds))
                monthly_capital["Year " + str(i)].append(npf.ppmt((yearly_TAE/100)/12, 12*(i-1)+j, years*12, -self.financialNeeds))
                financial_cost = financial_cost + monthly_interest["Year " + str(i)][j-1]
            interest_yearly["Year " + str(i)] = interest_yearly["Year " + str(i)] + sum(monthly_interest["Year " + str(i)])      
            capital_amortization["Year " + str(i)] = capital_amortization["Year " + str(i)] + sum(monthly_capital["Year " + str(i)])
 
                
        
        
        
 
        return financial_cost, monthly_payment, monthly_interest, monthly_capital, capital_amortization, interest_yearly

    
    
    
if __name__ == '__main__':
    escenario_1 = financialCost(1400000)
    financial_cost, monthly_payment, monthly_interest, monthly_capital, capital_amortization, interest_yearly = escenario_1.financialCalculation(5, 5)

    