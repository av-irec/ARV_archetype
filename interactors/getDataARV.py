# -*- coding: utf-8 -*-
"""
Created on Mon May  2 08:44:28 2022

@author: srabadan
"""

#Abstract method import

from abc import ABC, abstractmethod



# Repositories

from repositories import harmonizeDataARV

# Abstract class

class currencyType(ABC):
    @abstractmethod
    def getData(self,direction):
        pass  
    

class SQL_surfaceARV(currencyType): # 
    def __init__(self,ref_cat):
        self.ref_cat = ref_cat
    def getData(self):
        typeFile = harmonizeDataARV.get_surfaces_1building(self.ref_cat)   # Repository to use
        read = harmonizeDataARV.harmonizer(typeFile) 
        areabyCadastralcode, distributionRatio, ref_use = read.start()  #Output --> 2 dicts -> 1) Area of each building (floor-roof-wall) with cadastral referece + 2) Partition ratio with cadastral referece + 3) Use of the cadastral reference (dwelling-storage-comercial....) 

        return areabyCadastralcode, distributionRatio, ref_use

class SQL_propertyARV(currencyType): # 
    def getData(self): 
        
        typeFile = harmonizeDataARV.get_property()   # Repository to use
        read = harmonizeDataARV.harmonizer(typeFile) 
        dict_owners = read.start()  

        return dict_owners

     
class getData_ARV:
    def __init__(self, sourceData : currencyType):
        self.sourceData = sourceData
           # 
    def start(self):        
        return self.sourceData.getData()
    
if __name__ == '__main__':
    source = SQL_surfaceARV(ref_cat = '1502501DD7810D')
    b = getData_ARV(source)
    areabyCadastralcode, distributionRatio, ref_use = b.start()
 
    
    
    
    
    
    