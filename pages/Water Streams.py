import streamlit as st
from PIL import Image
from io import BytesIO
import rasterio
import numpy as np
import matplotlib.pyplot as plt


def read_dem(dem_path):
    with rasterio.open(dem_path) as dataset:
        elevation = dataset.read(1)
        return elevation, dataset.transform


def plot_dem(elevation):
    plt.imshow(elevation, cmap='terrain')
    plt.colorbar(label='Elevation (meters)')
    plt.title('Digital Elevation Model')
    st.pyplot()


def compute_flow_directions(elevation):
    gradient_x, gradient_y = np.gradient(elevation)
    flow_directions = np.arctan2(gradient_y, gradient_x)
    flow_directions = np.degrees(flow_directions) % 360
    flow_directions[flow_directions < 0] += 360
    flow_direction_codes = np.ceil(flow_directions / 45).astype(int)
    return flow_direction_codes


def highlight_water_streams(dem_array, flow_directions, water_threshold):
    water_streams = (flow_directions == 7) | (flow_directions == 8)
    water_streams = water_streams & (dem_array <= water_threshold)
    highlighted_dem = np.ma.masked_where(~water_streams, dem_array)
    return highlighted_dem


def main():
    st.title("Water Streams Highlighting")

    uploaded_file = st.file_uploader(
        "Upload a TIF image", type=["tif", "tiff"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_contents = uploaded_file.read()

        # Open the image using BytesIO
        dem_array, transform = read_dem(BytesIO(file_contents))

        # Plot DEM data
        plot_dem(dem_array)

        # Compute flow directions
        flow_directions = compute_flow_directions(dem_array)

        # Add a slider for adjusting water stream threshold
        water_threshold = st.slider(
            "Water Stream Threshold", min_value=np.min(dem_array), max_value=np.max(dem_array), value=np.min(dem_array)
        )

        # Highlight water streams based on the threshold
        highlighted_dem = highlight_water_streams(
            dem_array, flow_directions, water_threshold
        )

        # Plot highlighted water streams
        plt.imshow(highlighted_dem, cmap='Blues')
        plt.colorbar(label='Elevation (meters)')
        plt.title('Highlighted Water Streams')
        st.pyplot()


if __name__ == "__main__":
    main()
