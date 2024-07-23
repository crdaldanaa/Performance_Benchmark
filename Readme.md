# Software Cálculo Performance Benchmark

![](image_GIS.jpg)
__Creador :__ Cristian Aldana

* [Email](criistianaldana@outlook.com)
* [Linkedin](https://www.linkedin.com/in/cristian-aldana-046254140)
* [Github](https://github.com/crdaldanaa)


## Objetivo

Este script está diseñado para calcular el benchmark de proyectos de Aforestación, Reforestación y Restauración [ARR](https://ecologi.com/projects/afforestation-reforestation-and-revegetation-projects), conforme a la metodología [VM0047](https://verra.org/wp-content/uploads/2023/09/VM0047_ARR_v1.0-1.pdf) del estándar Verra en el escenario [ex-ante](https://abatable.com/carbon-glossary/ex-ante-credits/).
La metodología VM0047 proporciona un marco estructurado para desarrollar proyectos ARR.

## Definiciones
Las definiciones descritas a continuación provienen de la metodología VM0047 del estándar Verra.

1. **Control Plot**: Parcelas localizadas fuera del área de proyecto que poseen similaridad con los parcelas de proyecto. En estas se monitorea el Stocking Index por medio de sensores remotos.
2.  **Stocking Index**: Indice no especificado proveniente de sensores remotos que presenta una correlación (demostrada) con el almacenamiento de carbono medido in-situ. (Por ejemplo, NDVI, NDFI, EVI, entre otros).
3. **Project Plot**: Parcelas de hasta 10 ha muestreadas representativamente de la totalidad del área de proyecto. En estas se monitorea el Stocking Index por medio de sensores remotos.

## Características del Script

* **Lectura y Validación de Datos**: Importa y válida conjuntos de datos de parcelas de control y de proyecto.
>[!IMPORTANT]
>Los archivos que se seleccionen para la ejecución del programa (Control plo) deben estar en 
* **Selección de Parcelas**: Selecciona un subconjunto aleatorio de parcelas de proyecto para el análisis.
* **Cálculo de Distancias y Asignación de Parcelas**: Utiliza una matriz de distancias para asignar parcelas de proyecto a parcelas de control.
* **Evaluación del Desempeño**: Calcula métricas clave como el Desempeño Estandarizado (SDM) y el Puntaje Z, asegurando que cumplan con los umbrales establecidos.
* **Generación de Informes**: Produce un informe detallado del benchmark, destacando los resultados del análisis y las métricas de rendimiento.

>[!NOTE]
>El software realiza cada uno de los pasos delimitados por la metodología [VM0047](https://verra.org/wp-content/uploads/2023/09/VM0047_ARR_v1.0-1.pdf) en su versión 1.0.

##  Requerimientos 

Para ejecutar el presente necesario instalar los siguientes programas:

* [Python](https://www.python.org/downloads/)

## Instalación

Para instalar y configurar el entorno del proyecto, realice los siguientes pasos:

```bash
# Localice una carpeta donde vaya a clonar el repositorio
cd path

# Clone el repositorio
git clone https://github.com/usuario/proyecto.git

# Navegue al directorio donde se alojo el repositorio
cd proyecto

# Instale las dependencias
pip install -r requirements.txt
```

## Uso
1. 