# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:23:34 2022

@author: srabadan
"""

# Abstract method import

from abc import ABC, abstractmethod


# Resources

from repositories import dataDISConsumption, repositoryComercializadora, csvTRNSYS
from utils import filterComercializadora, meanCalculation


# Abstract class

class currencyType(ABC):
    @abstractmethod
    def dataSource(self):
        pass


class dataDIS(currencyType):
    def dataSource(self):
        import pandas as pd
        typeFile = dataDISConsumption.multi_annually()
        data_consumption = dataDISConsumption.get_data(typeFile)
        data_Ddis, data_eur = data_consumption.start()
        data_eur = data_eur.head(-1)
        data_out = {}

        for i in data_Ddis:
            data_Ddis[str(i)] = data_Ddis[str(i)].reset_index()
            data_Ddis[str(i)].columns = data_Ddis[str(i)].columns.str.replace(
                'timeDiscrimination', 'timeDis')
            data_Ddis[str(i)].columns = data_Ddis[str(i)].columns.str.replace(
                'economicSector', 'econoSector')
            t = []
            for j in data_Ddis[str(i)]:
                if 'mi' in j:
                    t.append(j)
            t.pop()
            data_out[str(i)] = pd.DataFrame()
            data_out[str(i)]['Med'] = 1
            count = 0
            count_2 = 0
            n_row = 0
            for label, content in data_Ddis[str(i)].iterrows():
                for index, value in content.items():
                    if index in t:
                        data_out[str(i)].loc[count, 'Med'] = value / \
                            (data_Ddis[str(i)].loc[n_row, 'sumContracts'])
                        count = count + 1
                        count_2 = count_2 + 1
                        if count_2 == 24:
                            n_row = n_row + 1
                            count_2 = 0
            time_start = str(i) + '-01-01 00:00'
            data_out[str(i)].index = [pd.Timestamp(time_start) +
                                      pd.Timedelta(hours=i) for i in data_out[str(i)].index]
        data_out['Eur'] = data_eur.Eur

        return data_out


class TRNSYS(currencyType):  
    def dataSource(self):
        pass

    
class dataComercializadora(currencyType):
    def dataSource(self):
        import pandas as pd
        typeFile = repositoryComercializadora.multiCSV()
        data_consumption = repositoryComercializadora.get_data(typeFile)
        type_output = filterComercializadora.dataframe()
        data_out_df, data_eur = data_consumption.start()
        data_eur = data_eur.head(-1)

        data_out = {}
        for key in data_out_df:
            for i in range(0, len(data_out_df[key])):
                if str(data_out_df[key].AE_kWh[i]) != 'nan':
                    data_out_df[key].AE_kWh[i] = str(data_out_df[key].AE_kWh[i]).replace(',', '.')
            filter_C = filterComercializadora.calculo(type_output, data_out_df[key])
            data_out_df[key] = filter_C.start()
            data_out.setdefault(key,{})
            data_out_df[key] = data_out_df[key].rename(columns={'AE_kWh' : 'Med'})
            data_out[key].setdefault(data_out_df[key].index[100].strftime("%Y"),pd.to_numeric(data_out_df[key].Med).to_frame())
            
        data_eur.squeeze() 
        data_out.setdefault('Eur',data_eur.Eur)
        

            
        return data_out


class TRNSYS(currencyType):
    def dataSource(self):
        pass


class get_data:
    def __init__(self, typeFile: currencyType):
        self.typeFile = typeFile

    def start(self):
        return self.typeFile.dataSource()


if __name__ == '__main__':
    typeFile = TRNSYS()
    output = get_data(typeFile)
    output_reader, P_ht, P_cl, P_lig, P_dev, P_dhw = output.start()
