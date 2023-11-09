# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:51:06 2022

@author: srabadan
"""

from abc import ABC, abstractmethod




class outputAnalysis(ABC):
    @abstractmethod
    def calculation(self,humidex,top,n_zones):
        pass  


class comfortGraph(outputAnalysis):
    def calculation(self,humidex,top,n_zones):
        DW_sum_humidex = 0
        for i in range(1,n_zones+1):
            # DW_sum_humidex = DW_sum_humidex + humidex['DW_' + str(i)]['Noticeable Discomfort'] + humidex['DW_' + str(i)]['Evident Discomfort'] + humidex['DW_' + str(i)]['Intense Discomfort'] + humidex['DW_' + str(i)]['Dangerous Discomfort'] + humidex['DW_' + str(i)]['Heat Stroke Probable']  
            # DW_sum_humidex = DW_sum_humidex + humidex['DW_' + str(i)]['Intense Discomfort'] + humidex['DW_' + str(i)]['Dangerous Discomfort'] + humidex['DW_' + str(i)]['Heat Stroke Probable']  
            DW_sum_humidex = DW_sum_humidex + humidex['DW_' + str(i)]['Evident Discomfort'] + humidex['DW_' + str(i)]['Intense Discomfort'] + humidex['DW_' + str(i)]['Dangerous Discomfort'] + humidex['DW_' + str(i)]['Heat Stroke Probable']  

        DW_average_above = DW_sum_humidex/n_zones
        x_graph_humidex = DW_average_above/8760*100 # % de horas
        DW_sum_humidex = 0
        for i in range(1,n_zones+1):
            # DW_sum_humidex = DW_sum_humidex + humidex['DW_' + str(i)]['Evident Discomfort'] + humidex['DW_' + str(i)]['Intense Discomfort'] + humidex['DW_' + str(i)]['Dangerous Discomfort'] + humidex['DW_' + str(i)]['Heat Stroke Probable']  
            # DW_sum_humidex = DW_sum_humidex + humidex['DW_' + str(i)]['Intense Discomfort'] + humidex['DW_' + str(i)]['Dangerous Discomfort'] + humidex['DW_' + str(i)]['Heat Stroke Probable']  
            DW_sum_humidex = DW_sum_humidex + humidex['DW_' + str(i)]['Evident Discomfort'] + humidex['DW_' + str(i)]['Intense Discomfort'] + humidex['DW_' + str(i)]['Dangerous Discomfort'] + humidex['DW_' + str(i)]['Heat Stroke Probable']  

        DW_average_above = DW_sum_humidex/n_zones        
        point_graph_humidex = DW_average_above

        DW_sum_top = 0
        for i in range(1,n_zones+1):
            # DW_sum_top = DW_sum_top + top['DW_' + str(i)]['IEQ_w2'] + top['DW_' + str(i)]['IEQ_w3'] + top['DW_' + str(i)]['IEQ_w4']
            DW_sum_top = DW_sum_top + top['DW_' + str(i)]['IEQ_w3'] + top['DW_' + str(i)]['IEQ_w4']            
        DW_average_dis_winter = DW_sum_top/n_zones        
        y_graph_winter_dis = DW_average_dis_winter/8760*100 # % de horas
        
        DW_sum_top = 0
        for i in range(1,n_zones+1):
            # DW_sum_top = DW_sum_top + top['DW_' + str(i)]['IEQ_s2'] + top['DW_' + str(i)]['IEQ_s3'] + top['DW_' + str(i)]['IEQ_s4']
            DW_sum_top = DW_sum_top + top['DW_' + str(i)]['IEQ_s3'] + top['DW_' + str(i)]['IEQ_s4']            
        DW_average_dis_summer = DW_sum_top/n_zones        
        x_graph_summer_dis = DW_average_dis_summer/8760*100 # % de horas        
        
        DW_sum_humidex = 0
        for i in range(1,n_zones+1):
            DW_sum_humidex = DW_sum_humidex + humidex['DW_' + str(i)]['Intense Discomfort'] + humidex['DW_' + str(i)]['Dangerous Discomfort'] + humidex['DW_' + str(i)]['Heat Stroke Probable']  
        DW_average_above = DW_sum_humidex/n_zones        
        point_graph_humidex = DW_average_above    

        
        
        return x_graph_humidex, point_graph_humidex, x_graph_summer_dis, y_graph_winter_dis
    
class calculo:
    def __init__(self, typeAnalysis : outputAnalysis,humidex,top,n_zones):
        self.typeAnalysis = typeAnalysis
        self.humidex = humidex
        self.n_zones = n_zones
        self.top = top
         
    def start(self):        
        return self.typeAnalysis.calculation(self.humidex,self.top,self.n_zones)
        