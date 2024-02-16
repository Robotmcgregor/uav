# Processing UAV images manual pipeline (i.e. notebook)

**Pipeline Description**: This manual pipeline calls on 3 scripts located within the ntg_repo\uav\scripts repository. 
The manual pipeline workflow consists of the following:
 - five band composite image
 - clips the image
 - updates the image metadata

**Required parameters**:
 - Pix4D stitched image (multispectral only)
 - extent shapefile
 - data located in the uav directory tree structure (Z:\Scratch\uav\2022\wtr01)

Extent shapefile parameter requirements
| FID | Shape | flight |
| -- | --| --|
| integer | Polygon | site name (string) |

Shapefile must:
- be a single observation
- overlay the image you are wanting to clip
- be a polygon
- be in the same projection as the image


Once data has been processed the extent shapefiles need to be appended to the uav_extent geodatabase. All attributes need to be completed and the Pix4D report attached. Failure to do so may result in the refusal of future UAV equipment loan requests until data has been updated.

UAV Extent geodatabase is located: Z:\Scratch\uav

## Steps to load UAV extent to UAV Extent geodatabase.

 - Project extent shapefile to Geographic’ (GDA94)
 - Merge or append to a copy of the template shapefile to ensure schema compatibility
 - Edit attributes
 - Edit uav_extent layer
 - Load objects [Load objects must be added to your ArcGIS editor toolbar](https://desktop.arcgis.com/en/arcmap/10.3/manage-data/geodatabases/loading-data-in-arcmap-adding-the-load-objects-com.htm)
