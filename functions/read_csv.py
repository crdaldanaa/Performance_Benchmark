# %%
import os
import pandas as pd
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sys


def select_folder():
    def window_folder():
        folder_selected = filedialog.askdirectory()
        return folder_selected

    # Crear la ventana principal de Tkinter
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    try:
        path_selected = os.path.normpath(window_folder())
        return path_selected
    except OSError:
        print("No se selecciono ninguna carpeta")


def solicitar_valor(msg):
    # Crear una ventana principal
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Crear un diálogo de entrada simple
    valor = simpledialog.askstring(
        "Entrada", f'Introduce el {msg}:')

    # Si se cierra la ventana sin ingresar un valor, detener el programa
    if valor is None:
        print("La ventana fue cerrada. Saliendo del programa.")
        sys.exit()  # Detener la ejecución del programa

    try:
        valor = int(valor)
        return valor
    except ValueError:
        valor = 'n'
        return valor


def seleccionar_separador():
    """
    Muestra una ventana flotante con una lista desplegable para seleccionar el carácter de separación.
    :return: Carácter de separación seleccionado por el usuario, o None si se cierra la ventana.
    """
    # Crear una ventana principal
    root = tk.Tk()
    root.title("Seleccionar Carácter de Separación")

    selection = None

    # Función para manejar la selección
    def on_select():
        nonlocal selection
        selection = combo.get()
        root.destroy()  # Cerrar la ventana al seleccionar

    # Lista de posibles caracteres de separación
    opciones = [',', ';', '\t', '|']

    # Crear un label y combobox
    tk.Label(root, text="Selecciona el carácter de separación:").pack(pady=20)
    combo = ttk.Combobox(root, values=opciones)
    combo.pack(pady=25)
    combo.set(opciones[0])  # Establecer un valor por defecto

    # Botón para confirmar la selección
    tk.Button(root, text="Seleccionar", command=on_select).pack(pady=10)

    # Esperar a que el usuario haga una selección
    root.mainloop()

    # Retornar la selección del usuario
    return selection


def program_select_file(n):
    def seleccionar_archivo(n):
        """
        Abre un cuadro de diálogo para seleccionar un archivo y retorna la ruta del archivo seleccionado.
        :return: Ruta del archivo seleccionado, o None si se cancela la selección.
        """
        # Crear una ventana principal
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal

        # Abrir el cuadro de diálogo para seleccionar un archivo
        ruta_archivo = filedialog.askopenfilename(
            title=f'Selecciona el archivo {n}',
            filetypes=[("Archivos CSV", "*.csv"),
                       ("Todos los archivos", "*.*")]
        )

        return ruta_archivo

    ruta = seleccionar_archivo(n)

    if ruta:
        print(f"Ruta del archivo {n}: {ruta}")
        # Guardar la ruta del archivo en una variable para su uso posterior
        ruta_csv = ruta
        return ruta_csv
    else:
        print("No se seleccionó ningún archivo. Saliendo del programa.")
        sys.exit()  # Detener la ejecución del programa


def input_csv():
    list_names = ['Control_Plots', 'Project_Plots']
    dfs = {}  # Diccionario para almacenar los DataFrames

    sep = seleccionar_separador()

    for name in list_names:
        while True:
            ruta = program_select_file(name)

            if ruta is None:
                print("La operación fue cancelada por el usuario. Terminando ejecución.")
                return None, None  # Terminar la ejecución si se cierra la ventana

            if os.path.exists(ruta):
                try:
                    df_cargado = pd.read_csv(ruta, sep=sep)
                    # Guardar el DataFrame en el diccionario
                    dfs[name] = df_cargado
                    break  # Salir del bucle si el archivo es válido
                except Exception as e:
                    print(f"No se pudo leer el archivo '{ruta}'. Error: {e}")

    # Retornar los DataFrames almacenados en el diccionario
    return dfs.get('Control_Plots'), dfs.get('Project_Plots')


# Ejemplo de uso
if __name__ == "__main__":
    """
    df_control, df_project = input_csv()
    print(df_control.head(10))
    print(f'\n{df_project.head(10)}')
    """
    print(select_folder())

# %%
