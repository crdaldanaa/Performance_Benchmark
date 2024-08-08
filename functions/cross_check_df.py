import pandas as pd
import numpy as np


def check_df(df_project, df_control):
    def names_si(df):
        # Inicializar el diccionario vacío
        header_dict = {}
        covars = []

        # Recorrer los nombres de los encabezados del DataFrame
        for header in df.columns:
            if header.lower() == 'id':
                id_name = header
                continue
            elif '_' in header:
                parts = header.split('_', 1)  # Dividir en dos partes
                print(parts)
                year = int('20'+parts[1])
                header_dict[header] = year
                covars.append(header)
            else:
                covars.append(header)

        # print(f'\n***Información del Dataframe {name_df}***')
        # print(f'Nombres de las Columnas que son covariables:\n{covars}\n')

        # print("##Información de las columnas Stocking Index")
        # print(f'Se tiene un total de datos de {
        #      len(header_dict)} años para el Performance Benchmark')
        # for key, values in header_dict.items():
        #    print(f'La columna {key} corresponde al año {values}')

        header_dict = dict(sorted(header_dict.items()))

        return covars, header_dict, id_name

    name_df_control = "Control Plots"
    name_df_project = "Project Plots"

    strs_project, dict_project, id_project = names_si(df_project)
    strs_control, dict_control, id_control = names_si(df_control)

    def compare_dicts(dict1, dict2):
        var = 0
        val_compare = 0
        for i in dict1.keys():
            if i in dict2.keys():
                val_compare += 1

        if len(dict1.items()) == val_compare and len(dict1.items()) == len(dict2.items()):
            # print("Los diccionarios son iguales.")
            var = 1
            return var
        else:
            # print("Los diccionarios no son iguales.")
            var = 0
            keys1 = set(dict1.keys())
            keys2 = set(dict2.keys())

            diff_keys_in_dict1 = keys1 - keys2
            diff_keys_in_dict2 = keys2 - keys1
            return var, diff_keys_in_dict1, diff_keys_in_dict2

    def compare_strings(str1, str2):
        var = 0
        val_compare = 0
        for i in str1:
            if i in str2:
                val_compare += 1

        if len(str1) == val_compare and len(str1) == len(str2):
            # print("Las covariables son iguales")
            var = 1
            return var
        else:
            # print("Las cadenas no son iguales.")
            var = 0
            return var

    def no_null_data(df, name_df):
        print(f'Revisando y limpiando los valores nulos del dataframe {
            name_df}')
        df = df.dropna(how='any')
        df = df.reset_index(drop=True)
        print(f'El dataframe {name_df} ha sido limpiado con éxito')
        return df

    if type(compare_dicts(dict_control, dict_project)) == tuple:
        dif_dicts = compare_dicts(dict_control, dict_project)
        dif_dicts = dif_dicts[0]

    else:
        dif_dicts = compare_dicts(dict_control, dict_project)

    if compare_strings(strs_control, strs_project) == 0:
        if dif_dicts == 0:
            dif_dicts, missing_control, missing_project = compare_dicts(
                dict_control, dict_project)
            if missing_project != 0:
                print(f'En el dataframe {
                    name_df_control} no se encuentran las siguientes columnas: ')
                for i in missing_project:
                    no = 1
                    print(f'{no}. {i}')
                    no += 1

            elif missing_control != 0:
                print(f'\nEn el dataframe {
                    name_df_project} no se encuentran las siguientes columnas: ')
                print(len(missing_control))
                for i in missing_control:
                    no = 1
                    print(f'{no}. {i}')
                    no += 1

            print(f'\nPor favor revise y verifique que cada una de las columnas de los dataframes tengan los mismos nombres')
            response = True

        else:
            print(f'\nSe presentan diferencias entre las covariables los dos datasets de entrada ({name_df_control}, {
                  name_df_project}).\nPor favor revise y verifique que cada una de las columnas de los dataframes tengan los mismos nombres')
            response = True
    else:
        print("Verificación de datasets completada.")
        response = False

        df_control = no_null_data(df_control, name_df_control)
        df_control['Type'] = "Control"
        df_project = no_null_data(df_project, name_df_project)
        df_project['Type'] = "Project"
        df_control = df_control.astype(
            {col: 'float32' for col in df_control.select_dtypes(include=['float64']).columns})
        df_project = df_project.astype(
            {col: 'float32' for col in df_project.select_dtypes(include=['float64']).columns})

        # print(df_project)
        # print(df_control)

    return response, df_control, df_project, strs_project, dict_project, id_project


if __name__ == '__main__':
    df_control = pd.DataFrame({
        'ID': [1, 2, 3],
        'year_10': [4.1, 5.2, 3.3],
        'year_15': [4.2, 5.3, 3.4],
        'year_20': [4.5, np.nan, 3.5],
        'Slope': [25, 30, 42]
    })

    df_project = pd.DataFrame({
        'ID': [1, 2, 3],
        'year_10': [4.2, 5.3, 3.4],
        'year_15': [4.1, 5.2, 3.3],
        'year_20': [np.nan, 5.4, 3.5],
        'Slope': [25, 30, 42],
    })

    response, df_control, df_project, strs_project, dict_project, id_project = check_df(
        df_project, df_control)

    print(df_control)
