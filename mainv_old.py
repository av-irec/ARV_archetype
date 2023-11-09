# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 18:18:31 2021

@author: Samuel Rabadán - IREC
"""

# Import libraries and packages
import os
import sys

# Path

direct = os.getcwd()
sys.path[0] = direct

from interactors import calculoCoste, analysisActive, investmentActiveARV, analysisTRNSYS
from utils import meanCalculation, energyScenarios, energyConsumption, globalCostScenarios



# %% Passive

"""
Este código main es para ARV:
    1) n_viv_simulated (int) -- Los inputs son el número de viviendas simuladas (columnas del output .out/.csv)
    2) building_to_analyse (str) -- Nombre de la carpeta donde están todas las simulaciones -> ..\1_analysisArchetype_Generico\resources\data\..
    3) ref_cat_analysis (str) -- Referencia catastral para obtener valores de la base de dato de ARV en PostgreSQL
"""
# n_viv_simulated = 2
# building_to_analyse = 'SIQUIER20'
# ref_cat_analysis = '1902602DD7810D'

n_viv_simulated = 1
building_to_analyse = 'FE35'
ref_cat_analysis = '1701521DD7810B'


surface = 90 # Superficie de cada vivienda para calcultar los valores de coste global

"""cs
El método energyAnalysis() de la clase analysisTRNSYS calcula la energía primara y el CO2 en función de las simuaciones
    1) Leer las carpetas de la simulaciones (para más detalles ver word "detallesinputs")
    2) Con los coeficientes de paso se calcula la energía primaria y el CO2
    3) P_ht (heating) - P_cl (cooling) - P_lig (iluminación - electricidad) - P_dev (electrodomésticos - electricidad) - P_dhw (agua caliente sanitaria)
    4) Las unidades son para P [kWh/m2] - PE [kWh/m2] - CO2 [kgCO2/m2]
    5) Estructura de diccionarios:
    
        P_ht{simulación
                {vivienda
                     [lista con 8760 valores]
                }
            }                
                                                             
"""

analysisType = analysisTRNSYS.energyAnalysis(n_viv = n_viv_simulated, name = building_to_analyse)
data = analysisTRNSYS.do_analysis(analysisType)
P_ht, P_cl, P_lig, P_dev, P_dhw, PE_ht, PE_cl, PE_lig,PE_dev ,PE_dhw, CO2_ht, CO2_cl, CO2_lig, CO2_dev, CO2_dhw = data.start()


"""
La clase meanCalculation realiza el cálculo de la media entre las simulaciones:
    
** Aqui falta realizar la ponderación de las plantas intermedias, para ARV:
    1) Añadir como input la referencia catastral
    2) Realizar la consulta en la base de datos SQL para saber el número de plantas
    3) Restarle al número de plantas obtenido 2 -> n_plantas_intermedias = n_plantas totales - 1 (planta baja) - 1 (planta bajo cubierta)
    4) Multiplicar los consumos de la planta intermedia por n_plantas_intermedias
    5) Ver en el word "detallesinputs"  la propuesta de identificación de las plantas intermedias.
       
El output PE_ht_mean es 1 número float con la suma anual                                                             
"""

project = meanCalculation.ARV_dwellings() # Las medias de energía primaria se utilizan para calcular las subvenciones
output = meanCalculation.calculo(project, PE_ht, PE_cl, PE_lig,PE_dev, PE_dhw)
PE_ht_mean, PE_cl_mean, PE_lig_mean,PE_dev_mean ,PE_dhw_mean = output.start()

project = meanCalculation.ARV_dwellings() # Las medias de energía primaria NO se utilizan, valor de comprobación 
output = meanCalculation.calculo(project, P_ht, P_cl, P_lig,P_dev, P_dhw)
P_ht_mean, P_cl_mean, P_lig_mean,P_dev_mean ,P_dhw_mean = output.start()


"""
Inputs más influyentes para el modelo económico, el resto están predefinidos                                                            
"""

Pfees = 0.02 # Coste de los proyectos -> % sobre le PEM
DF = 0.03 # Coste de la dirección de obra -> % sobre le PEM
tender_down = 0.1 # Reducción por economía de escala
facilities_passive = {'DHW' : False, 'PV' : False, 'HVAC' : False} # Para el cálculo de medidas pasivas no hay instalaciones

''' 
"""
Outputs del modelo econonómico -> 1 por carpeta de simulación                                                   
"""

buildingCost_passive = {}
dwellingCost_passive = {}
dwellings_fees_passive = {}
buildingGrants_passive = {}
deltaEPNR_passive = {}
PE_passive = {}
EPNR_BC = {}

for i in PE_ht_mean:
    count_esp = -1
    buildingCost_passive.setdefault(i,{})
    dwellingCost_passive.setdefault(i,{})
    dwellings_fees_passive.setdefault(i,{})
    buildingGrants_passive.setdefault(i,{})
    deltaEPNR_passive.setdefault(i,0)
    PE_passive.setdefault(i,0)
    i_aux = i.split('_')   # Identificación de los parámetros de la simulación (ver "detallesinputs")
    i_aux_2 = list(i_aux[0]) # Identificación de los parámetros de la simulación (ver "detallesinputs")
    if 'BC' in i:           # Calculo del caso base (1 por orientación -> 4 en total)
        EPNR_BC.setdefault(i,PE_ht_mean[i]+PE_cl_mean[i]+PE_dhw_mean[i]) 
        deltaEPNR_passive[i] = 0 
        PE_passive[i] = EPNR_BC[i]             
    if not 'BC' in i:
        if i_aux_2[1] == str(1): # ¿Simulación con ventanas?
            windows = False
        else:
            windows = True
        PE_passive[i] = PE_ht_mean[i]+PE_cl_mean[i]+PE_dhw_mean[i]
        if i_aux[1] == str(0):  # Identificación de la orientación
            EPNR_BC_aux =  EPNR_BC['BC0_'+str(0)]              
        if i_aux[1] == str(90):
            EPNR_BC_aux =  EPNR_BC['BC0_'+str(90)]  
        if i_aux[1] == str(180):
            EPNR_BC_aux =  EPNR_BC['BC0_'+str(180)]  
        if i_aux[1] == str(270):
            EPNR_BC_aux =  EPNR_BC['BC0_'+str(270)]  
        deltaEPNR_passive[i] = (1-(PE_passive[i]/EPNR_BC_aux))*100 # Reducción de energía primaria no renovable [%]
        """
        Llamada al modelo económico
        *** El método calculoCuota_CMH utilza los datos de un Excel, en el caso de ARV se debe cambiar y programar.
        La subvención predefinida es el programa 3 de rehabilitación de edificios (limites y % de subveción)
        """
        cuotaCalc = calculoCoste.calculoCuota_CMH(windows = windows, common_facilities = False, facilities = facilities_passive, Pfees = Pfees, DF = DF, tender_down = tender_down, deltaEPNR = deltaEPNR_passive[i], ref_cat_analysis = ref_cat_analysis)
        calc = calculoCoste.calculationCuote(cuotaCalc)
        buildingCost_aux, dwellingCost_aux, dwellings_fees_aux, building_grants_aux = calc.start()
        buildingCost_passive[i] = buildingCost_aux
        dwellingCost_passive[i] = dwellingCost_aux
        dwellings_fees_passive[i] = dwellings_fees_aux
        buildingGrants_passive[i] = building_grants_aux
        
        
'''

#%% Active & Energy Scenarios

"""
Opciones contempladas en ARV
"""

grado_ht = {'joule':0,'BC':1,'caldera_GN':0,'butano':0,'nada':0}
grado_cl = {'split':0,'BC':0,'multi_split':1,'nada':0}
grado_dhw ={'caldera_GN':0,'butano':0,'BC':1}


"""
Cálculo de la energía primaria con las instalaciones
"""

project = analysisActive.ARV_CO2_PE(P_cl, P_ht, P_lig, P_dev, P_dhw)
activeAnalysis = analysisActive.do_analysis(project, grado_ht, grado_cl, grado_dhw)
PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt , PE_dhw_rt, CO2_ht_rt, CO2_cl_rt, CO2_lig_rt, CO2_dev_rt, CO2_dhw_rt = activeAnalysis.start()

"""
Distribución de instalaciones base para el cálculo de medidas activas.
La distribución siempre será igual a la de analisysTRNSYS, de todas formas se ha dejado abierto por si fuera necesario modificarlo
"""



grado_ht = {'joule': 0.35, 'BC': 0.28, 'caldera_GN': 0.15, 'butano': 0.15, 'nada': 0.07}
grado_cl = {'split': 0.1, 'BC': 0.43, 'multi_split': 0.04, 'nada': 0.43}
grado_dhw = {'caldera_GN': 0.64, 'butano': 0.1, 'BC': 0, 'joule': 0.26}
        
"""
Cálculo de consumos por vector energético (electricidad - gas natural - butano) + estimación fotovoltaica
"""

output = energyConsumption.ARV_CONS(grado_ht, grado_cl, grado_dhw, ref_cat_analysis)
Cons_scenarios = energyConsumption.calculo(output, P_ht, P_cl, P_lig, P_dev, P_dhw)
output_scenarios_cons, PV_estimation = Cons_scenarios.start()

"""
Cálculo de energía primaria en función del escenario de medidas activas (electricidad - gas natural - butano) 
    --> Se introduce la energía primaria de todos los escenarios posibles (rehabilitado o no)
"""

output = energyScenarios.ARV_Scenarios()
PE_scenarios = energyScenarios.calculo(output, PE_ht, PE_cl, PE_lig, PE_dev, PE_dhw, PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt, PE_dhw_rt, PV_estimation)
output_scenarios_PE = PE_scenarios.start()






# %% Inversión incluyendo la parte activa



project = investmentActiveARV.investmentActive_ARV(output_scenarios_PE, ref_cat_analysis)
investmentAct = investmentActiveARV.calculation(project)
buildingCost_active, dwellingCost_active, dwellings_fees_active, buildingGrants_active, deltaEPNR_active = investmentAct.start()

#%% Excel de prueba 
def excel_curva(output_scenarios_PE, buildingCost_active, P_ht, P_cl, P_dhw, PE_ht, PE_cl, PE_dhw, deltaEPNR_active):

    import csv
    ruta_csv = 'Tabla_excel_' + building_to_analyse +'.csv' 
    with open(ruta_csv, 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        myData = []
        writer.writerow(['Caso','Ventanas','Convecional/Eco','Opción','Espesor (W)','Espesor (R)','Orientación','Msplit','PV','BC','Investment','EPNR','P_ht','P_cl','P_dhw','PE_ht','PE_cl','PE_dhw','deltaEPNR_active',''])
        for i in output_scenarios_PE:
            for j in output_scenarios_PE[i]:
                data_aux = []
                # Caso
                valor_a_escribir = i 
                data_aux.append(valor_a_escribir)  

                i_aux = i.split('_')
                i_aux_2 = list(i_aux[0])
                
                # Ventanas
                if 'BC' in i:
                    valor_a_escribir = 1
                else:
                    if i_aux_2[1] == str(1):
                        valor_a_escribir = 1
                    else:
                        valor_a_escribir = 2

                data_aux.append(valor_a_escribir)
                
                # Convencional/Eco
                if 'BC' in i:
                    valor_a_escribir = 0
                else:
                    if i_aux_2[2] == str(1):
                        valor_a_escribir = 1
                    else:
                        valor_a_escribir = 2
                data_aux.append(valor_a_escribir)
             
                # Opción
                if 'BC' in i:
                    valor_a_escribir = 0
                else:
                    valor_a_escribir = i_aux_2[3]
                data_aux.append(valor_a_escribir) 
               
                # Espesor (W)
                if 'BC' in i:
                    valor_a_escribir = 0
                else:
                    valor_a_escribir = i_aux[2]
                data_aux.append(valor_a_escribir) 
 
                # Espesor (R)
                if 'BC' in i:
                    valor_a_escribir = 0
                else:
                    valor_a_escribir = i_aux[3]
                data_aux.append(valor_a_escribir)


                # Orientación 
                valor_a_escribir = i_aux[1]
                data_aux.append(valor_a_escribir)
  

                # Instalaciones

                if 'Split_rf' in j:
                    valor_a_escribir = 1
                    data_aux.append(valor_a_escribir)

                if 'Split_nrf' in j: 
                    valor_a_escribir = 0
                    data_aux.append(valor_a_escribir)

                if 'PV_yes'in j:
                    valor_a_escribir = 1
                    data_aux.append(valor_a_escribir)

                if 'PV_no' in j:
                    valor_a_escribir = 0
                    data_aux.append(valor_a_escribir)

                if 'BC_yes' in j:
                    valor_a_escribir = 1
                    data_aux.append(valor_a_escribir)

                if 'BC_no' in j: 
                    valor_a_escribir = 0
                    data_aux.append(valor_a_escribir)
    
                  
                # Investment
                valor_a_escribir = buildingCost_active[i][j][ref_cat_analysis]['building_total_VAT']
                data_aux.append(valor_a_escribir)

                 
                # EPNR
                valor_a_escribir = output_scenarios_PE[i][j]
                data_aux.append(valor_a_escribir)

                
                # P_ht
                valor_a_escribir = P_ht[i]
                data_aux.append(valor_a_escribir)

                
                # P_ht
                valor_a_escribir = P_cl[i]
                data_aux.append(valor_a_escribir)
                  
                
                # P_dhw
                valor_a_escribir = P_dhw[i]
                data_aux.append(valor_a_escribir)
                
                # PE_ht
                valor_a_escribir = PE_ht[i]
                data_aux.append(valor_a_escribir)
     
                
                # PE_ht
                valor_a_escribir = PE_cl[i]
                data_aux.append(valor_a_escribir)
   
                
                # PE_dhw
                valor_a_escribir = PE_dhw[i]
                data_aux.append(valor_a_escribir)
                               
                # deltaEPNR_active
                valor_a_escribir = deltaEPNR_active[i][j]
                data_aux.append(valor_a_escribir)                

                myData.append(data_aux)
        writer.writerows(myData)

    return myData    

myData = excel_curva(output_scenarios_PE, buildingCost_active, P_ht_mean, P_cl_mean, P_dhw_mean, PE_ht_mean, PE_cl_mean, PE_dhw_mean, deltaEPNR_active)                


# %% Global cost

"""
Cálculo de cotes globales por vivienda:
    1) Se han supuesto unas inversiones de la parte activa según precio de mercado
    2) El coste de mantenimiento se propone 3%, según CYPE
    3) Coste de replacement según instalación -> bombas de calor y placas fotovoltaicas 1 vez. Inversor 4 veces
"""

years = 50
n_dwellings = list(buildingCost_active[list(buildingCost_active.keys())[-1]]['Split_rf+PV_yes+BC_yes'].values())[0]['nDwellings']


Investment_BCMULTI = (list(buildingCost_active[list(buildingCost_active.keys())[-1]]['Split_rf+PV_yes+BC_yes'].values())[0]['facilities_HVAC_PEC'])/n_dwellings
Investment_PV = (list(buildingCost_active[list(buildingCost_active.keys())[-1]]['Split_rf+PV_yes+BC_yes'].values())[0]['facilities_PV_PEC'])/n_dwellings
Investment_BCDHW = (list(buildingCost_active[list(buildingCost_active.keys())[-1]]['Split_rf+PV_yes+BC_yes'].values())[0]['facilities_DHW_PEC'])/n_dwellings

maintance_perc = 0.03

Maintenance_BCMULTI = Investment_BCMULTI*maintance_perc
Maintenance_PV = Investment_PV*maintance_perc
Maintenance_BCDHW = Investment_BCDHW*maintance_perc

Replacement_BCMULTI = Investment_BCMULTI/years
Replacement_PV = Investment_PV/years + (Investment_PV*n_dwellings*0.1*4)/years
Replacement_BCDHW = Investment_BCDHW/years

Investment_inst = [Investment_PV, Investment_BCDHW, Investment_BCMULTI]
Maintenance_inst = [Maintenance_PV, Maintenance_BCDHW, Maintenance_BCMULTI]
Replacement_inst = [Replacement_PV, Replacement_BCDHW, Replacement_BCMULTI]

precio_ele = 0.23     # €/kWh 
precio_gas = 0.10    # €/kWh
precio_butano = 0.13  # €/kWh
degradacion_inst_i = 0.005  # 0.5 % anual
tasa_inflacion_i = 0.01   # 1% anual

Maintenance_BC = [0, 100, Maintenance_BCMULTI]
Replacement_BC = [0, 1764/years, 3000/years]




project = globalCostScenarios.globalCost_ARV(output_scenarios_cons, precio_ele, precio_gas, precio_butano, degradacion_inst_i, tasa_inflacion_i, years, surface)
globalARV = globalCostScenarios.calculo(project, Maintenance_BC, Replacement_BC, Maintenance_inst, Replacement_inst, PV_estimation)
energyCost, maintenanceCost, replaceCost = globalARV.start()














