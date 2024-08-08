from functions import read_csv, benchmark, cross_check_df, matriz_distances, slope_years, tests, weights
import numpy as np
import random
import pandas as pd
import time
from numba import njit


def benchmark_software():
    df_control_plots, df_project_plots = read_csv.input_csv()
    response, df_control_plots, df_project_plots, strs_project, dict_project, id_project = cross_check_df.check_df(
        df_project_plots, df_control_plots)

    if response:
        print("La verificación de los Dataset no se completo con Exito.\n Reviselos e intente nuevamente")
        return None

    n = read_csv.solicitar_valor(
        "número de project plots (n) a seleccionar")

    try:
        k = read_csv.solicitar_valor(
            "número de vecinos cercanos (k) a seleccionar")
        # Almacenar resultados válidos
        valid_results = []
        min_total_pb = float('inf')
        best_result = {}
        count = 0
        """print(df_project_plots)"""

        for i in range(20):
            print(f'Generando el escenario {i}.')
            np.random.seed(None)
            random.seed(None)
            # print(f'Este es el df original {df_project_plots}')
            print(f"Muestreando las {n} parcelas definidas por el usuario")
            # print(f'Este es le numero de filas en el df Project {len(df_project_plots)}')
            df_sample_plots = df_project_plots.sample(n)
            df_sample_plots = df_sample_plots.sort_values(
                by=df_sample_plots.columns[0])
            """print(f'Este es le numero de filas muestreadas en el df Project {
                  len(df_sample_plots)}')"""

            """print(f'\nEste es le numero inicial filas en el df Control {
                  len(df_control_plots)}')"""

            df_sample_control_plots = df_control_plots.sample(n*100)
            df_sample_control_plots = df_sample_control_plots.sort_values(
                by=df_sample_control_plots.columns[0])

            """
            print(f"Este es la matriz de muestras tomadas para el Project Plot\n{
                  df_sample_plots}")
            print(f"Este es la matriz de muestras tomadas para el control Plot\n{
                  df_sample_control_plots}")
            """

            # print(f'Generando matriz de Distancias')

            matrix_distances = matriz_distances.distance_mahalanobis_matrix(
                df_sample_plots, df_sample_control_plots, strs_project, id_project)
            print(matrix_distances)

            print(f'Matriz de Distancias Finalizada')
            """
            # Paso 1: Extraer todos los valores de la primera columna de df1 y guardarlos en una cadena
            sample_plots_id_values = df_sample_plots.iloc[:, 0].tolist()
            values_string = ','.join(sample_plots_id_values)
            # print(f"Cadena de valores de la primera columna de df1: {values_string}")

            # Paso 2: Extraer todas las filas de df2 cuya primera columna sea igual a algún valor de df1
            matrix_distances_filtered = matrix_distances[matrix_distances.iloc[:, 0].isin(
                sample_plots_id_values)]
            """

            try:
                assigned_plots, df_selected_plots = matriz_distances.arrange_plots(
                    df_sample_plots, df_sample_control_plots, matrix_distances, id_project, k)
                sdm_dict, max_val_sdm = tests.sdm_column(
                    df_selected_plots, strs_project)

                print(
                    f'Este es el resultado de la prueba sdm en el escenario {i}\n{sdm_dict}')

                df_weights = weights.weights(assigned_plots)
                df_selected_plots, cols = slope_years.slope_SI(
                    df_selected_plots, dict_project)

                z_dict, max_val_z, last_cols = tests.z_column(
                    df_selected_plots, cols)
                print(
                    f'Este es el resultado de la prueba ztest en el escenario {i}\n{z_dict}')

                benchmark_df, total_pb = benchmark.performance_benchmark(
                    df_selected_plots, last_cols, z_dict)

                time.sleep(60)

                # Filtrar si cumple con las condiciones
                if max_val_sdm <= 0.25:
                    count += 1
                    valid_results.append({
                        'df_selected_plots': df_selected_plots,
                        'sdm_dict': sdm_dict,
                        'df_weights': df_weights,
                        'benchmark_df': benchmark_df,
                        'total_pb': total_pb
                    })

                    # Actualizar el mejor resultado si el total_pb es menor
                    if total_pb < min_total_pb:
                        min_total_pb = total_pb
                        best_result = {
                            'matrix_distances': matrix_distances,
                            'df_selected_plots': df_selected_plots,
                            'sdm_dict': sdm_dict,
                            'df_weights': df_weights,
                            'benchmark_df': benchmark_df,
                        }
                """
                else:
                    best_result = {
                        'df_selected_plots': df_selected_plots,
                        'sdm_dict': sdm_dict,
                        'df_weights': df_weights,
                        'benchmark_df': benchmark_df,
                    }
                """

            except ValueError:
                print("Ingrese un número de vecinos cercanos (k) válido")
            except RecursionError:
                print("Ingrese un número de vecinos cercanos (k) válido")

        if not best_result:
            print("No se encontraron resultados válidos.")
            return None

        matrix_distances = best_result.get(
            'matrix_distances', pd.DataFrame())
        selected_plots_df = best_result.get(
            'df_selected_plots', pd.DataFrame())
        sdm_dict = best_result.get('sdm_dict', {})
        weights_df = best_result.get('df_weights', pd.DataFrame())
        benchmark_df = best_result.get('benchmark_df', pd.DataFrame())

        print(f'Se obtuvieron {
              count} escenarios que cumplen con las condiciones')

    except UnboundLocalError:
        print("")

    except TypeError:
        print("Ingrese un valor válido de parcelas")

    except ValueError:
        print(f'El número de parcelas seleccionadas ({
              n}) es mayor que el número de parcelas en el dataset Project Plot')

    return matrix_distances, selected_plots_df, sdm_dict, weights_df, benchmark_df


if __name__ == '__main__':
    benchmark_software()
