import streamlit as st
from PIL import Image
from io import BytesIO
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def main():
    st.title("Line of Sight Analysis")

    uploaded_file = st.file_uploader(
        "Upload a TIF image", type=["tif", "tiff"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_contents = uploaded_file.read()

        # Open the image using BytesIO
        dem_data = rasterio.open(BytesIO(file_contents))
        dem_array = dem_data.read(1)
        transform = dem_data.transform

        # Set default elevation range
        elevation_min, elevation_max = np.min(dem_array), np.max(dem_array)

        # Set default colormap
        colormap = ListedColormap(
            ['#045a8d', '#2b8cbe', '#74a9cf', '#bdc9e1', '#f1eef6'])

        # Add sliders for elevation range and colormap
        elevation_min, elevation_max = st.slider(
            "Elevation Range", elevation_min, elevation_max, (elevation_min, elevation_max))
        colormap_name = st.selectbox(
            "Colormap", ["Blues", "Greens", "Reds", "Purples", "Oranges"])

        # Update colormap based on user selection
        colormap = plt.cm.get_cmap(colormap_name)

        # Apply the colormap to the DEM array
        plt.imshow(dem_array, cmap=colormap,
                   vmin=elevation_min, vmax=elevation_max)
        plt.colorbar(label='Elevation (meters)')
        plt.title('Digital Elevation Model with Colormap')
        st.pyplot()

        # Continue with the rest of your code for visibility analysis


if __name__ == "__main__":
    main()
