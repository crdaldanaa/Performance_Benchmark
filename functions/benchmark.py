import pandas as pd


def performance_benchmark(df, df_lastest_cols, dict_z):
    def calculate_pb(column):
        grouped = df.groupby('Type')[column]
        means = grouped.mean()

        # Calcular el Ztest
        mean_1 = means['Project']
        mean_2 = means['Control']

        pb = (mean_2/mean_1)*100

        return pb

    values_pb = []

    aux = None

    for column in df_lastest_cols:
        first_part = column.split('_')[0]
        value = round(calculate_pb(column), 2)
        second_part = column.split('_')[1]
        if first_part == 't1':
            range = '0-' + second_part
        else:
            if aux is not None:
                range = str(int(aux) + 1) + '-' + \
                    str(int(aux)+int(second_part))
            else:
                range = '0-' + second_part

        aux = second_part

        values_pb.append([first_part, range, value])

    # Creamos el DataFrame final
    df_pb = pd.DataFrame(values_pb, columns=[
                         'Item', 'Years Range', 'Performance Benchmark %'])

    # Crear una copia de la column
    df_pb['PB Adjusted %'] = df_pb['Performance Benchmark %'].clip(lower=0)

    # Reemplazar valores negativos por cero en la copia
    sum_pb = df_pb['PB Adjusted %'].sum()

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
    df_pb = final_pb(df_pb, dict_z)

    # print(df_pb)
    return df_pb, sum_pb


if __name__ == '__main__':
    import pandas as pd
    from cross_check_df import *
    from matriz_distances import *
    from slope_years import *
    from weights import *
    from tests import z_column, sdm_column

    df_project = pd.DataFrame({
        'ID': ['P1', 'P2', 'P3'],
        'year_10': [0.0, 0.3, 0.2],
        'year_15': [0.2, 0.4, 0.3],
        'year_20': [0.5, 0.5, 0.5]
    })

    df_control_plots = pd.DataFrame({
        'ID': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'],
        'year_10': [0.5, 0.3, 0.2, 0.8, 1.0, 0.5, 1.0, 0.7, 0.8, 0.9],
        'year_15': [0.5, 0.3, 0.2, 0.6, 0.5, 0.4, 0.7, 0.7, 0.8, 0.5],
        'year_20': [0.5, 0.3, 0.2, 0.1, 0.4, 0.3, 0.5, 0.6, 0.8, 0.1]
    })

    response, df_control_plots, df_project_plots, strs_project, dict_project, id_name = check_df(
        df_project, df_control_plots)

    matrix_distances, assigned_plots, df_selected_plots = arrange_plots(
        df_project_plots, df_control_plots, strs_project, id_name, 1)

    """
    print(df_selected_plots)

    print(sdm_column(df_selected_plots))
    """

    df_selected_plots, n = slope_SI(df_selected_plots, dict_project)

    z_scores, max_ztest, df_lastest_columns = z_column(df_selected_plots, n)

    df_pb, max_pb = performance_benchmark(
        df_selected_plots, df_lastest_columns, z_scores)

    print(df_pb)
