def Sumfloors(P_ht, P_cl, P_lig, P_dev, P_dhw):
    kwargs = {
        'P_ht': P_ht,
        'P_cl': P_cl,
        'P_lig': P_lig,
        'P_dev': P_dev,
        'P_dhw': P_dhw
    }

    output = {}

    for key, value in kwargs.items():
        simulations = set([k.rsplit("_", 1)[0] for k in value.keys()])
        summed_results = {}
        for sim in simulations:
            relevant_columns = [col for col in value.keys() if col.startswith(sim)]
            summed_value = 0
            for col in relevant_columns:
                val = value[col]
                if isinstance(val, list):
                    summed_value += sum(val)
                elif isinstance(val, (int, float)):
                    summed_value += val
                else:
                    raise TypeError(f"Unsupported data type: {type(val)}")
            summed_results[sim] = summed_value
        output[key] = summed_results

    return output['P_ht'], output['P_cl'], output['P_lig'], output['P_dev'], output['P_dhw']