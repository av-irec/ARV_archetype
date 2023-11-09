# -*- coding: utf-8 -*-
"""
Created on Mon May  2 08:44:28 2022

@author: srabadan
"""

#Abstract method import

from abc import ABC, abstractmethod

# SQL_statments

from utils.getSurfacesARV import getSurfaces_ARV


# Abstract class

class currencyType(ABC):
    @abstractmethod
    def harmonizeSurface(self):
        pass  
    
#    
class get_surfaces(currencyType):
    def harmonizeSurface(self):
        
        #SQL conection details
        hostname = "localhost"      # Database in the PC
        database = "ARV_district_buildings"   # Set the database
        username = "postgres"       # Username in PostgreSQL
        pwd = "1234"                # Passwod in PostgreSQL
        port_id = 5432              # Port in PostgreSQL
        areabyCadastralcode, distributionRatio, ref_use= getSurfaces_ARV(hostname,database,username,pwd,port_id) #SQL script

        
        return areabyCadastralcode, distributionRatio, ref_use


        
        
class harmonizer:
    def __init__(self, typeFile : currencyType):
        self.typeFile = typeFile
         
    def start(self):        
        return self.typeFile.harmonizeSurface()
    

    
    
    
    
    
    