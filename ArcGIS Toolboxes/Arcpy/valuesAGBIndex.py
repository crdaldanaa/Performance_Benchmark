import arcpy

import os

# Establecer los paths a los archivos

#def correlationValues(pointsShp, spatialReference, rasterFileIndexes, rasterFileAgb, outputTableFile):

arcpy.env.overwriteOutput = True
#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(spatialReference)

workspace = r'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\Test'
arcpy.env.workspace = workspace
rasterFileIndexes = r'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\land_indices_2017.tif'
rasterFileAgb = r'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\AGB_CEDA_2017.tif'
pointsShp = r'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\Total_Points.shp'
#outputTableFile = arcpy.CreateTable_management(workspace, "ExtractedValues_v1.csv")

# Añadir bandas del los raster a una lista común
band_list = []

# Añadir campos para cada banda del VRT y raster
raster_list = [rasterFileIndexes, rasterFileAgb]

raster_bands = [
    (r'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\land_indices_2017.tif', ['AFRI1600', 'AFRI2100']),
    (r'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\AGB_CEDA_2017.tif', ['Band_1'])  # Añadir bandas específicas si es necesario
]

# Construir la cadena de entrada para in_rasters en ExtractMultiValuesToPoints
in_rasters = []

def get_bands(path_to_raster):
    """ Get a list of band names from a multiband raster """

    # Save previous workspace
    oldws = arcpy.env.workspace

    #Get raster objects from band names
    arcpy.env.workspace = path_to_raster
    bands = arcpy.ListRasters()

    #Restore previous workspace
    arcpy.env.workspace = oldws

    return bands

print(get_bands(r'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\Test'))

"""
arcpy.sa.ExtractMultiValuesToPoints(
    in_point_features="Total_Points",
    in_rasters=r"'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\land_indices_2017.tif\AFRI1600' AFRI1600_1;'D:\OneDrive\02_Carbon Market\03_Work\01_ALLCOT\08_Bioporio\land_indices_2017.tif\AFRI2100' AFRI2100_1",
    bilinear_interpolate_values="NONE"
)

for raster in raster_list:
    pointsValues = os.path.join(workspace, "pointsValues")
    arcpy.sa.ExtractValuesToPoints(
        in_point_features=pointsShp,
        in_raster=raster,
        out_point_features=pointsValues,
        interpolate_values="INTERPOLATE",
        add_attributes="VALUE_ONLY"
    )

    print("Extracción de valores completada y exportada a la tabla.")
"""