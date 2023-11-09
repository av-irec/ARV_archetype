# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""

# Abstract method import

from abc import ABC, abstractmethod

# Interactors

from interactors import getDataARV



# Abstract class



class userType_config(ABC):
    def __init__(self, UT_distribution):
        self.UT_distribution = UT_distribution
    @abstractmethod
    def userTypeInsert(self):
        pass


class propertyKnown(userType_config):
    """
    Parameters:
        
        UT_distribution (dict -> %) -- Percentage of distribution of User Types (5)      

        UT1 - 50/50
        UT2 - 10 years - 120 quotes
        UT3 - 15 years - 180 quotes
        UT4 - inscription in the register
        UT5 - defaulter
        
     """
    def __init__(self, UT_distribution):

        super().__init__(UT_distribution)
    def userTypeInsert(self, ref_cat = 'all'):
        """
        Inputs:            
            ref_cat (string) -- Write ref_cat to analyse specific building or 'all' to analyse all the buildings in the DDBB    
      
        """        
        import random
        from itertools import accumulate      
        


        sourceData = getDataARV.SQL_propertyARV()    # SQL_statments ARV
        get_data = getDataARV.getData_ARV(sourceData)   # Surfaces of each building
        # Reposity Outputs dicts -> 1) Area of each building (floor-roof-wall) with cadastral referece + 2) Partition ratio with cadastral referece
        dict_owners = get_data.start()
        
        
        legal_count = 0
        dwellings_scope = 0
        for i in dict_owners:
            if i in ref_cat or ref_cat == 'all':
                for j in dict_owners[i]:
                    dwellings_scope = dwellings_scope + 1
                    if dict_owners[i][j]['entity'] == 'legal':
                        legal_count = legal_count + 1
                    
        real_legal_perc = legal_count/dwellings_scope*100
        diff_UT1 =  self.UT_distribution['UT1'] - real_legal_perc
        sum_total = 0
        prop = {}
        for i in self.UT_distribution:
            if i == 'UT1':
                continue
            sum_total = sum_total + self.UT_distribution[i]
            prop[i] = self.UT_distribution[i]/(self.UT_distribution['UT2']+self.UT_distribution['UT3']+self.UT_distribution['UT4']+self.UT_distribution['UT5'])
        for i in self.UT_distribution:
            if i == 'UT1':
                continue            
            self.UT_distribution[i] = round(self.UT_distribution[i] + diff_UT1*prop[i])
            
        self.UT_distribution['UT1'] = round(real_legal_perc) 
        
        if sum(self.UT_distribution.values()) != 100:
            self.UT_distribution['UT2'] = self.UT_distribution['UT2'] + (100 - sum(self.UT_distribution.values()))
            

        
        dict_owners_output = {}
        dict_values_thresholds = list(accumulate(list(self.UT_distribution.values())))
        for i in dict_owners:
            if i in ref_cat or ref_cat == 'all':
                dict_owners_output.setdefault(i,{})
                for j in dict_owners[i]:
                    if dict_owners[i][j]['entity'] == 'legal':
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT1'})
                        continue
                    random_number = random.randint(self.UT_distribution['UT1'], 100)
                    if dict_values_thresholds[0] < random_number <= dict_values_thresholds[1]:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT2'})                        
                    elif dict_values_thresholds[1] < random_number <= dict_values_thresholds[2]:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT3'})    
                    elif dict_values_thresholds[2] < random_number <= dict_values_thresholds[3]:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT4'})   
                    elif dict_values_thresholds[3] < random_number <= dict_values_thresholds[4]:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT5'}) 
                    else:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT2'})
                
 
            
        return dict_owners, dict_owners_output , self.UT_distribution

class propertynotKnown(userType_config):
    """
    Parameters:
        
        UT_distribution (dict -> %) -- Percentage of distribution of User Types (5)      

        UT1 - 50/50
        UT2 - 10 years - 120 quotes
        UT3 - 15 years - 180 quotes
        UT4 - inscription in the register
        UT5 - defaulter
        
     """    
    def __init__(self, UT_distribution):
        super().__init__(UT_distribution)
    def userTypeInsert(self, ref_cat = 'all'):        
        """
        Inputs:            
            ref_cat (string) -- Write ref_cat to analyse specific building or 'all' to analyse all the buildings in the DDBB    
      
        """

        import random
        from itertools import accumulate
        
        
        sourceData = getDataARV.SQL_propertyARV()    # SQL_statments ARV
        get_data = getDataARV.getData_ARV(sourceData)   # Surfaces of each building
        # Reposity Outputs dicts -> 1) Area of each building (floor-roof-wall) with cadastral referece + 2) Partition ratio with cadastral referece
        dict_owners = get_data.start()       
        
        dict_owners_output = {}
        dict_values_thresholds = list(accumulate(list(self.UT_distribution.values())))
        for i in dict_owners:
            if i in ref_cat or ref_cat == 'all':
                dict_owners_output.setdefault(i,{})
                for j in dict_owners[i]:
                    random_number = random.randint(self.UT_distribution['UT1'], 100)             
                    if random_number <= dict_values_thresholds[0]: 
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT1'})
                    elif dict_values_thresholds[0] < random_number <= dict_values_thresholds[1]:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT2'})                        
                    elif dict_values_thresholds[1] < random_number <= dict_values_thresholds[2]:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT3'})    
                    elif dict_values_thresholds[2] < random_number <= dict_values_thresholds[3]:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT4'})   
                    elif dict_values_thresholds[3] < random_number <= dict_values_thresholds[4]:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT5'})  
                    else:
                        dict_owners_output[i].setdefault(j, {'userType' : 'UT2'})
                
 
            
        return dict_owners, dict_owners_output , self.UT_distribution

if __name__ == '__main__':
    scenario_usertype = propertynotKnow({'UT1' : 15, 'UT2' :  50, 'UT3' : 10, 'UT4' : 15, 'UT5': 10})
    dict_owners, dict_owners_output,  output_usertype = scenario_usertype.userTypeInsert('all')


    