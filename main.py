
import time
from SQL_statements import database_connection, getSurfacesTemp
from utils import meanCalculation, energyConsumption, energyScenarios, print_results
from interactors import analysisTRNSYS, analysisActive, investmentActiveARV
import os
import sys

direct = os.getcwd()
sys.path[0] = direct
# arguments


def main( name, n_viv,refcat):



    engine = database_connection.engine
    data_processor = getSurfacesTemp.DataProcessor(engine)
    areabyCadastralcode, distributionRatio, ref_use = data_processor.get_data(refcat)
    area = [((areabyCadastralcode[refcat]['roof']*0.25)*0.8)/len(distributionRatio[refcat])]

    analysisType = analysisTRNSYS.energyAnalysis(n_viv, name, refcat)
    data = analysisTRNSYS.do_analysis(analysisType)
    P_ht, P_cl, P_lig, P_dev, P_dhw, PE_ht, PE_cl, PE_lig,PE_dev ,PE_dhw, CO2_ht, CO2_cl, CO2_lig, CO2_dev, CO2_dhw = data.start()


    project = meanCalculation.ARV_dwellings() # Las medias de energía primaria se utilizan para calcular las subvenciones
    output = meanCalculation.calculo(project, P_ht, P_cl, P_lig,P_dev, P_dhw, name)
    P_ht_mean, P_cl_mean, P_lig_mean,P_dev_mean ,P_dhw_mean = output.start()


    project = meanCalculation.ARV_dwellings() # Las medias de energía primaria se utilizan para calcular las subvenciones
    output = meanCalculation.calculo(project, PE_ht, PE_cl, PE_lig,PE_dev, PE_dhw, name)
    PE_ht_mean, PE_cl_mean, PE_lig_mean,PE_dev_mean ,PE_dhw_mean = output.start()





    grado_ht = {'joule':0,'BC':1,'caldera_GN':0,'butano':0,'nada':0}
    grado_cl = {'split':0,'BC':0,'multi_split':1,'nada':0}
    grado_dhw ={'caldera_GN':0,'butano':0,'BC':1, 'joule':0}



    project = analysisActive.ARV_CO2_PE(P_cl, P_ht, P_lig, P_dev, P_dhw)
    activeAnalysis = analysisActive.do_analysis(project, grado_ht, grado_cl, grado_dhw)
    PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt , PE_dhw_rt, CO2_ht_rt, CO2_cl_rt, CO2_lig_rt, CO2_dev_rt, CO2_dhw_rt = activeAnalysis.start()


    grado_ht = {'joule': 0.35, 'BC': 0.28, 'caldera_GN': 0.15, 'butano': 0.15, 'nada': 0.07}
    grado_cl = {'split': 0.1, 'BC': 0.43, 'multi_split': 0.04, 'nada': 0.43}
    grado_dhw = {'caldera_GN': 0.64, 'butano': 0.1, 'BC': 0, 'joule': 0.26}


    output = energyConsumption.ARV_CONS(grado_ht, grado_cl, grado_dhw, area, name,  P_ht, P_cl, P_lig, P_dev, P_dhw)
    Cons_scenarios = energyConsumption.calculo(output, P_ht, P_cl, P_lig, P_dev, P_dhw,name)
    output_scenarios_cons, electricity, PV_estimation = Cons_scenarios.start()




    output = energyScenarios.ARV_Scenarios()
    PE_scenarios = energyScenarios.calculo(output, PE_ht, PE_cl, PE_lig, PE_dev, PE_dhw, PE_ht_rt, PE_cl_rt, PE_lig_rt, PE_dev_rt, PE_dhw_rt, PV_estimation, name)
    output_scenarios_PE = PE_scenarios.start()



    project = investmentActiveARV.investmentActive_ARV(output_scenarios_PE, refcat, name)
    investmentAct = investmentActiveARV.calculation(project)
    buildingCost_active, dwellingCost_active, dwellings_fees_active, buildingGrants_active, deltaEPNR_active = investmentAct.start()

    myData =  print_results.print_excel(output_scenarios_PE, buildingCost_active, P_ht_mean, P_cl_mean, P_dhw_mean, PE_ht_mean,PE_cl_mean, PE_dhw_mean, deltaEPNR_active, name, refcat)


    return myData

if __name__ == '__main__':
    start_time = time.time()
    main('FE35', 1, '1701521DD7810B')
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time} seconds")



