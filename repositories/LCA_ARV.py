# -*- coding: utf-8 -*-
"""

@author: srabadan
"""

from abc import ABC, abstractmethod
from resources import reader


class currencyProject(ABC):
    @abstractmethod
    def get_data(self,project):
        pass              
      
    
        
class LCA_ARV(currencyProject):
    def get_data(project):
        import sys
        direct = sys.path[0]
        filePath = direct + '\\resources\data\LCA_data.csv'
        typeFile = reader.readCSV_withoutheader()
        read = reader.reader(filePath,typeFile)
        output_reader = read.start()        
        materials = {}
        for i in output_reader:                    # Dictionary with n Zones as a key
            if i[0] not in materials.keys():
                materials.setdefault(i[0],{'espesor':{}})
                for j in output_reader:
                    if i[0] == j[0]:
                        materials[i[0]]['espesor'][j[1]] =  {'€_m2':j[2],'A1-3_CO2':j[3],'A4_CO2':j[4],'A5_CO2':j[5],'A1-3_EPNR':j[6],'A4_EPNR':j[7],'A5_EPNR':j[8]}                   
                
    
        return materials
        

        
class readLCA_ARV:
    def __init__(self, project : currencyProject):
        self.project = project
         
    def start(self):        
        return self.project.get_data()
    
    

if __name__ == '__main__':
    
    project = LCA_ARV()
    output = readLCA_ARV(project)
    data_LCA  = output.start()     


# materials.setdefault(i[0],{'espesor':,'€_m2':0,'A1-3_CO2':0,'A4_CO2':0,'A5_CO2':0,'A1-3_EPNR':0,'A4_EPNR':0,'A5_EPNR':0}) # kgCO2/m2 - MJ/m2 (PENRT)
    
    
    
    
    
