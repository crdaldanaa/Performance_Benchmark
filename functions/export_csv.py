import dask.dataframe as dd


def save_csv(input_file, columns_needed, output_file, char):
    # Leer el archivo CSV con Dask, seleccionando solo las columnas necesarias
    df = dd.read_csv(input_file, usecols=columns_needed)

    # Guardar el DataFrame seleccionado en un nuevo archivo CSV
    df.to_csv(output_file, single_file=True, index=False, sep=char)


def cambiar_separadores(input_file, original_delimiter, new_delimiter, output_file):
    # Leer el archivo CSV con el delimitador original
    df = dd.read_csv(input_file, delimiter=original_delimiter)

    # Guardar el DataFrame con el nuevo delimitador
    df.to_csv(output_file, single_file=True, index=False, sep=new_delimiter)


if __name__ == '__main__':
    # Ruta del archivo CSV de entrada
    # input_file = r"D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\Data\Project_Plots.csv"
    input_file = r"D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\Data\GRVI\GRVI_ProjectPlots.csv"

    # Columnas que necesitas seleccionar
    # Reemplaza con los nombres de tus columnas
    columns_needed = ['ID', 'GRVI_14', 'GRVI_17', 'GRVI_24']

    # Ruta del archivo CSV de salida definido por el usuario
    output_file = r"D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\Data\GRVI\GRVI_ProjectPlots1.csv"

    """
    save_csv(input_file, columns_needed, output_file, ',')
    """

    # Ejecutar la función
    cambiar_separadores(input_file, ';', ",", output_file)
    print(f"Programa Finalizado!!")
