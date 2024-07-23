import pandas as pd
from scipy.spatial.distance import mahalanobis
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary


def arrange_plots(df_project, df_control, str_covars, id_name, k_neighbors):
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

        # Crear un DataFrame vacío para almacenar las distancias
        distances_df = pd.DataFrame(df_project[id_name])

        for i, control_plot in df_control.iterrows():
            control_id = control_plot[id_name]
            distances = []
            for j, project_plot in df_project.iterrows():
                distance = mahalanobis_distance(
                    project_plot[str_covars].values,
                    control_plot[str_covars].values,
                    inv_cov_matrix
                )
                distances.append(distance)

            # Agregar las distancias al DataFrame con el nombre de la columna correspondiente al id de control_plot
            distances_df[control_id] = distances
        return distances_df

    matrix_distances = distance_mahalanobis_matrix(
        df_project, df_control, str_covars, id_name)

    # print(f'Esta es la matriz de distancias (Mahalanobis) entre los dataframes Control Plots y Project Plots.\n{matrix_distances}\n')

    # Extraemos los IDs de los project plots y los control plots
    project_plot_ids = matrix_distances.iloc[:, 0].values
    control_plot_ids = matrix_distances.columns[1:].values

    # Creamos el problema de minimización
    prob = LpProblem("Minimize_Mahalanobis_Distances", LpMinimize)

    # Creamos las variables de decisión
    x = LpVariable.dicts("assign", [
                         (i, j) for i in project_plot_ids for j in control_plot_ids], cat=LpBinary)

    # Función objetivo: minimizar la suma de las distancias de Mahalanobis
    prob += lpSum(matrix_distances.loc[matrix_distances.iloc[:, 0] == i, j].values[0]
                  * x[(i, j)] for i in project_plot_ids for j in control_plot_ids)

    # Restricción 1: cada project plot se asigna a un máximo de n control plots
    for i in project_plot_ids:
        prob += lpSum(x[(i, j)] for j in control_plot_ids) == k_neighbors

    # Restricción 2: cada control plot solo puede ser asignado a un único project plot
    for j in control_plot_ids:
        prob += lpSum(x[(i, j)] for i in project_plot_ids) <= 1

    # Resolvemos el problema
    prob.solve()

    # Extraemos las asignaciones y las distancias correspondientes
    assignments = []
    for i in project_plot_ids:
        for j in control_plot_ids:
            if x[(i, j)].varValue == 1:
                distance = matrix_distances.loc[matrix_distances.iloc[:, 0]
                                                == i, j].values[0]
                assignments.append([i, j, distance])

    # Creamos el DataFrame final
    assigned_plots = pd.DataFrame(assignments, columns=[
        "Project Plot ID", "Control Plot ID", "Mahalanobis Distance"])

    # print(assigned_plots)

    control_set = set()

    for index, row in assigned_plots.iterrows():
        control_plot_id = row['Control Plot ID']
        control_set.add(control_plot_id)
    control_set = sorted(control_set)

    # print(control_set)

    # List to store rows that meet the condition
    rows_to_add = []

    # Iterate through the rows of df_control_plots
    for index, item in df_control.iterrows():
        control_id = item[id_name]
        if control_id in control_set:
            # Append the row to the list
            rows_to_add.append(item)

    # Concatenate the list of rows into the new DataFrame
    df_project = pd.concat(
        [df_project, pd.DataFrame(rows_to_add)], ignore_index=True)

    # print(df_project)

    return matrix_distances, assigned_plots, df_project


if __name__ == '__main__':
    from cross_check_df import *

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
    print(strs_project)
    matrix_distances, assigned_plots, df_project = arrange_plots(
        df_project_plots, df_control_plots, strs_project, id_name, 1)

    print(assigned_plots)
