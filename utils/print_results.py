import csv

def print_excel(output_scenarios_PE, buildingCost_active, P_ht, P_cl, P_dhw, PE_ht, PE_cl, PE_dhw, deltaEPNR_active,name, refcat):

    ruta_csv = 'Tabla_excel_' + name + '.csv'
    with open(ruta_csv, 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        myData = []
        writer.writerow(
            ['Caso', 'Ventanas', 'Convecional/Eco', 'Opcion', 'Espesor (W)', 'Espesor (R)', 'Orientacion', 'Msplit',
             'PV', 'BC', 'Investment', 'EPNR', 'P_ht', 'P_cl', 'P_dhw', 'PE_ht', 'PE_cl', 'PE_dhw', 'deltaEPNR_active',
             ''])
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

                if 'PV_yes' in j:
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
                valor_a_escribir = buildingCost_active[i][j][refcat]['building_total_VAT']
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