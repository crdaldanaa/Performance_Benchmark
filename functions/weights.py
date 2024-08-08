import numpy as np


def weights(df):
    def calculate_weights(df):
        exp_neg_distance = np.exp(-df['Mahalanobis Distance'])
        df['Wcontrol,i,j'] = exp_neg_distance / exp_neg_distance.sum()
        return df

    # Crear una copia de la columna 'Project_Plot'
    df['Project Plot ID Copy'] = df["Project Plot ID"]

    # Agrupar por Project_Plot y aplicar la función de cálculo de pesos
    df_weights = df.groupby('Project Plot ID', group_keys=False).apply(
        calculate_weights, include_groups=False).reset_index(drop=True)

    # Añadir la columna 'Project_Plot_Copy' al inicio de grouped_df
    df_weights.insert(0, 'Project Plot ID',
                      df_weights.pop('Project Plot ID Copy'))

    # print(df_weights)
    return df_weights


if __name__ == '__main__':
    from cross_check_df import *
    from matriz_distances import *

    df_project_plots = pd.DataFrame({
        'ID': ['P1', 'P2', 'P3'],
        '2010': [4.1, 5.2, 5.0],
        '2015': [4.2, 5.3, 5.1],
        '2020': [4.5, 5.4, 5.3]
    })

    df_control_plots = pd.DataFrame({
        'ID': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'],
        '2010': [4.1, 5.2, 3.3, 3.5, 1.0, 8.5, 5.2, 7.5, 8.4, 6.1],
        '2020': [4.7, 5.4, 3.5, 1.6, 2.5, 6.6, 7.7, 8.2, 3.4, 2.5],
        '2015': [4.2, 5.3, 3.4, 2.1, 2.4, 2.5, 5.5, 6.6, 7.7, 4.1]
    })

    response, df_control_plots, df_project_plots, strs_project, dict_project, id_name = check_df(
        df_project_plots, df_control_plots)

    matrix_distances = distance_mahalanobis_matrix(
        df_project_plots, df_control_plots, strs_project, id_name)

    assigned_plots, df_selected_plots = arrange_plots(
        df_project_plots, df_control_plots, matrix_distances, id_name, 1)

    print(weights(assigned_plots))
