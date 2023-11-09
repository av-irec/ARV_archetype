# -*- coding: utf-8 -*-
"""

@author: srabadan
"""

from abc import ABC, abstractmethod
from resources import reader


class currencyProject(ABC):
    @abstractmethod
    def calculation(self,y_graph_investment,n_zones,n_viv,EP_bc_total,EP_rf_total,Package):
        pass              
      
    
        
class ARV_grants(currencyProject):
    def calculation(self,y_graph_investment,n_zones,n_viv,EP_bc_total,EP_rf_total,Package):
        
        x_graph_inv_dPe = []
        y_graph_inv_dPe = []
        
        x_graph_inv_dPe.append(EP_bc_total)
        y_graph_inv_dPe.append(0)
        espesores = list(y_graph_investment['P1.1']['espesor'].keys())
        for i in range(0,len(EP_rf_total)):
            deltaPE = (1-(EP_rf_total[i]/EP_bc_total))*100
            if deltaPE < 30:
                x_graph_inv_dPe.append(EP_rf_total[i])
                y_graph_inv_dPe.append(y_graph_investment[Package]['espesor'][espesores[i]])                
            if 30 <= deltaPE < 45:
                x_graph_inv_dPe.append(EP_rf_total[i])
                if y_graph_investment[Package]['espesor'][espesores[i]]*0.4 >= 8100:
                    y_graph_inv_dPe.append((y_graph_investment[Package]['espesor'][espesores[i]])-8100)
                else:
                    y_graph_inv_dPe.append((y_graph_investment[Package]['espesor'][espesores[i]])*0.6)                
            if 45 <= deltaPE < 60:
                x_graph_inv_dPe.append(EP_rf_total[i])
                if y_graph_investment[Package]['espesor'][espesores[i]]*0.65 >= 14500:
                    y_graph_inv_dPe.append((y_graph_investment[Package]['espesor'][espesores[i]])-14500)
                else:
                    y_graph_inv_dPe.append((y_graph_investment[Package]['espesor'][espesores[i]])*0.35)
            if deltaPE >= 60:
                x_graph_inv_dPe.append(EP_rf_total[i])
                if y_graph_investment[Package]['espesor'][espesores[i]]*0.8 >= 21400:
                    y_graph_inv_dPe.append((y_graph_investment[Package]['espesor'][espesores[i]])-21400)
                else:
                    y_graph_inv_dPe.append((y_graph_investment[Package]['espesor'][espesores[i]])*0.2)                  
                
    
        
        return x_graph_inv_dPe, y_graph_inv_dPe

        

        
class calculo:
    def __init__(self, project : currencyProject,y_graph_investment,n_zones,n_viv,EP_bc_total,EP_rf_total,Package):
        self.project = project
        self.y_graph_investment = y_graph_investment
        self.n_zones = n_zones
        self.n_viv = n_viv
        self.EP_bc_total = EP_bc_total
        self.EP_rf_total = EP_rf_total
        self.Package = Package
         
    def start(self):        
        return self.project.calculation(self.y_graph_investment,self.n_zones,self.n_viv,self.EP_bc_total,self.EP_rf_total, self.Package)
    
    




# materials.setdefault(i[0],{'espesor':,'€_m2':0,'A1-3_CO2':0,'A4_CO2':0,'A5_CO2':0,'A1-3_EPNR':0,'A4_EPNR':0,'A5_EPNR':0}) # kgCO2/m2 - MJ/m2 (PENRT)
    
    
    
    
    
