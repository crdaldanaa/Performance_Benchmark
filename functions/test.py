import pandas as pd
from scipy.spatial.distance import mahalanobis
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary


def distance_mahalanobis_matrix(df_project, df_control, str_covars, id_name):
    cov_matrix = np.cov(
        df_project[str_covars].values, rowvar=False)

    # Añadir una pequeña constante a la diagonal para hacer la matriz invertible
    regularization_constant = 1e-10
    cov_matrix += np.eye(cov_matrix.shape[0]) * regularization_constant

    inv_cov_matrix = np.linalg.inv(cov_matrix)

    # Función para calcular la distancia de Mahalanobis
    def mahalanobis_distance(x, y, inv_cov_matrix):
        return mahalanobis(x, y, inv_cov_matrix)

    # Nombre de la columna adicional
    columna_id = 'Project Plot ID'

    # Extraer los nombres de las columnas desde la primera columna del DataFrame existente
    column_names = [columna_id] + df_control[id_name].tolist()

    # Crear una lista para almacenar todas las filas de distancias
    all_distances = []

    # Itera sobre los project plots
    for i, project_plot in df_project.iterrows():
        project_id = project_plot[id_name]
        distances = [project_id]
        # Calcula las distancias para cada control plot
        for j, control_plot in df_control.iterrows():
            distance = mahalanobis_distance(
                project_plot[str_covars].values,
                control_plot[str_covars].values,
                inv_cov_matrix
            )
            distances.append(round(float(distance), 3))

        # Añadir la fila de distancias a la lista
        all_distances.append(distances)

    # Crear el DataFrame final con todas las distancias
    distances_df = pd.DataFrame(all_distances, columns=column_names)

    return distances_df


if __name__ == '__main__':
    from cross_check_df import *

    df_project_plots = pd.DataFrame({
        'ID': [1, 2, 3],
        '2010': [4.1, 5.2, 5.0],
        '2015': [4.2, 5.3, 5.1],
        '2020': [4.5, 5.4, 5.3]
    })

    df_control_plots = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        '2010': [4.1, 5.2, 3.3, 3.5, 1.0, 8.5, 5.2, 7.5, 8.4, 6.1],
        '2020': [4.7, 5.4, 3.5, 1.6, 2.5, 6.6, 7.7, 8.2, 3.4, 2.5],
        '2015': [4.2, 5.3, 3.4, 2.1, 2.4, 2.5, 5.5, 6.6, 7.7, 4.1]
    })

    response, df_control_plots, df_project_plots, strs_project, dict_project, id_name = check_df(
        df_project_plots, df_control_plots)
    matrix_distances = distance_mahalanobis_matrix(
        df_project_plots, df_control_plots, strs_project, id_name)

    print(matrix_distances)
