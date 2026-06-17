from owslib.csw import CatalogueServiceWeb
import geopandas as gpd
from shapely.geometry import box
import pandas as pd

# URL do CSW (exemplo - substitua pelo seu endpoint)
CSW_URL = "https://demo.pycsw.org/cite/csw"

# Conecta ao CSW
csw = CatalogueServiceWeb(CSW_URL)

# Faz a consulta (ajuste maxrecords conforme necessário)
csw.getrecords2(maxrecords=100, esn='full')

records = csw.records

data = []

for rec_id, rec in records.items():
    try:
        uuid = rec.identifier
        titulo = rec.title
        data_pub = getattr(rec, 'date', None)

        # Extrair bbox (se existir)
        if rec.bbox:
            minx, miny, maxx, maxy = rec.bbox
            geom = box(minx, miny, maxx, maxy)
        else:
            geom = None

        data.append({
            "uuid": uuid,
            "titulo": titulo,
            "data": data_pub,
            "geometry": geom
        })

    except Exception as e:
        print(f"Erro no registro {rec_id}: {e}")

# Criar GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry="geometry", crs="EPSG:4326")

# Opcional: converter coluna de data
gdf["data"] = pd.to_datetime(gdf["data"], errors="coerce")

# Salvar como GeoParquet
output_file = "registros.parquet"
gdf.to_parquet(output_file, index=False)

print(f"Arquivo salvo em: {output_file}")
