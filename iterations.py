from functions import read_csv, benchmark, cross_check_df, matriz_distances, slope_years, tests, weights
import numpy as np
import random
import pandas as pd


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

        for i in range(1000):
            np.random.seed(None)
            random.seed(None)
            # print(f'Este es el df original {df_project_plots}')
            df_sample_plots = df_project_plots.sample(n)
            df_sample_plots = df_sample_plots.sort_values(
                by=df_sample_plots.columns[0])
            # print(df_sample_plots)
            try:
                matrix_distances, assigned_plots, df_selected_plots = matriz_distances.arrange_plots(
                    df_sample_plots, df_control_plots, strs_project, id_project, k)
                sdm_dict, max_val_sdm = tests.sdm_column(df_selected_plots)
                df_weights = weights.weights(assigned_plots)
                df_selected_plots, cols = slope_years.slope_SI(
                    df_selected_plots, dict_project)

                z_dict, max_val_z, last_cols = tests.z_column(
                    df_selected_plots, cols)

                benchmark_df, total_pb = benchmark.performance_benchmark(
                    df_selected_plots, last_cols, z_dict)

                # Filtrar si cumple con las condiciones
                if max_val_sdm <= 0.25 and max_val_z <= 1.96:
                    count += 1
                    valid_results.append({
                        'matrix_distances': matrix_distances,
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
            except ValueError:
                print("Ingrese un número de vecinos cercanos (k) válido")
            except RecursionError:
                print("Ingrese un número de vecinos cercanos (k) válido")

        if not best_result:
            print("No se encontraron resultados válidos.")
            return None

        matrix_distances_df = best_result.get(
            'matrix_distances', pd.DataFrame())
        selected_plots_df = best_result.get(
            'df_selected_plots', pd.DataFrame())
        sdm_dict = best_result.get('sdm_dict', {})
        weights_df = best_result.get('df_weights', pd.DataFrame())
        benchmark_df = best_result.get('benchmark_df', pd.DataFrame())

        print(f'Se obtuvieron {
              count} escenarios que cumplen con las condiciones')

        return matrix_distances_df, selected_plots_df, sdm_dict, weights_df, benchmark_df

    except TypeError:
        print("Ingrese un valor válido de parcelas")
    except ValueError:
        print(f'El número de parcelas seleccionadas ({
              n}) es mayor que el número de parcelas en el dataset Project Plot')


if __name__ == '__main__':
    benchmark_software()
