import numpy as np
from numba import njit


def sdm_column(df, str_covars):
    def calculate_sdm(column):
        grouped = df.groupby('Type')[column]
        means = grouped.mean()
        stds = grouped.std()

        # Calcular la Standardized Difference of Means (SDM)
        mean_1 = means['Project']
        mean_2 = means['Control']
        std_1 = stds['Project']
        std_2 = stds['Control']

        sdm = float(round(abs(mean_1 - mean_2) /
                    np.sqrt((std_1**2 + std_2**2) / 2), 2))
        return sdm

    sdm_dict = {}

    covars_cols = df[str_covars]
    for column in covars_cols:
        sdm_dict[column] = calculate_sdm(column)

    max_sdm = max(sdm_dict.values())

    return sdm_dict, max_sdm


def z_column(df, n):
    def calculate_ztest(column):
        grouped = df.groupby('Type')[column]
        means = grouped.mean()
        stds = grouped.std()
        counts = grouped.count()

        # Calcular el Ztest
        mean_1 = means['Project']
        mean_2 = means['Control']
        std_1 = stds['Project']
        std_2 = stds['Control']
        n_1 = counts['Project']
        n_2 = counts['Control']

        se = np.sqrt((std_1**2 / n_1) + (std_2**2 / n_2))

        ztest = float(round(abs((mean_1 - mean_2) / se), 2))

        return ztest

    # Seleccionar las n últimas columnas del DataFrame
    lastest_columns = df.columns[-n:]

    # Aplicar la función a las dos últimas columnas
    z_scores = {}
    for column in lastest_columns:
        z_scores[column] = calculate_ztest(column)

    max_ztest = min(z_scores.values())

    def final_pb(df, dict):
        def get_value(row, data_dict):
            key_prefix = row['Item']  # Obtener la primera parte de la clave
            for key, value in data_dict.items():
                # Verifica si la clave comienza con el prefijo
                if key.startswith(f"{key_prefix}_"):
                    return value
            return None  # Retorna None si no se encuentra coincidencia

        # Crear una nueva columna en el DataFrame con los valores del diccionario
        df['Z_Value'] = df.apply(get_value, data_dict=dict, axis=1)
        return df

    # print(z_scores)
    return z_scores, max_ztest, lastest_columns


if __name__ == '__main__':
    import pandas as pd
    from cross_check_df import *
    from matriz_distances import *
    from slope_years import *
    from weights import *

    df_project = pd.DataFrame({
        'ID': [1, 2, 3],
        'year_10': [4.5, 5.3, 3.4],
        'year_15': [4.1, 5.2, 3.3],
        'year_20': [4.0, 5.4, 3.5]
    })

    df_control_plots = pd.DataFrame({
        'ID': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'],
        'year_10': [4.1, 5.2, 3.3, 3.5, 1.0, 8.5, 5.2, 7.5, 8.4, 6.1],
        'year_20': [4.7, 5.4, 3.5, 1.6, 2.5, 6.6, 7.7, 8.2, 3.4, 2.5],
        'year_15': [4.2, 5.3, 3.4, 2.1, 2.4, 2.5, 5.5, 6.6, 7.7, 4.1]
    })

    response, df_control_plots, df_project_plots, strs_project, dict_project, id_name = check_df(
        df_project, df_control_plots)

    matrix_distances, assigned_plots, df_selected_plots = arrange_plots(
        df_project_plots, df_control_plots, strs_project, id_name, 2)

    dict, value = sdm_column(df_selected_plots)

    print(value)

    df_selected_plots, n = slope_SI(df_selected_plots, dict_project)

    dict_z, max_z, lastest_df = z_column(df_selected_plots, n)

    print(dict_z)
    print(max_z)
