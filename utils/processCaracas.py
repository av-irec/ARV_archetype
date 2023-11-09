import pandas as pd
from sqlalchemy import text
from  SQL_statements import database_connection

def process_caracas(ref_cat, P_ht, P_cl, P_lig, P_dev, P_dhw):
    kwargs = {
        'P_ht': P_ht,
        'P_cl': P_cl,
        'P_lig': P_lig,
        'P_dev': P_dev,
        'P_dhw': P_dhw
    }
    output = {}
    for key, vector in kwargs.items():
        escenarios = []
        for i in vector.keys():
            if not i.startswith('BC0') and 'R0' not in i.rsplit("_", 2)[1]:
                escenarios.append(i.rsplit("_", 1)[0])

        for scenario in escenarios:
            key_BF = scenario + "_BF"
            key_IF = scenario + "_IF"
            if key_BF not in vector:
                vector[key_BF] = vector[scenario.rsplit("_", 1)[0] + "_R0" + "_BF"]
            if key_IF not in vector:
                vector[key_IF] = vector[scenario.rsplit("_", 1)[0] + "_R0" + "_IF"]

        dicto = {key: value for key, value in vector.items() if 'R0' not in key}

        engine = database_connection.engine
        with open('SQL_statements/group_storeys.sql', 'r') as file:
            group_storeys = file.read()
            # Execute the query with the parcela variable
        with engine.connect() as connection:
            query = text(group_storeys)
            group_storeys = pd.read_sql_query(query, connection, params={"parcela": ref_cat})

        total_floors = group_storeys[group_storeys['group_apt'] == 'IF']['count_plantes'].iloc[0]

        def multiply_list_elements(val):
            return [i * total_floors for i in val]

        dicto_df = pd.DataFrame(dicto)
        IF_floors = [col for col in dicto_df.columns if col.endswith('IF')]
        dicto_df[IF_floors] = dicto_df[IF_floors].applymap(multiply_list_elements)

        vector_calculated = dicto_df.to_dict()
        output[key] = vector_calculated

    return output['P_ht'], output['P_cl'], output['P_lig'], output['P_dev'], output['P_dhw']



