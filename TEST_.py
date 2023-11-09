import pandas as pd

from interactors import analysisActive,  analysisTRNSYS, executionCost, executionCost, investmentActiveARV
from repositories import csvTRNSYS
from utils import meanCalculation, energyScenarios
from SQL_statements import database_connection, getSurfacesTemp
from sqlalchemy import text
from repositories import csvTRNSYS, CMH




n_viv = 1
name = 'FE35'
refcat = '1701521DD7810B'






import pickle




analysisType = analysisTRNSYS.energyAnalysis(n_viv, name, refcat)
data = analysisTRNSYS.do_analysis(analysisType)
P_ht, P_cl, P_lig, P_dev, P_dhw, PE_ht, PE_cl, PE_lig,PE_dev ,PE_dhw, CO2_ht, CO2_cl, CO2_lig, CO2_dev, CO2_dhw = data.start()


grado_ht = {'joule':0,'BC':1,'caldera_GN':0,'butano':0,'nada':0}
grado_cl = {'split':0,'BC':0,'multi_split':1,'nada':0}
grado_dhw ={'caldera_GN':0,'butano':0,'BC':1,'joule':0}



project = analysisActive.ARV_CO2_PE(P_cl, P_ht, P_lig, P_dev, P_dhw)
activeAnalysis = analysisActive.do_analysis(project, grado_ht, grado_cl, grado_dhw)
PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt , PE_dhw_rt, CO2_ht_rt, CO2_cl_rt, CO2_lig_rt, CO2_dev_rt, CO2_dhw_rt = activeAnalysis.start()

# Specify the path to your PKL file
file_path = "C:/arxius/fe35/PV_estimation.pkl"

# Open the file in read-binary mode
with open(file_path, 'rb') as file:
    # Load the data from the file
    PV_estimation = pickle.load(file)

output = energyScenarios.ARV_Scenarios()
PE_scenarios = energyScenarios.calculo(output, PE_ht, PE_cl, PE_lig, PE_dev, PE_dhw, PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt, PE_dhw_rt, PV_estimation, name)
output_scenarios_PE = PE_scenarios.start()



project = investmentActiveARV.investmentActive_ARV(output_scenarios_PE, refcat, name)
investmentAct = investmentActiveARV.calculation(project)
buildingCost_active, dwellingCost_active, dwellings_fees_active, buildingGrants_active, deltaEPNR_active = investmentAct.start()









