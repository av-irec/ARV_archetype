# -*- coding: utf-8 -*-
"""
Created on Mon May  2 08:44:28 2022

@author: srabadan
"""

#Abstract method import

from abc import ABC, abstractmethod

# Resources

from resources import reader

# Repositories


# Abstract class

class currencyType(ABC):
    @abstractmethod
    def harmonizeCMH_data(self,direction):
        pass  
    

class CMH_data(currencyType): # Get data from CMH prices
    def harmonizeCMH_data(self,direction):
        typeFile = reader.readCSV()   #file .csv 
        read = reader.reader(direction,typeFile) # Resource to read
        data_CMH_base = read.start()  #Output --> Dict with prices inputs. Key -> magnitude - Value -> Cost
        data_CMH_harmonised = {}
        for i in data_CMH_base:
            data_CMH_harmonised[i[0]] = i[-1]
        return data_CMH_harmonised

        
        
class getData_CMH:
    def __init__(self, typeFile : currencyType,direction):
        self.typeFile = typeFile
        self.direction = direction
         
    def start(self):        
        return self.typeFile.harmonizeCMH_data(self.direction)
    
# if __name__ == '__main__':
#     typeFile = objGeom()
#     dire = r'..\resources\data\zona_pilotes.obj'
#     hamonize = harmonizer(typeFile, dire)
#     geometry_base, geometry, geometry_face, geometry_ref  = hamonize.start()    
    
    
    
    
    
    