# Añadir la raíz del proyecto al PYTHONPATH
from functions import read_csv, save_df, graphs
from iterations import benchmark_software


def run():
    matrix_distances_df, selected_plots_df, sdm_dict, weights_df, benchmark_df = benchmark_software()
    path = read_csv.select_folder()
    graphs.sdm_graph(sdm_dict, path)
    path_excel = save_df.save_df_excel(
        matrix_distances_df, path, 'Matrix Distance Mahalanobis')
    save_df.add_df_new_sheet(selected_plots_df, path_excel, 'SI')
    save_df.add_df_new_sheet(weights_df, path_excel, 'Control Weights')
    # save_df.add_df_new_sheet(benchmark_df, path_excel, 'Benchmark')


if __name__ == '__main__':
    run()
