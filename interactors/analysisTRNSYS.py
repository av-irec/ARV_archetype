# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:24:52 2022

@author: srabadan
"""


# Abstract method import

from abc import ABC, abstractmethod

# Repositories


from repositories import csvTRNSYS, csvTRNSYS
from utils import comfortValues, comfortGraph, transformation_EP_CO2
# Abstract class


class currencyAnalysis(ABC):
    def __init__(self, n_viv, name, refcat):
        self.n_viv = n_viv
        self.name = name
        self.refcat = refcat
    @abstractmethod
    def analysisCalculation(self):
        pass


class energyAnalysis(currencyAnalysis):  # Calculation of the investment with CMH data as a cost input
    """
    Parameters:
        
        n_viv (int) -- Número de viviendas simuladas
        name (str) -- Nombre de la carpeta donde están los resultados de las simulaciones
       
    """    
    def __init__(self, n_viv, name, refcat):
        currencyAnalysis.__init__(self, n_viv, name, refcat)
    def analysisCalculation(self):
        
        # Lectura de los archivos que salen directamente de la simulación en TRNSYS (ver word "detallesinputs")
        
        typeStep = csvTRNSYS.HourlyMulti()
        output = csvTRNSYS.readTRNSYS(typeStep, self.n_viv, self.name, self.refcat)
        output_reader, P_ht, P_cl, P_lig, P_dev, P_dhw = output.start()
        
        # Repartición de consumos para el caso en donde no haya reforma de la parte activa

        grado_ht = {'joule':0.35,'BC':0.28,'caldera_GN':0.15,'butano':0.15,'nada':0.07}
        grado_cl = {'split':0.1,'BC':0.43,'multi_split':0.04,'nada':0.43}
        grado_dhw ={'caldera_GN':0.64,'butano':0.1,'BC':0, 'joule':0.26}
        
        # Diccionarios con el mismo formato que P_ht. P_cl, P_lig, P_dev y P_dhw
        
        PE_ht = {}
        PE_cl = {}
        PE_lig = {}
        PE_dev = {}
        PE_dhw = {}
     
        # Instancia de la clase para pasar de demanda a consumo de energía primaria.
         
        project = transformation_EP_CO2.pE_ARV_demand(grado_ht, grado_cl, grado_dhw)
        for i in P_ht:
            
            # El método pE_ARV_demand que se encuentra dentro de la clase transformation_EP_CO2 se ejectura 1 vez por cada simulación leída
            
            output = transformation_EP_CO2.calculo(project, P_ht[i], P_cl[i], P_lig[i],P_dev[i],P_dhw[i])
            PE_ht_aux, PE_cl_aux, PE_lig_aux,PE_dev_aux ,PE_dhw_aux = output.start()
            PE_ht.setdefault(i, PE_ht_aux)
            PE_cl.setdefault(i, PE_cl_aux)
            PE_lig.setdefault(i, PE_lig_aux)
            PE_dev.setdefault(i,PE_dev_aux)
            PE_dhw.setdefault(i, PE_dhw_aux)
                

        CO2_ht = {}
        CO2_cl = {}
        CO2_lig = {}
        CO2_dev = {}
        CO2_dhw = {}
        
        # Instancia de la clase para pasar de demanda a emisiones de CO2
        
        project = transformation_EP_CO2.CO2_ARV_demand(grado_ht, grado_cl, grado_dhw)
        for i in P_ht:
            
            # El método CO2_ARV_demand que se encuentra dentro de la clase transformation_EP_CO2 se ejectura 1 vez por cada simulación leída
            
            output = transformation_EP_CO2.calculo(
                project, P_ht[i], P_cl[i], P_lig[i],P_dev[i],P_dhw[i])
            CO2_ht_aux, CO2_cl_aux, CO2_lig_aux, CO2_dev_aux, CO2_dhw_aux   = output.start()
            CO2_ht.setdefault(i, CO2_ht_aux)
            CO2_cl.setdefault(i, CO2_cl_aux)
            CO2_lig.setdefault(i, CO2_lig_aux)
            CO2_dev.setdefault(i,CO2_dev_aux)
            CO2_dhw.setdefault(i, CO2_dhw_aux)

        return P_ht, P_cl, P_lig, P_dev, P_dhw, PE_ht, PE_cl, PE_lig,PE_dev ,PE_dhw, CO2_ht, CO2_cl, CO2_lig, CO2_dev, CO2_dhw                               

class comfortAnalysis(currencyAnalysis):  
    """
    
    Lectura de los valores de comfort *** falta reprogramación a las nuevas simulaciones. Para la reprogramación se propone:
    
    1) No sacar los gráficos directamente, los outputs deben ser los valores de humidex y temperatura operativa que se calculan en el 'util' comfortValues()
    2) Ajustar la lectura y sobretodo los outputs de TRNSYS para que los parámetros saen los mismos que en la clase energyAnalysis(), n_viv + name
    3) n_viv son las viviendas simuladas, este valor debe servir para que el código lea inequivocamente donde tiene que leer, columnas del .out/.csv. Tomar como ejemplo csvTRNSYS.HourlyMulti() 
    
    """
    
    def __init__(self, n_viv, name):
        currencyAnalysis.__init__(self, n_viv, name)
    def analysisCalculation(self):
        pass
        typeStep = csvTRNSYS.comfortMulti()
        output = csvTRNSYS.readTRNSYS(typeStep, self.n_viv)
        Humidex, T_op = output.start()    
        x_graph_comfort = {}
        point_graph_comfort = {}
        x_graph_summer_dis = {}
        y_graph_winter_dis = {}
        
        for i in Humidex:
            
            typeAnalysis = comfortValues.humidexIndex()
            output = comfortValues.calculo(typeAnalysis, Humidex[i])
            humidexOutcomes = output.start()
            
            typeAnalysis = comfortValues.TopIndex()
            output = comfortValues.calculo(typeAnalysis, T_op[i])
            topOutcomes = output.start()            
            

            typeAnalysis = comfortGraph.comfortGraph()
            output = comfortGraph.calculo(typeAnalysis, humidexOutcomes,topOutcomes, self.n_viv)
            x_graph_comfort_aux, point_graph_comfort_aux, x_graph_summer_dis_aux,y_graph_winter_dis_aux = output.start()

            x_graph_comfort.setdefault(i, x_graph_comfort_aux)
            point_graph_comfort.setdefault(i, point_graph_comfort_aux)
            x_graph_summer_dis.setdefault(i, x_graph_summer_dis_aux)
            y_graph_winter_dis.setdefault(i, y_graph_winter_dis_aux)  

class do_analysis:
    def __init__(self, Project: currencyAnalysis):
        self.Project = Project

    def start(self):
        return self.Project.analysisCalculation()

if __name__ == '__main__':
    n_zones = 1
    n_viv = 1
    building_to_analyse = 'FE35'

    project = energyAnalysis(n_viv = n_viv, name = building_to_analyse)
    data = do_analysis(project)
    output_reader_LCA, P_ht, P_cl, P_lig, P_dev, P_dhw, PE_ht, PE_cl, PE_lig,PE_dev ,PE_dhw, CO2_ht, CO2_cl, CO2_lig, CO2_dev, CO2_dhw  = data.start()

    print(P_ht)
    print(PE_ht)
    print(CO2_ht)