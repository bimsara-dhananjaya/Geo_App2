import streamlit as st
import geopandas as gpd
import os
from zipfile import ZipFile


def main():
    st.title("Shapefile Data Extractor")

    # Upload ZIP file containing shapefile
    uploaded_zip = st.file_uploader(
        "Upload ZIP file containing shapefile", type="zip")

    if uploaded_zip is not None:
        # Extract the contents of the ZIP file to a temporary directory
        with ZipFile(uploaded_zip, 'r') as zip_ref:
            zip_ref.extractall('temp')

        # Get all files in the extracted directory
        files = os.listdir('temp')

        # Filter files to only include those with .shp extension
        shapefile_files = [file for file in files if file.endswith(".shp")]

        if len(shapefile_files) == 0:
            st.error("No shapefile found in the uploaded ZIP file.")
        elif len(shapefile_files) > 1:
            st.error(
                "Multiple shapefiles found in the uploaded ZIP file. Please upload only one shapefile.")
        else:
            # Load shapefile into GeoDataFrame
            shapefile_path = os.path.join('temp', shapefile_files[0])
            gdf = gpd.read_file(shapefile_path)

            # Display basic information about the GeoDataFrame
            st.subheader("Shapefile Information:")
            st.write("Number of rows:", len(gdf))
            st.write("CRS (Coordinate Reference System):", gdf.crs)

            # Display the first few rows of the GeoDataFrame
            st.subheader("Preview of Data:")
            st.write(gdf.head())

            # Display specific columns
            selected_column = st.selectbox(
                "Select a column to display:", gdf.columns)
            st.write(gdf[selected_column])

        # Clean up temporary directory
        os.system('rm -rf temp')


if __name__ == "__main__":
    main()
