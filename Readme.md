# Software Cálculo Performance Benchmark

![](image_GIS.jpg)
__Creador :__ Cristian Aldana

* [Email](criistianaldana@outlook.com)
* [Linkedin](https://www.linkedin.com/in/cristian-aldana-046254140)
* [Github](https://github.com/crdaldanaa)


## Objetivo

Este script está diseñado para calcular el benchmark de proyectos de Aforestación, Reforestación y Restauración [ARR](https://ecologi.com/projects/afforestation-reforestation-and-revegetation-projects), conforme a la metodología [VM0047](https://verra.org/wp-content/uploads/2023/09/VM0047_ARR_v1.0-1.pdf) del estándar Verra en el escenario [ex-ante](https://abatable.com/carbon-glossary/ex-ante-credits/).

La metodología VM0047 proporciona un marco estructurado para desarrollar proyectos ARR.
>[!NOTE]
>El software realiza cada uno de los pasos delimitados por la metodología [VM0047](https://verra.org/wp-content/uploads/2023/09/VM0047_ARR_v1.0-1.pdf) en su versión 1.0.

## Definiciones
Las definiciones descritas a continuación provienen de la metodología VM0047 del estándar Verra.

1. **Control Plot**: Parcelas localizadas fuera del área de proyecto que poseen similaridad con los parcelas de proyecto. En estas se monitorea el Stocking Index por medio de sensores remotos.
2.  **Stocking Index**: Indice no especificado proveniente de sensores remotos que presenta una correlación (demostrada) con el almacenamiento de carbono medido in-situ. (Por ejemplo, NDVI, NDFI, EVI, entre otros).
3. **Project Plot**: Parcelas de hasta 10 ha muestreadas representativamente de la totalidad del área de proyecto. En estas se monitorea el Stocking Index por medio de sensores remotos.

## Características del Script

* **Lectura y Validación de Datos**: Importa y válida conjuntos de datos de parcelas de control y de proyecto.
* **Selección de Parcelas**: Selecciona un subconjunto n (*definido por el usuario*) aleatorio de parcelas de proyecto para el análisis.
* **Cálculo de Distancias y Asignación de Parcelas**: Cálcula la [distancia de Mahalanobis](https://es.mathworks.com/help/stats/mahal.html) entre cada posible combinación de parcelas de control y de proyecto.
* **Asignación de Parcelas**: Para la asignación de las k (*definido por el usuario*) control plots a cada project plot y emplea un modelo de minimización tal que:
$$\text{min} \sum_{i=1}^{n} \sum_{j=1}^{m} \sqrt{(P_i - C_j)^T S^{-1} (P_i - C_j)}$$

Sujeto a las siguientes restricciones:

1. Cada Project Plot $P_i$ solo puede tener k o menos parcelas asignadas a un parcela de proyecto $P_i$. Esto se puede expresar con la siguiente restricción:

$$\sum_{j=1}^{m} x_{ij} \leq n, \quad \forall i = 1, \ldots, p$$

2. Cada parcela de control $C_j$ solo puede ser asignada a una única parcela de proyecto $P_i$. Esto se puede expresar con la siguiente restricción:

$$\sum_{i=1}^{p} x_{ij} \leq 1, \quad \forall j = 1, \ldots, m$$

Donde:

- $x_{ij}$ es una variable binaria que toma el valor 1 si la parcela de control $C_j$ está asignada a la parcela de proyecto $P_i$, y 0 en caso contrario.
- n es el número de control plots $C_j$ assignadas a cada project plot $P_i$.
>[!NOTE]
La restricción asegura que cada parcela de control $C_j$ esté asignada como máximo a una única parcela de proyecto $P_i$.

* **Evaluación del Desempeño**: Calcula métricas clave como el Diferencia de media Estandarizada ([SDM](https://www.statistics.com/glossary/standardized-mean-difference/) por sus siglas en ingles) y la prueba Z, asegurando que cumplan con los umbrales establecidos (0.25 y 1.96 respectivamente).
* **Prueba de Escenarios**: Se calculan cada uno de los pasos descritos anteriormente un total de 1000 veces y se selecciona el escenario con menor Performance Benchmark de los escenarios evaluados.
* **Generación de Informes**: A partir del escenario más óptimo obtenido se produce un informe detallado del benchmark, destacando los resultados del análisis, las métricas de rendimiento y las gráficas correspondientes.

>[!IMPORTANT]
>Los archivos que se seleccionen para la ejecución del programa (Control plot y Project plot) deben estar en formato csv.


##  Requerimientos 

Para ejecutar el presente programa es necesario instalar los siguientes programas:

* [Python](https://www.python.org/downloads/)

## Instalación

Para instalar y configurar el entorno del proyecto, realice los siguientes pasos:

```bash
# Localice una carpeta donde vaya a clonar el repositorio
cd path

# Clone el repositorio
git clone git@github.com:crdaldanaa/Performance_Benchmark.git

# Navegue al directorio donde se alojo el repositorio
cd proyecto

# Instale las dependencias
pip install -r requirements.txt
```

## Uso
Para el uso correcto del programa, realice los siguientes pasos:

1. Ejecute el archivo main.py
   
2. Seleccione el caracter de separación predeterminado para los archivos csv que contienen el Stocking Index de los Control Plots y Project Plots dentro de la lista desplegable
   
3. Seleccione el archivo que corresponde a los datos del Stocking Index de los diferentes Control Plots
   
4. Seleccione el archivo que corresponde a los datos del Stocking Index de los diferentes Project Plots
   
5. Introduzca el número de Project Plots (n) a seleccionar (Número entero)
   
6. Introduzca el número de Control Plots (k) a parear con cada Project Plot (Número entero)
   
7. Seleccione la carpeta donde se van a almacenar los resultados