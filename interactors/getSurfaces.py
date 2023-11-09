# -*- coding: utf-8 -*-
"""
Created on Mon May  2 08:44:28 2022

@author: srabadan
"""

#Abstract method import

from abc import ABC, abstractmethod



# Repositories

from repositories import harmonize_surfaces

# Abstract class

class currencyType(ABC):
    @abstractmethod
    def getSurfaces(self,direction):
        pass  
    

class SQL_dataARV(currencyType): # 
    def getSurfaces(self):
        typeFile = harmonize_surfaces.get_surfaces()   # Repository to use
        read = harmonize_surfaces.harmonizer(typeFile) 
        areabyCadastralcode, distributionRatio, ref_use = read.start()  #Output --> 2 dicts -> 1) Area of each building (floor-roof-wall) with cadastral referece + 2) Partition ratio with cadastral referece + 3) Use of the cadastral reference (dwelling-storage-comercial....) 

        return areabyCadastralcode, distributionRatio, ref_use

        
class getData_surfaces:
    def __init__(self, sourceData : currencyType):
        self.sourceData = sourceData
           # 
    def start(self):        
        return self.sourceData.getSurfaces()
    
# if __name__ == '__main__':
#     typeFile = objGeom()
#     dire = r'..\resources\data\zona_pilotes.obj'
#     hamonize = harmonizer(typeFile, dire)
#     geometry_base, geometry, geometry_face, geometry_ref  = hamonize.start()    
    
    
    
    
    
    