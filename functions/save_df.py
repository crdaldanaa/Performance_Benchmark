import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
from openpyxl.worksheet.table import Table, TableStyleInfo
from numba import njit
import os


def save_df_excel(df, save_path, sheet_name):
    # Obtener la fecha actual
    now = datetime.now()

    # Extraer día, mes y año
    dia = now.strftime("%d")
    mes = now.strftime("%m")
    año = now.strftime("%Y")

    date = dia+mes+año
    name_excel = str('Results_PB_'+date+'.xlsx')
    save_path = os.path.join(save_path, name_excel)

    print(save_path)

    df.to_excel(save_path, sheet_name=sheet_name, index=False)

    # print(f'DataFrame guardado en {save_path} en la hoja {sheet_name}.')

    return save_path


def add_df_new_sheet(df, save_path, sheet_name):
    try:
        # Carga el libro de trabajo existente
        book = load_workbook(save_path)

        # Crea un objeto ExcelWriter con el libro existente
        with pd.ExcelWriter(save_path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f'DataFrame añadido como nueva hoja {
                  sheet_name} en {save_path}.')
    except FileNotFoundError:
        print(f'El archivo {save_path} no existe. Se creará un nuevo archivo.')
        save_df_excel(df, save_path, sheet_name)


if __name__ == '__main__':
    from read_csv import *
    df_example = pd.DataFrame({
        'Day': [1, 2, 3, 4, 5, 6],
        'Meet': [True, False, True, False, False, False]
    })

    df_example1 = pd.DataFrame({
        'Day': [1, 2, 3, 4, 5, 6],
        'Meet': [True, False, True, False, False, False]
    })

    # print(type(select_folder()))

    path = save_df_excel(
        df_example, select_folder(), "Test01")

    add_df_new_sheet(df_example1, path, "Sheet02")
