import streamlit as st
from PIL import Image
from io import BytesIO
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource


def read_dem(dem_path):
    with rasterio.open(dem_path) as dataset:
        elevation = dataset.read(1)
        return elevation, dataset.transform


def calculate_slope_and_aspect(elevation):
    gradient_x, gradient_y = np.gradient(elevation)
    slope = np.arctan(np.sqrt(gradient_x**2 + gradient_y**2))
    aspect = np.arctan2(-gradient_y, gradient_x)
    aspect[aspect < 0] += 2.0 * np.pi
    return np.degrees(slope), np.degrees(aspect)


def calculate_curvature(elevation):
    gradient_x, gradient_y = np.gradient(elevation)
    gradient_xx, gradient_xy = np.gradient(gradient_x)
    gradient_yx, gradient_yy = np.gradient(gradient_y)
    curvature = (gradient_xx * gradient_yy - gradient_xy * gradient_yx) / \
        (1 + gradient_x**2 + gradient_y**2)**(3/2)
    return curvature


def main():
    st.title("DEM, Slope, Aspect, Curvature, and Hillshade Identification")

    uploaded_file = st.file_uploader(
        "Upload a TIF image", type=["tif", "tiff"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_contents = uploaded_file.read()

        # Open the image using BytesIO
        dem_array, transform = read_dem(BytesIO(file_contents))

        # Display the normal DEM
        st.subheader("Digital Elevation Model (DEM)")
        plt.imshow(dem_array, cmap='terrain')
        plt.colorbar(label='Elevation (meters)')
        plt.title('Digital Elevation Model (DEM)')
        st.pyplot()

        # Compute and display the slope
        slope, aspect = calculate_slope_and_aspect(dem_array)

        # Toggle Slope visibility
        show_slope = st.checkbox("Show Slope", value=False)
        if show_slope:
            st.subheader("Slope Map")
            slope_min, slope_max = st.slider(
                "Adjust Slope Range", min_value=0, max_value=90, value=(0, 90))
            plt.imshow(np.clip(slope, slope_min, slope_max), cmap='viridis')
            plt.colorbar(label='Slope (degrees)')
            plt.title('Slope Map')
            st.pyplot()

        # Toggle Aspect visibility
        show_aspect = st.checkbox("Show Aspect", value=False)
        if show_aspect:
            st.subheader("Aspect Map")
            aspect_min, aspect_max = st.slider(
                "Adjust Aspect Range", min_value=0, max_value=360, value=(0, 360))
            plt.imshow(np.clip(aspect, aspect_min, aspect_max), cmap='hsv')
            plt.colorbar(label='Aspect (degrees)')
            plt.title('Aspect Map')
            st.pyplot()

        # Compute and display the curvature
        curvature = calculate_curvature(dem_array)

        # Toggle Curvature visibility
        show_curvature = st.checkbox("Show Curvature", value=False)
        if show_curvature:
            st.subheader("Curvature Map")
            curvature_min, curvature_max = st.slider(
                "Adjust Curvature Range", min_value=-0.1, max_value=0.1, value=(-0.1, 0.1), step=0.01)
            plt.imshow(np.clip(curvature, curvature_min,
                       curvature_max), cmap='coolwarm')
            plt.colorbar(label='Curvature')
            plt.title('Curvature Map')
            st.pyplot()

        # Toggle Hillshade visibility
        show_hillshade = st.checkbox("Show Hillshade", value=False)
        if show_hillshade:
            st.subheader("Hillshade")
            hillshade_intensity = st.slider(
                "Adjust Hillshade Intensity", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
            ls = LightSource(azdeg=315, altdeg=45)
            hillshade = ls.hillshade(dem_array, vert_exag=hillshade_intensity)
            plt.imshow(hillshade, cmap='gray', aspect='auto')
            plt.title('Hillshade')
            st.pyplot()


if __name__ == "__main__":
    main()
