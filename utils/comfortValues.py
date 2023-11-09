# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:51:06 2022

@author: srabadan
"""

from abc import ABC, abstractmethod




class outputAnalysis(ABC):
    @abstractmethod
    def calculation(self,Humidex):
        pass  


class humidexIndex(outputAnalysis):
    def calculation(self,Humidex):    
        comfortOutcomes = {}
        for i in Humidex:
            comfortOutcomes.setdefault(i,{'Little or no Discomfort':0,'Noticeable Discomfort':0,'Evident Discomfort':0,'Intense Discomfort':0,'Dangerous Discomfort':0,'Heat Stroke Probable':0})
            for j in Humidex[i]:
                if j < 30:
                    comfortOutcomes[i]['Little or no Discomfort'] = comfortOutcomes[i]['Little or no Discomfort'] + 1
                if 30 <= j < 35:
                    comfortOutcomes[i]['Noticeable Discomfort'] = comfortOutcomes[i]['Noticeable Discomfort'] + 1
                if 35 <= j < 40:
                    comfortOutcomes[i]['Evident Discomfort'] = comfortOutcomes[i]['Evident Discomfort'] + 1        
                if 40 <= j < 45:
                    comfortOutcomes[i]['Intense Discomfort'] = comfortOutcomes[i]['Intense Discomfort'] + 1                     
                if 45 <= j < 54:
                    comfortOutcomes[i]['Dangerous Discomfort'] = comfortOutcomes[i]['Dangerous Discomfort'] + 1    
                if j >= 54:
                    comfortOutcomes[i]['Heat Stroke Probable'] = comfortOutcomes[i]['Heat Stroke Probable'] + 1             
        return comfortOutcomes
    
class TopIndex(outputAnalysis):
    def calculation(self,top):  
        comfortOutcomes = {}
        for i in top:
            m = 0
            count = 0
            comfortOutcomes.setdefault(i,{'IEQ_w1':0,'IEQ_w2':0,'IEQ_w3':0,'IEQ_w4':0,'IEQ_s1':0,'IEQ_s2':0,'IEQ_s3':0,'IEQ_s4':0})
            for j in top[i]:
                count = count + 1
                if 1 <= count < 2160 or 6552 < count <= 8760:  # Winter October - March
                    if 7 <= m < 23: 
                        if j > 20:
                            comfortOutcomes[i]['IEQ_w1'] = comfortOutcomes[i]['IEQ_w1'] + 1
                        if 18 < j <= 20:
                            comfortOutcomes[i]['IEQ_w2'] = comfortOutcomes[i]['IEQ_w2'] + 1                        
                        if 16 <= j <= 18:
                            comfortOutcomes[i]['IEQ_w3'] = comfortOutcomes[i]['IEQ_w3'] + 1 
                        if  j < 16:
                            comfortOutcomes[i]['IEQ_w4'] = comfortOutcomes[i]['IEQ_w4'] + 1  
                            # AÑADIR UN CONDICIONAL PARA BAJAR LA TEMPERATURA POR LA NOCHE -> 17ºC setpoint -> 7 up a 23 down
                    else:
                        if j >= 17:
                            comfortOutcomes[i]['IEQ_w1'] = comfortOutcomes[i]['IEQ_w1'] + 1
                        if 16 < j < 17:
                            comfortOutcomes[i]['IEQ_w2'] = comfortOutcomes[i]['IEQ_w2'] + 1                        
                        if 15 <= j <= 16:
                            comfortOutcomes[i]['IEQ_w3'] = comfortOutcomes[i]['IEQ_w3'] + 1 
                        if  j < 14:
                            comfortOutcomes[i]['IEQ_w4'] = comfortOutcomes[i]['IEQ_w4'] + 1  
                            # AÑADIR UN CONDICIONAL PARA BAJAR LA TEMPERATURA POR LA NOCHE -> 17ºC setpoint -> 7 up a 23 down
       
                if not (1 <= count < 2160 or 6552 < count <= 8760):  # Summer May - September
                    if 7 <= m < 23:                                 
                        if j <= 26:
                            comfortOutcomes[i]['IEQ_s1'] = comfortOutcomes[i]['IEQ_s1'] + 1
                        if 26 < j <= 27:
                            comfortOutcomes[i]['IEQ_s2'] = comfortOutcomes[i]['IEQ_s2'] + 1                        
                        if 27 < j <= 28:
                            comfortOutcomes[i]['IEQ_s3'] = comfortOutcomes[i]['IEQ_s3'] + 1 
                        if  j > 28:
                            comfortOutcomes[i]['IEQ_s4'] = comfortOutcomes[i]['IEQ_s4'] + 1
                    else:
                        if j <= 35:
                            comfortOutcomes[i]['IEQ_s1'] = comfortOutcomes[i]['IEQ_s1'] + 1
                        if 35 < j <= 36:
                            comfortOutcomes[i]['IEQ_s2'] = comfortOutcomes[i]['IEQ_s2'] + 1                        
                        if 36 < j <= 37:
                            comfortOutcomes[i]['IEQ_s3'] = comfortOutcomes[i]['IEQ_s3'] + 1 
                        if  j > 37:
                            comfortOutcomes[i]['IEQ_s4'] = comfortOutcomes[i]['IEQ_s4'] + 1                             
                if m == 23:
                    m = 0
                if m!= 23:
                    m = m + 1                         
            
        return comfortOutcomes    
class calculo:
    def __init__(self, typeAnalysis : outputAnalysis,Humidex):
        self.typeAnalysis = typeAnalysis
        self.Humidex = Humidex

         
    def start(self):        
        return self.typeAnalysis.calculation(self.Humidex)
        