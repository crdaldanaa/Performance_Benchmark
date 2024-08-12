import arcpy
from arcpy import env
import os

def formatSQL2(shp, dataList, NameCol, sqlTemplate, operator=" OR "):
    'a function to generate a SQL statement'
    sql = ''
    with arcpy.da.SearchCursor(shp, [NameCol]) as cursor:
        for row in cursor:
            value = row[0]
            for count, data in enumerate(dataList):
                if count != len(dataList) - 1:
                     sql += sqlTemplate.format(data) + operator
                else:
                    sql += sqlTemplate.format(data)
            return sql

def donorPoolarea (workspace, project_shp,biomes_shp,NameColBiomes, runap_shp,projects_shp,comunitaries_areas, bnb_shp, NameColBNB, CategoryNb, rivers_shp, jurisdiccionalArea, NameColJurisdiccional):
    #Define la sobrescritura de archivos
    arcpy.env.overwriteOutput = True

    """
    PROCESO PARA LA IDENTIFICACIÓN DE LOS BIOMAS Y/O JURISDICCIONES DEL AREA DE PROYECTO
    """

    try:
        # Se genera una lista con la capa del proyecto y la capa de jurisdicciones
        jurisdiccion_list = [project_shp, jurisdiccionalArea]

        ## Crea el archivo shp temporal para guardar el intersect entre las jurisdicciones y el PA
        temp_intersect_jurisdiccional_pa = os.path.join(workspace, "intersect_jurisdiccional_pa")

        # Ejecuta el intersect entre las jurisdicciones y el PA
        arcpy.analysis.Intersect(
            in_features=jurisdiccion_list,
            out_feature_class=temp_intersect_jurisdiccional_pa,
            join_attributes="ALL",
            cluster_tolerance=None,
            output_type="INPUT"
        )

        # Mantiene solamente la columna con el nombre de la Jurisdiccion
        arcpy.DeleteField_management(
            in_table=temp_intersect_jurisdiccional_pa,
            drop_field=NameColJurisdiccional,
            method="KEEP_FIELDS"
        )

        # Se inicializa un conjunto oara almacenar valores unicos de las jurisdicciones
        jurisdiccion_unique_values = set()

        # Recorre la capa intersectada y obtiene los valores unicos de las jurisdicciones y las devuelve en una lista
        with arcpy.da.SearchCursor(temp_intersect_jurisdiccional_pa, [NameColJurisdiccional]) as cursor:
            for row in cursor:
                value = row[0]  # Obtiene el valor de la columna especificada
                jurisdiccion_unique_values.add(value)

        jurisdiccion_unique_values = list(biomes_unique_values)

        ## Agrupa las variables de proyecto y la de biomas
        variables_list = [project_shp, biomes_shp]

        ## Crea el archivo shp temporal para guardar el intersect entre el PA y los biomas
        temp_intersect_pa = os.path.join(workspace,"intersect_pa")

        # Intersecta las capas anteriores
        arcpy.analysis.Intersect(
            in_features= variables_list,
            out_feature_class= temp_intersect_pa,
            join_attributes="ALL",
             cluster_tolerance=None,
             output_type="INPUT"
        )

        # Mantiene el nombre de la columna de la capa de biomas y elimina las demas
        arcpy.DeleteField_management(
            in_table=temp_intersect_pa,
            drop_field= NameColBiomes,
            method="KEEP_FIELDS"
        )

        # Se inicializa un conjunto set para almacenar valores unicos de los biomas
        biomes_unique_values = set()

        # Recorre el shp intersectado y extrae todos los valores de la columna que contiene los nombres de los biomas
        with arcpy.da.SearchCursor(temp_intersect_pa, [NameColBiomes]) as cursor:
            for row in cursor:
                value = row[0]  # Obtiene el valor de la columna especificada
                biomes_unique_values.add(value)

        # Obtiene un conjunto que almacena los nombres de los biomas del área del proyecto
        biomes_unique_values = list(biomes_unique_values)

    except:
        # Recorre la capa intersectada y obtiene los valores unicos de las jurisdicciones y las devuelve en una lista
        with arcpy.da.SearchCursor(temp_intersect_jurisdiccional_pa, [NameColJurisdiccional]) as cursor:
            for row in cursor:
                value = row[0]  # Obtiene el valor de la columna especificada
                jurisdiccion_unique_values.add(value)

        jurisdiccion_unique_values = list(biomes_unique_values)

        ## Agrupa las variables de proyecto y la de biomas
        variables_list = [project_shp, biomes_shp]

        ## Crea el archivo shp temporal para guardar el intersect entre el PA y los biomas
        temp_intersect_pa = os.path.join(workspace, "intersect_pa")

        # Intersecta las capas anteriores
        arcpy.analysis.Intersect(
            in_features=variables_list,
            out_feature_class=temp_intersect_pa,
            join_attributes="ALL",
            cluster_tolerance=None,
            output_type="INPUT"
        )

        # Mantiene el nombre de la columna de la capa de biomas y elimina las demas
        arcpy.DeleteField_management(
            in_table=temp_intersect_pa,
            drop_field=NameColBiomes,
            method="KEEP_FIELDS"
        )

        # Se inicializa un conjunto set para almacenar valores unicos de los biomas
        biomes_unique_values = set()

        # Recorre el shp intersectado y extrae todos los valores de la columna que contiene los nombres de los biomas
        with arcpy.da.SearchCursor(temp_intersect_pa, [NameColBiomes]) as cursor:
            for row in cursor:
                value = row[0]  # Obtiene el valor de la columna especificada
                biomes_unique_values.add(value)

        # Obtiene un conjunto que almacena los nombres de los biomas del área del proyecto
        biomes_unique_values = list(biomes_unique_values)


    """
    PROCESO PARA IDENTIFICACIÓN DONOR POOL AREA
    """

    ## Crea el archivo shp temporal para guardar el buffer de 100 Km del proyecto
    temp_buffer_dpa= os.path.join(workspace,"buffer_dpa_temp")

    ## Ejecuta un buffer de 100 Km al área del proyecto
    arcpy.analysis.Buffer(
        in_features=project_shp,
        out_feature_class=temp_buffer_dpa,
        buffer_distance_or_field="100 Kilometers",
        line_side="OUTSIDE_ONLY",
        line_end_type="ROUND",
        dissolve_option="ALL",
        dissolve_field=None,
        method="PLANAR"
    )

    ## Crea el archivo shp temporal para guardar el clip entre el buffer creado y la capa de biomas
    temp_clip_dpa= os.path.join(workspace,"clip_dpa_temp")

    if len(jurisdiccion_list) > 1:
        ## Genera un clip entre el buffer y las jurisdicciones
        arcpy.analysis.PairwiseClip(
            in_features=jurisdiccionalArea,
            clip_features=temp_buffer_dpa,
            out_feature_class= temp_clip_dpa,
            cluster_tolerance=None
        )

        ## Crea el archivo shp temporal para guardar el clip entre el buffer creado y las jurisdicciones
        temp_jursdiccion_dpa = os.path.join(workspace, "JurisdiccionalMatched_dpa_temp")

        ## Se crea la expresion base SQL para seleccionar las jurisdicciones que concuerdan con el area del proyecto
        sqlexpresionJ = NameColJurisdiccional + " = '{0}'"

        ## Se seleccionan los biomas que concuerdan
        arcpy.Select_analysis(
            in_features=temp_clip_dpa,
            out_feature_class=temp_jursdiccion_dpa,
            where_clause=formatSQL2(temp_clip_dpa, NameColJurisdiccional, jurisdiccion_unique_values, sqlexpresionJ)
        )

        # Se genera una lista con la capa de interseccion preliminar y la de biomas
        variables_opc1 = [temp_jursdiccion_dpa, biomes_shp]

        ## Crea el archivo shp temporal para guardar el intersect entre las dos varialbles
        temp_intersect_jb_dpa = os.path.join(workspace, "intersect_jb_dpa")

        # Ejecuta el intersect entre las dos variables
        arcpy.analysis.Intersect(
            in_features=variables_opc1,
            out_feature_class=temp_intersect_jb_dpa,
            join_attributes="ALL",
            cluster_tolerance=None,
            output_type="INPUT"
        )

        sqlexpresionB = NameColBiomes + " = '{0}'"

        ## Se seleccionan los biomas que concuerdan
        arcpy.Select_analysis(
            in_features=temp_clip_dpa,
            out_feature_class=temp_jursdiccion_dpa,
            where_clause=formatSQL2(temp_clip_dpa, jurisdiccion_unique_values, NameColBiomes, sqlexpresionB)
        )


        ## Crea el archivo shp temporal para guardar el clip entre el buffer creado y la capa de biomas
        temp_biomes_dpa = os.path.join(workspace, "biomesMatched_dpa_temp")

        ## Se crea la expresion base SQL para seleccionar los biomas que concuerdan con el area del proyecto
        sqlexpresionB = NameColBiomes + " = '{0}'"

        ## Se seleccionan los biomas que concuerdan
        arcpy.Select_analysis(
            in_features=temp_clip_dpa,
            out_feature_class=temp_biomes_dpa,
            where_clause=formatSQL2(temp_clip_dpa, biomes_unique_values, sqlexpresion)
        )

        temp_biomes_dpa = os.path.join(workspace, "biomesMatched_dpa_temp")

        sqlexpresionBiomes = NameColBiomes + " = '{0}'"
        sqlexpresionJurisdiccion = NameColJurisdiccional + " = '{0}'"

        arcpy.Select_analysis(
            in_features=temp_clip_dpa,
            out_feature_class=temp_biomes_dpa,
            where_clause=formatSQL2(temp_clip_dpa, biomes_unique_values, sqlexpresion)
        )

        excludedApAreas_dpa = os.path.join(workspace, "excludedApAreas_dpa_temp")

        arcpy.Erase_analysis(
            in_features= temp_biomes_dpa,
            erase_features= runap_shp,
             out_feature_class= excludedApAreas_dpa
        )

        excludedPaAreas_dpa = os.path.join(workspace, "excludedPaAreas_dpa_temp")

        arcpy.Erase_analysis(
            in_features= excludedApAreas_dpa,
            erase_features= projects_shp,
            out_feature_class= excludedPaAreas_dpa
        )

        excludedComunities_dpa = os.path.join(workspace,"excludedForest_dpa_temp")

        arcpy.Erase_analysis(
            in_features= excludedPaAreas_dpa,
            erase_features= comunitaries_areas,
            out_feature_class= excludedComunities_dpa
        )

        col_names = [NameColBiomes, NameColBNB]

        expressionFinal = NameColBNB + " = '" + CategoryNb + "'"

        try:
            excludedRivers_dpa = os.path.join(workspace, "excludedRivers_dpa_temp")

            arcpy.Erase_analysis(
                in_features=excludedComunities_dpa,
                erase_features=rivers_shp,
                out_feature_class=excludedRivers_dpa
            )

            final_list_Forest = [excludedRivers_dpa,bnb_shp]

            intersect_Forest_dpa = os.path.join(workspace, "intersect_Forest_dpa")

            arcpy.analysis.Intersect(
                in_features= final_list_Forest,
                out_feature_class= intersect_Forest_dpa,
                join_attributes="ALL",
                cluster_tolerance=None,
                output_type="INPUT"
            )

            arcpy.management.DeleteField(
                in_table=intersect_Forest_dpa,
                drop_field= col_names,
                method="KEEP_FIELDS"
            )

            donorPoolArea = os.path.join(workspace, "donorPoolArea")

            arcpy.Select_analysis(intersect_Forest_dpa,donorPoolArea,expressionFinal)

        except:
            intersect_Forest_dpa = os.path.join(workspace, "intersect_Forest_dpa")

            arcpy.analysis.Intersect(
                in_features=excludedComunities_dpa,
                out_feature_class=intersect_Forest_dpa,
                join_attributes="ALL",
                cluster_tolerance=None,
                output_type="INPUT"
            )

            arcpy.management.DeleteField(
                in_table=intersect_Forest_dpa,
                drop_field=col_names,
                method="KEEP_FIELDS"
            )

            donorPoolArea = os.path.join(workspace, "donorPoolArea")

            arcpy.Select_analysis(intersect_Forest_dpa, donorPoolArea, expressionFinal)

if __name__ == "__main__":
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    param2 = arcpy.GetParameterAsText(2)
    param3 = arcpy.GetParameterAsText(3)
    param4 = arcpy.GetParameterAsText(4)
    param5 = arcpy.GetParameterAsText(5)
    param6 = arcpy.GetParameterAsText(6)
    param7 = arcpy.GetParameterAsText(7)
    param8 = arcpy.GetParameterAsText(8)
    param9 = arcpy.GetParameterAsText(9)
    param10 = arcpy.GetParameterAsText(10)
    donorPoolarea(param0, param1,param2,param3,param4,param5,param6,param7,param8,param9,param10)
