import streamlit as st
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

# Function to create GeoDataFrame from CSV data


def create_geodataframe(data, latitude_col, longitude_col, label_col):
    if latitude_col not in data.columns or longitude_col not in data.columns:
        st.error(
            "Error: Selected latitude or longitude columns not found in the DataFrame.")
        return None

    geometry = [Point(xy)
                for xy in zip(data[longitude_col], data[latitude_col])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry)

    # Set the coordinate reference system to WGS84
    gdf.crs = 'EPSG:4326'

    # Set the label column
    if label_col and label_col in data.columns:
        gdf['label'] = data[label_col]

    return gdf

# Streamlit app


def main():
    st.title("Georeferencing App")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None and uploaded_file.readable():
        # Allow users to select latitude, longitude, and label columns
        try:
            data = pd.read_csv(uploaded_file)
            columns = data.columns
        except pd.errors.EmptyDataError:
            st.error("Error: The CSV file is empty.")
            return

        latitude_col = st.selectbox("Select Latitude Column", options=columns)
        longitude_col = st.selectbox(
            "Select Longitude Column", options=columns)
        label_col = st.selectbox(
            "Select Label Column (Optional)", options=[""] + list(columns))

        st.sidebar.subheader("Data Preview")
        st.sidebar.write(data.head())

        st.sidebar.subheader("Map Preview")
        gdf = create_geodataframe(data, latitude_col, longitude_col, label_col)

        if gdf is not None:
            st.map(gdf)

            st.sidebar.subheader("Save GeoDataFrame")
            if st.button("Save GeoDataFrame"):
                gdf.to_file("output.shp", driver="ESRI Shapefile")
                st.success("GeoDataFrame saved successfully!")


if __name__ == "__main__":
    main()
