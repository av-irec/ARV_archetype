# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:51:06 2022

@author: srabadan
"""

from abc import ABC, abstractmethod


class selectedOutput(ABC):
    """
    Parameters:

        grado_ht (dict) -- Repartición de instalaciones para la demanda de calefacción
        grado_cl (dict) -- Repartición de instalaciones para la demanda de refrigeración
        grado_dhw (dict) -- Repartición de instalaciones para la demanda de agua caliente sanitaria
        coef_CO2 (float) -- Coeficientes de consumo a CO2 (electricidad/gas natural/butano)
        coef_NRPE (float) -- Coeficientes de consumo a energía primaria (electricidad/gas natural/butano)
    """
    def __init__(self, grado_ht, grado_cl, grado_dhw, coef_CO2, coef_NRPE):
        self.grado_ht = grado_ht
        self.grado_cl = grado_cl
        self.grado_dhw = grado_dhw
        self.coef_CO2 = coef_CO2
        self.coef_NRPE = coef_NRPE

    @abstractmethod
    def calculation():
        pass


class pE_ARV_demand(selectedOutput):
    """
    Los coeficientes de paso están predefinidos a los de península. Si se quieren cambiar se debe indicar en la instancia de la clase
    """
    def __init__(self, grado_ht, grado_cl, grado_dhw, coef_CO2={'ele': 0.331, 'GN': 0.252, 'butano': 0.254}, coef_NRPE={'ele': 2.968, 'GN': 1.190, 'butano': 1.201}):
        super().__init__(grado_ht, grado_cl,grado_dhw, coef_CO2, coef_NRPE)

    def calculation(self, P_ht, P_cl, P_lig, P_dev, P_dhw, EER = 2, COP=2, COP_DHW=1.7, eta_cal=0.7):
        """
        Inputs:

            P_ht (dict) -- Demanda de calefacción
            P_cl (dict) -- Demanda de refrigeración
            P_lig (dict) -- Demanda de iluminación
            P_dev (dict) -- Demanda de electrodomésticos
            P_dhw (dict) -- Demanda de agua caliente sanitaria
            EER (float) -- Eficiencia en refrigeración (prefinido a 2 -> CE3X)
            COP (float) -- Eficiencia en calefacción (prefinido a 2 -> CE3X)
            COP_DHW (float) -- Eficiencia en agua caliente sanitaria con bomba de calor (prefinidos a 1.7)
            eta_cal (float) -- Eficiencia caldera gas natural o butano (prefinidos a 70% -> Optihub)

        """


        COP_C3X = 2
        PE_ht = {}
        PE_cl = {}
        PE_lig = {}
        PE_dev = {}
        PE_dhw = {}

        # Los ouputs de esta clase tendrán la misma configuración que los inputs (PE_ht será un diccionario con la misma configuración que P_ht)
        for i in P_ht:
            PE_ht.setdefault(i, [])
            PE_cl.setdefault(i, [])
            PE_lig.setdefault(i, [])
            PE_dev.setdefault(i, [])
            PE_dhw.setdefault(i, [])
            count = 0
            for j in range(0, len(P_ht[i])):

                # Se multiplica la demanda (P_ht) por las opciones de según distribución (grado_ht) y por la eficiencia correspondiente (COP / eta_cal)

                PE_ht[i].append(P_ht[i][count]*(((self.grado_ht['joule']+(self.grado_ht['BC'])/COP)*self.coef_NRPE['ele'])+((self.grado_ht['caldera_GN']+self.grado_ht['nada'])/eta_cal*self.coef_NRPE['GN'])+(self.grado_ht['butano']/eta_cal*self.coef_NRPE['butano'])))
                PE_cl[i].append(P_cl[i][count]*(((self.grado_cl['split']+self.grado_cl['BC'] +self.grado_cl['multi_split'])/EER+self.grado_cl['nada']/COP_C3X)*self.coef_NRPE['ele']))
                PE_lig[i].append(P_lig[i][count]*self.coef_NRPE['ele'])
                PE_dev[i].append(P_dev[i][count]*self.coef_NRPE['ele'])
                PE_dhw[i].append(P_dhw[i][count]*((self.grado_dhw['caldera_GN']/eta_cal*self.coef_NRPE['GN'])+(self.grado_dhw['butano']/eta_cal*self.coef_NRPE['butano'])+(self.grado_dhw['BC']/COP_DHW*self.coef_NRPE['ele'])+(self.grado_dhw['joule']/1 * self.coef_NRPE['ele'])))
                count = count + 1

        return PE_ht, PE_cl, PE_lig, PE_dev, PE_dhw

class CO2_ARV_demand(selectedOutput):
    """
    Los coeficientes de paso están predefinidos a los de península. Si se quieren cambiar se debe indicar en la instancia de la clase
    """
    def __init__(self, grado_ht, grado_cl, grado_dhw, coef_CO2={'ele': 0.331, 'GN': 0.252, 'butano': 0.254},coef_NRPE={'ele': 2.937, 'GN': 1.190, 'butano': 1.201}):
        super().__init__(grado_ht, grado_cl, grado_dhw, coef_CO2, coef_NRPE)
    def calculation(self, P_ht, P_cl, P_lig, P_dev, P_dhw, EER = 2, COP=2, COP_DHW=1.7, eta_cal=0.7):
        """
        Inputs:

            P_ht (dict) -- Demanda de calefacción
            P_cl (dict) -- Demanda de refrigeración
            P_lig (dict) -- Demanda de iluminación
            P_dev (dict) -- Demanda de electrodomésticos
            P_dhw (dict) -- Demanda de agua caliente sanitaria
            EER (float) -- Eficiencia en refrigeración (prefinido a 2 -> CE3X)
            COP (float) -- Eficiencia en calefacción (prefinido a 2 -> CE3X)
            COP_DHW (float) -- Eficiencia en agua caliente sanitaria con bomba de calor (prefinidos a 1.7)
            eta_cal (float) -- Eficiencia caldera gas natural o butano (prefinidos a 70% -> Optihub)

        """
        COP_C3X = 2
        CO2_ht = {}
        CO2_cl = {}
        CO2_lig = {}
        CO2_dev = {}
        CO2_dhw = {}

        # Los ouputs de esta clase tendrán la misma configuración que los inputs (CO2_ht será un diccionario con la misma configuración que P_ht)

        for i in P_ht:
            CO2_ht.setdefault(i, [])
            CO2_cl.setdefault(i, [])
            CO2_lig.setdefault(i, [])
            CO2_dev.setdefault(i, [])
            CO2_dhw.setdefault(i, [])
            count = 0
            for j in range(0, len(P_ht[i])):

                # Se multiplica la demanda (P_ht) por las opciones de según distribución (grado_ht) y por la eficiencia correspondiente (COP / eta_cal)

                CO2_ht[i].append(P_ht[i][count]*(((self.grado_ht['joule']+(self.grado_ht['BC'])/COP)*self.coef_CO2['ele'])+(
                    (self.grado_ht['caldera_GN']+self.grado_ht['nada'])/eta_cal*self.coef_CO2['GN'])+(self.grado_ht['butano']/eta_cal*self.coef_CO2['butano'])))
                CO2_cl[i].append(P_cl[i][count]*(((self.grado_cl['split']+self.grado_cl['BC'] +
                                self.grado_cl['multi_split'])/EER+self.grado_cl['nada']/COP_C3X)*self.coef_CO2['ele']))
                CO2_lig[i].append(P_lig[i][count]*self.coef_CO2['ele'])
                CO2_dev[i].append(P_dev[i][count]*self.coef_CO2['ele'])
                CO2_dhw[i].append(P_dhw[i][count]*((self.grado_dhw['caldera_GN']/eta_cal*self.coef_CO2['GN'])+(
                    self.grado_dhw['butano']/eta_cal*self.coef_CO2['butano'])+(self.grado_dhw['BC']/COP_DHW*self.coef_CO2['ele'])+(self.grado_dhw['joule']/1 * self.coef_NRPE['ele'])))
                count = count + 1
        return CO2_ht, CO2_cl, CO2_lig, CO2_dev, CO2_dhw

#

class calculo:
    def __init__(self, project: selectedOutput, P_ht, P_cl, P_lig, P_dev, P_dhw, EER = 2, COP=2, COP_dhw=1.7, eta_cal=0.7):
        self.project = project
        self.P_ht = P_ht
        self.P_cl = P_cl
        self.P_lig = P_lig
        self.P_dev = P_dev
        self.P_dhw = P_dhw
        self.EER = EER
        self.COP = COP
        self.COP_dhw = COP_dhw
        self.eta_cal = eta_cal

    def start(self):
        return self.project.calculation(self.P_ht, self.P_cl, self.P_lig, self.P_dev, self.P_dhw, self.EER, self.COP, self.COP_dhw, self.eta_cal)
