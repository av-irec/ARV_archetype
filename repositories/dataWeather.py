# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:03:37 2022

@author: srabadan
"""

#Abstract method import

from abc import ABC, abstractmethod

# Resources

from resources import reader

# Abstract class

class currencyType(ABC):
    @abstractmethod
    def dataSource(self,direction):
        pass  
        
class fileTRNSYS(currencyType): # Read .out weather from TRNSYS 
    def dataSource(self,filePath):
        import pandas as pd
        typeFile = reader.readTRNSYS()
        df = reader.reader(filePath,typeFile)
        df = df.start()
        df.index = [pd.Timestamp('2021-01-01 00:00') + pd.Timedelta(hours=i) for i in df.index]
        df.columns = [namecol.replace(' ', '') for namecol in df.columns]
        return df        
        
    
class file_CSV(currencyType): # Read weather data from CSV
    def dataSource(self,filePath):
        pass


             
    
class dataWeather:
    def __init__(self, typeFile : currencyType,direction):
        self.direction = direction
        self.typeFile = typeFile
         
    def start(self):        
        return self.typeFile.dataSource(self.direction)
    
    
if __name__ == '__main__':
    typeFile = fileTRNSYS()
    dire = r'..\resources\data\C2Barcelona_Airp.out'
    get_data = dataWeather(typeFile, dire)
    params = get_data.start()      
  
    
