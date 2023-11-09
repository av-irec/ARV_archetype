# -*- coding: utf-8 -*-
"""

@author: avaquero
"""

from abc import ABC, abstractmethod
from resources import reader
from utils import processCaracas
import os

class currencyStep(ABC):
    @abstractmethod
    def get_data(self,typeStep):
        pass


class yearly(currencyStep):
    def get_data(typeStep,n_zones):
        pass

class monthly(currencyStep):
    def get_data(typeStep,n_zones):
        pass

class HourlyMulti(currencyStep):
    def get_data(typeStep,n_zones, name, refcat):
        import sys
        import os
        direct = sys.path[0]
        filePath = direct + '\\resources\data' + '\\' + str(name) + '\\' +'AllCombinedResults.csv'
        typeFile = reader.readCSV_withoutheader()
        read = reader.reader(filePath,typeFile)
        output_reader = read.start() 
        folders = []
        for i in output_reader:
            folders.append(i[1])
            
        P_ht = {}   # Heating demand
        P_cl = {}   # Cooling demand
        P_lig = {}  # Lighting demand
        P_dev = {}  # Devices demand
        P_dhw = {}  # Domestic hot water demand                
                
        for j in folders:
            P_ht.setdefault(j,{})
            P_cl.setdefault(j,{})
            P_lig.setdefault(j,{})
            P_dev.setdefault(j,{})
            P_dhw.setdefault(j,{})      
            filePath = direct + '\\resources\data' + '\\' + str(name) + '\\' + j + '\\' + 'Demand_per_use_FB2.txt'
            typeFile = reader.readCSV_withoutheader()
            read = reader.reader(filePath,typeFile)
            output_reader = read.start() 
                
            for k in range(1,n_zones+1):                    # Dictionary with n Zones as a key
                P_dev[j].setdefault('Dwelling_' + str(k),[])    
                P_lig[j].setdefault('Dwelling_' + str(k),[])
                P_ht[j].setdefault('Dwelling_' + str(k),[])
                P_cl[j].setdefault('Dwelling_' + str(k),[])
                P_dhw[j].setdefault('Dwelling_' + str(k),[])
               
            for k in output_reader:                      # Distributing the input data
                column_count = 1
                for n in range(1,n_zones+1):
                    data = k[0].split('\t')
                    P_dev[j]['Dwelling_' + str(n)].append(float(data[column_count].strip()))
                    P_lig[j]['Dwelling_' + str(n)].append(float(data[column_count+1].strip()))               
                    P_ht[j]['Dwelling_' + str(n)].append(float(data[column_count+2].strip()))            
                    P_cl[j]['Dwelling_' + str(n)].append(float(data[column_count+3].strip()))        
                    P_dhw[j]['Dwelling_' + str(n)].append(float(data[column_count+4].strip()))
                    column_count = column_count + 5
            
            for k in range(1,n_zones+1):                 # Delete the last row from the data
                    P_ht[j]['Dwelling_' + str(k)].pop(-1)
                    P_cl[j]['Dwelling_' + str(k)].pop(-1)               
                    P_lig[j]['Dwelling_' + str(k)].pop(-1)            
                    P_dev[j]['Dwelling_' + str(k)].pop(-1)       
                    P_dhw[j]['Dwelling_' + str(k)].pop(-1)



        if name == 'Caracas1':

            P_ht, P_cl, P_lig, P_dev, P_dhw = processCaracas.process_caracas(refcat,P_ht,P_cl,P_lig,P_dev,P_dhw)
        else:
            pass


        return output_reader, P_ht, P_cl, P_lig, P_dev, P_dhw
    

class comfortMulti(currencyStep):
    def get_data(typeStep,n_zones,refcat):
        import sys
        import os
        direct = r'C:\Users\avaquero\OneDrive - IREC-edu\CODI\11_AnalysisArchetype_Génerico' #sys.path[0]
        t = os.listdir(direct + '\\resources\data\outputs_TRNSYS_caracas')
        folders = {}
        for i in t:
            folders.setdefault(i,[])
            filePath = direct + '\\resources\data\outputs_TRNSYS_caracas'+ '\\' + i +'\\' +'AllCombinedResults.csv'
            typeFile = reader.readCSV_withoutheader()
            read = reader.reader(filePath,typeFile)
            output_reader = read.start()   
            for j in output_reader:
                folders[i].append(j[1])
        Humidex = {}   #  % of time in each category 
        T_op = {}                    
        for i in folders:
            for j in folders[i]:
                Humidex.setdefault(j,{})
                T_op.setdefault(j,{})
                filePath = direct + '\\resources\data\outputs_TRNSYS_caracas'+ '\\' + i +'\\' + j + '\\' + 'Commit_AllOutput.csv'
                typeFile = reader.readCSV_withoutheader()
                read = reader.reader(filePath,typeFile)
                output_reader = read.start()                  
      
                for k in range(1,n_zones+1):                    # Dictionary with n Zones as a key
                    Humidex[j].setdefault('DW_' + str(k),[])    
                    T_op[j].setdefault('DW_' + str(k),[])                          
                for k in output_reader:                      # Distributing the input data
                    for n in range(1,n_zones+1):
                        if n_zones == 3:
                            Humidex[j]['DW_' + str(n)].append(float(k[n+86]))
                            T_op[j]['DW_' + str(n)].append(float(k[n+89]))
                        if n_zones == 4:
                            if n < 4:
                                Humidex[j]['DW_' + str(n)].append(float(k[n+86]))
                                T_op[j]['DW_' + str(n)].append(float(k[n+89]))
                            if n == 4:
                                Humidex[j]['DW_' + str(n)].append(float(k[95]))
                                T_op[j]['DW_' + str(n)].append(float(k[n+89]))                                
                        
                for k in range(1,n_zones+1):                 # Delete the last row from the data
                        Humidex[j]['DW_' + str(k)].pop(0) 
                        T_op[j]['DW_' + str(k)].pop(0)
        return Humidex, T_op
        
class readTRNSYS:
    def __init__(self, typeStep : currencyStep, n_zones, name,refcat):
        self.typeStep = typeStep
        self.n_zones = n_zones
        self.name = name
        self.refcat = refcat
         
    def start(self):        
        return self.typeStep.get_data(self.n_zones, self.name, self.refcat)

    
if __name__ == '__main__':
    typeStep = HourlyMulti()
    n_zones = 1
    name = 'FE35'
    output_reader, P_ht, P_cl, P_lig, P_dev, P_dhw = readTRNSYS(typeStep,n_zones, name, refcat).start()
    





    
    
    
    
    
