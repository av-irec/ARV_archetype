# -*- coding: utf-8 -*-
"""

@author: srabadan
"""

from abc import ABC, abstractmethod
from resources import reader
from utils import sumfloors


class currencyOutput(ABC):
    @abstractmethod
    def calculation(self,PE_ht, PE_cl, PE_lig, PE_dev,PE_dhw):
        pass              
      

class ARV_dwellings(currencyOutput):
    """
    Inputs:
        Independientemente que se llame 'PE' puede ser demanda (P), energía primaria (PE) o emisiones (CO2)

        
    """    
    def calculation(self,**kwargs): 
        
        """
        Se utiliza **kwargs que nos permite separar en modo clave-valor para que la media se haga independientemente de:
            1) Número de viviendas
            2) Número de simulaciones
            3) Nombre de las carpetas            
        """
        
        output = {} 
        count_args = 0
        for i in kwargs:
            output.setdefault(str(i),{})
            for j in kwargs[i]:
                output[str(i)].setdefault(j,{})
                aux = 0
                count = 0
                for k in kwargs[i][j]:
                    aux = aux + sum(kwargs[i][j][k])
                    count = count + 1
                output[str(i)][j] = aux/count    
            count_args = count_args + 1             

        return output['PE_ht'], output['PE_cl'] , output['PE_lig'] , output['PE_dev'], output['PE_dhw']

        
class calculo:
    def __init__(self, project : currencyOutput,PE_ht, PE_cl, PE_lig,PE_dev, PE_dhw, name):
        self.project = project
        self.PE_ht = PE_ht
        self.PE_cl = PE_cl
        self.PE_lig = PE_lig
        self.PE_dev = PE_dev
        self.PE_dhw = PE_dhw
        self.name = name

        
         
    def start(self):        
        output = self.project.calculation(PE_ht = self.PE_ht,PE_cl = self.PE_cl,PE_lig = self.PE_lig,PE_dev = self.PE_dev,PE_dhw = self.PE_dhw)
        if self.name == 'Caracas1':
            P_ht, P_cl, P_lig, P_dev, P_dhw = sumfloors.Sumfloors(output[0], output[1], output[2], output[3], output[4])
            return P_ht, P_cl, P_lig, P_dev, P_dhw
        else:
            return output
    
    




# materials.setdefault(i[0],{'espesor':,'€_m2':0,'A1-3_CO2':0,'A4_CO2':0,'A5_CO2':0,'A1-3_EPNR':0,'A4_EPNR':0,'A5_EPNR':0}) # kgCO2/m2 - MJ/m2 (PENRT)
    
    
    
    
    
