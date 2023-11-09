# -*- coding: utf-8 -*-
"""
Created on Mon May  2 08:44:28 2022

@author: srabadan
"""

#Abstract method import

from abc import ABC, abstractmethod

# SQL_statments

from SQL_statements.getSurfacesARV import getSurfaces_ARV
from SQL_statements.getPropertyARV import getProperty_ARV
from SQL_statements.getSurfacesARV_1building import getSurfaces_ARV_1building

# Abstract class

class currencyType(ABC):
    @abstractmethod
    def harmonizeData(self):
        pass  
    
#    
class get_surfaces(currencyType):
    def harmonizeData(self):

        #SQL conection details
        hostname = "172.16.27.100"      # Database in the PC
        database = "ARV_district_buildings"   # Set the database
        username = "postgres"       # Username in PostgreSQL
        pwd = "GeoTerm2023@@"                # Passwod in PostgreSQL
        port_id = 5432              # Port in PostgreSQL
        areabyCadastralcode, distributionRatio, ref_use= getSurfaces_ARV(hostname,database,username,pwd,port_id) #SQL script


        return areabyCadastralcode, distributionRatio, ref_use

class get_surfaces_1building(currencyType):
    def __init__(self, ref_cat):
        self.ref_cat = ref_cat
    def harmonizeData(self):
        
        #SQL conection details
        hostname = "172.16.27.100"      # Database in the PC
        database = "ARV_district_buildings"   # Set the database
        username = "postgres"       # Username in PostgreSQL
        pwd = "GeoTerm2023@@"                # Passwod in PostgreSQL
        port_id = 5432              # Port in PostgreSQL
        areabyCadastralcode, distributionRatio, ref_use= getSurfaces_ARV_1building(hostname,database,username,pwd,port_id, self.ref_cat) #SQL script

        
        return areabyCadastralcode, distributionRatio, ref_use

class get_property(currencyType):
    def harmonizeData(self):
        
        #SQL conection details
        hostname = "172.16.27.100"      # Database in the PC
        database = "ARV_district_buildings"   # Set the database
        username = "postgres"       # Username in PostgreSQL
        pwd = "GeoTerm2023@@"                # Passwod in PostgreSQL
        port_id = 5432              # Port in PostgreSQL
        dict_owners = getProperty_ARV(hostname,database,username,pwd,port_id) #SQL script

        
        return dict_owners
        
        
class harmonizer:
    def __init__(self, typeFile : currencyType):
        self.typeFile = typeFile
         
    def start(self):        
        return self.typeFile.harmonizeData()
    

    
    
    
    
    
    