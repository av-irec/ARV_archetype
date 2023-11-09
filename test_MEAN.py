#%%
from repositories import csvTRNSYS
import pandas as pd
from SQL_statements import database_connection
from sqlalchemy import text
from utils import meanCalculation,mean_calculation2

n_viv_simulated = 3
building_to_analyse = 'Caracas1'
parcela = '1502002DD7810B'
typeStep = csvTRNSYS.HourlyMulti()
output = csvTRNSYS.readTRNSYS(typeStep, n_viv_simulated, building_to_analyse)
output_reader, P_ht, P_cl, P_lig, P_dev, P_dhw = output.start()



project = meanCalculation.ARV_dwellings() # Las medias de energía primaria se utilizan para calcular las subvenciones
output = meanCalculation.calculo(project,  P_ht, P_cl, P_lig, P_dev, P_dhw)
P_ht_mean, P_cl_mean, P_lig_mean,P_dev_mean ,P_dhw_mean = output.start()


project2 = mean_calculation2.ARV_dwellings() # Las medias de energía primaria se utilizan para calcular las subvenciones
output = mean_calculation2.calculo(project2,  P_ht, P_cl, P_lig, P_dev, P_dhw,parcela)
output1, output2, output3 = output.start()


print(P_ht_mean)
print(output1)





