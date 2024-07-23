import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


def sdm_graph(dict, save_path):
    sdm_df = pd.DataFrame(list(dict.items()), columns=['Covars', 'SDM'])
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Covars', y='SDM', data=sdm_df,
                palette='cubehelix', legend=False, hue=5)
    plt.axhline(y=0.25, color='r', linestyle='--', label='Threshold 0.25')

    # Añadir título y etiquetas
    plt.title('Standardized Difference of Means (SDM) Covars')
    plt.xlabel('Covars')
    plt.ylabel('SDM')

    name_graph = 'graph_sdm_covars.jpg'
    save_path = os.path.join(save_path, name_graph)

    plt.savefig(save_path, bbox_inches='tight')


if __name__ == '__main__':
    import read_csv
    dict = {
        '2010': 0.7158291329065406,
        '2015': 0.7158291329065409,
        '2020': 0.698297248755174
    }

    path = read_csv.select_folder()

    sdm_graph(dict, path)
