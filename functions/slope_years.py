from numba import njit


def slope_SI(df, dict):
    # Recorrer las claves del diccionario
    keys = list(dict.keys())
    t = 1
    for i in range(len(keys) - 1):
        key_0 = keys[i]
        key_1 = keys[i + 1]

        # Calcular la nueva columna
        diff = (dict[key_1] - dict[key_0])
        new_col_name = f't{t}_{diff}'
        df[new_col_name] = df.apply(
            lambda row: (row[key_1] - row[key_0]) / diff,
            axis=1
        )
        t += 1

    t -= 1

    return df, t


if __name__ == '__main__':
    import pandas as pd
    from cross_check_df import *
    from matriz_distances import *
    from slope_years import *
    from weights import *

    df_project = pd.DataFrame({
        'ID': [1, 2, 3],
        'year_10': [4.2, 5.3, 3.4],
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

    weights(assigned_plots)

    slope_SI(df_selected_plots, dict_project)
