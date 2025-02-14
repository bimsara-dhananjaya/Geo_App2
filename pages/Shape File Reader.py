import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import tempfile
import zipfile
import os


def extract_shapefile(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


def main():
    st.title("Enhanced Shapefile Viewer on World Map")

    # File upload section for Shapefile
    shapefile_zip = st.file_uploader(
        "Upload Shapefile (ZIP archive)", type=["zip"])

    if shapefile_zip:
        # Create a temporary directory to extract the shapefile
        temp_dir = tempfile.mkdtemp()

        # Extract the contents of the ZIP archive
        extract_shapefile(shapefile_zip, temp_dir)

        # Find the .shp file in the extracted directory
        shp_file = next((f for f in os.listdir(temp_dir)
                        if f.endswith('.shp')), None)

        if shp_file:
            # Read the Shapefile using geopandas
            gdf = gpd.read_file(os.path.join(temp_dir, shp_file))

            # Display the first few rows of the attribute table
            st.write("Attribute Table:")
            st.write(gdf.head())

            # Calculate bounding box coordinates
            bbox = gdf.total_bounds

            # Map customization options
            st.sidebar.subheader("Map Options")
            auto_zoom = st.sidebar.checkbox(
                "Auto Zoom to Shapefile Bounds", True)

            if auto_zoom:
                center = [(bbox[1] + bbox[3]) / 2, (bbox[0] + bbox[2]) / 2]
                zoom = st.sidebar.slider(
                    "Zoom Level", min_value=1, max_value=18, value=12)
            else:
                center = st.sidebar.text_input(
                    "Map Center (lat, lon)", f"{(bbox[1] + bbox[3]) / 2}, {(bbox[0] + bbox[2]) / 2}")
                zoom = st.sidebar.slider(
                    "Zoom Level", min_value=1, max_value=18, value=2)

            # Display the map with customization
            m = folium.Map(location=center, zoom_start=zoom)

            # Styling options for GeoJSON layer
            geojson_style = st.sidebar.checkbox(
                "Customize GeoJSON Layer Style", False)
            if geojson_style:
                geojson_color = st.sidebar.color_picker(
                    "GeoJSON Layer Color", "#3388ff")
                geojson_opacity = st.sidebar.slider(
                    "GeoJSON Layer Opacity", min_value=0.0, max_value=1.0, value=0.6)

                # Add customized GeoJSON layer to the map
                folium.GeoJson(gdf, name='geojson', style_function=lambda x: {
                               'fillColor': geojson_color, 'fillOpacity': geojson_opacity}).add_to(m)
            else:
                # Add default GeoJSON layer to the map
                folium.GeoJson(gdf, name='geojson').add_to(m)

            # Display the Folium map in Streamlit
            folium_static(m)
        else:
            st.error("Error: Shapefile not found in the ZIP archive.")

        # Clean up: Remove the temporary directory
        os.rmdir(temp_dir)


if __name__ == '__main__':
    main()
