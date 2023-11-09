import pandas as pd

from interactors import analysisActive,  analysisTRNSYS, executionCost, executionCost
from repositories import csvTRNSYS
from utils import meanCalculation, energyScenarios
from SQL_statements import database_connection, getSurfacesTemp
from sqlalchemy import text
from repositories import csvTRNSYS, CMH
from utils import mean_calculation2


n_viv = 1
name = 'FE35'
refcat = '1701521DD7810B'






import pickle

# Specify the path to your PKL file
file_path = "C:/arxius/PV_estimation.pkl"

# Open the file in read-binary mode
with open(file_path, 'rb') as file:
    # Load the data from the file
    PV_estimation = pickle.load(file)



analysisType = analysisTRNSYS2.energyAnalysis(n_viv, name, refcat)
data = analysisTRNSYS2.do_analysis(analysisType)
P_ht, P_cl, P_lig, P_dev, P_dhw, PE_ht, PE_cl, PE_lig,PE_dev ,PE_dhw, CO2_ht, CO2_cl, CO2_lig, CO2_dev, CO2_dhw = data.start()


grado_ht = {'joule':0,'BC':1,'caldera_GN':0,'butano':0,'nada':0}
grado_cl = {'split':0,'BC':0,'multi_split':1,'nada':0}
grado_dhw ={'caldera_GN':0,'butano':0,'BC':1}



project = analysisActive.ARV_CO2_PE(P_cl, P_ht, P_lig, P_dev, P_dhw)
activeAnalysis = analysisActive.do_analysis(project, grado_ht, grado_cl, grado_dhw)
PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt , PE_dhw_rt, CO2_ht_rt, CO2_cl_rt, CO2_lig_rt, CO2_dev_rt, CO2_dhw_rt = activeAnalysis.start()


output = energyScenarios2.ARV_Scenarios()
PE_scenarios = energyScenarios2.calculo(output, PE_ht, PE_cl, PE_lig, PE_dev, PE_dhw, PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt, PE_dhw_rt, PV_estimation, name)
output_scenarios_PE = PE_scenarios.start()

output_scenarios = output_scenarios_PE

engine = database_connection.engine
Arquetipo = 'FE35'
with open('SQL_statements/materials.sql', 'r') as file:
    materials_query = file.read()

        # Execute the query with the parcela variable
with engine.connect() as connection:
    query = text(materials_query)
    materials = pd.read_sql_query(query, connection, params={"Arquetipo":Arquetipo })


buildingCost = {}
for config in output_scenarios:
    if not config.startswith('BC0'):

            wall_type = config.split("_")[2]
            roof_type = config.split("_")[3]
            pattern = config.split("_")[0]
            conv_eco = int(pattern[2])
            material = int(pattern[3])
            cost_wall = materials.loc[(materials['tipus'] == 'mur') & (materials['espesor'] == wall_type) & (materials['convecional_eco'] == int(pattern[2])) & (materials['opcion'] == int(pattern[3]))]['cost'].iloc[0]
            cost_roof = materials.loc[(materials['tipus'] == 'coberta') & (materials['espesor'] == roof_type) & (materials['convecional_eco'] == int(pattern[2])) & (materials['opcion'] == int(pattern[3]))]['cost']
            buildingCost[config] = {'wall_type': wall_type, 'roof_type': roof_type, 'pattern': pattern,'conv_eco': conv_eco, 'material': material, 'cost_wall': cost_wall, 'cost_roof': cost_roof }



pd.DataFrame(buildingCost).T.to_csv("C:/arxius/comprovacio2.csv")