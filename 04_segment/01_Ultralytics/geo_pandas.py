import geopandas
from shapely.geometry import Point, Polygon

s = geopandas.GeoSeries([Polygon([(0, 0), (1, 1), (2, 2), (3, 3)])])
print(s.centroid)
