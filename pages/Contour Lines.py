import streamlit as st
from PIL import Image
from io import BytesIO
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def main():
    st.title("Elevation Visualization Tool")  # Changed title here

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
        colormap_option = st.selectbox(
            "Colormap Option", ["Single Color", "Multi-Color"])

        if colormap_option == "Single Color":
            colormap_name = st.selectbox(
                "Colormap", ["Blues", "Greens", "Reds", "Purples", "Oranges"])
            colormap = plt.cm.get_cmap(colormap_name)
        else:
            # Create a custom multi-color colormap
            colors = ['#0000FF', '#00FF00', '#FFFF00', '#FFA500', '#FF0000']
            colormap = ListedColormap(colors)

        # Add sliders for elevation range and colormap
        elevation_min, elevation_max = st.slider(
            "Elevation Range", elevation_min, elevation_max, (elevation_min, elevation_max))

        # Calculate default contour line spacing
        contour_spacing_default = (elevation_max - elevation_min) / 10

        # Add slider for contour line spacing
        contour_spacing = st.slider(
            "Contour Line Spacing", float(elevation_min), float(elevation_max), float(contour_spacing_default))

        # Round contour spacing to the nearest integer
        contour_spacing = round(contour_spacing)

        # Add checkboxes to toggle contour lines and elevation annotations
        show_contours = st.checkbox("Show Contour Lines")
        show_elevation = st.checkbox("Show Elevation Annotations")

        # Apply the colormap to the DEM array
        plt.imshow(dem_array, cmap=colormap,
                   vmin=elevation_min, vmax=elevation_max)

        if show_contours:
            # Add contour lines
            contour_levels = np.arange(
                elevation_min, elevation_max, contour_spacing)
            plt.contour(dem_array, levels=contour_levels,
                        colors='black', linewidths=0.5)

        if show_elevation:
            if show_contours:  # Ensure DEM is not displayed twice
                plt.clf()  # Clear the existing plot
            # Display the DEM
            plt.imshow(dem_array, cmap=colormap,
                       vmin=elevation_min, vmax=elevation_max)
            # Add contour lines
            contour_levels = np.arange(
                elevation_min, elevation_max, contour_spacing)
            contour = plt.contour(dem_array, levels=contour_levels,
                                  colors='black', linewidths=0.5)
            # Annotate contour lines with elevation values
            plt.clabel(contour, inline=True, fontsize=8, fmt='%1.0f')

        plt.colorbar(label='Elevation (meters)')
        plt.title('Digital Elevation Model')
        plt.axis('off')  # Disable axis
        st.pyplot()


if __name__ == "__main__":
    main()
