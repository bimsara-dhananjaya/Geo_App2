import streamlit as st
import rasterio
from io import BytesIO
import numpy as np
import plotly.graph_objects as go


def main():
    st.title("DEM Viewer: Flood and Landslide Susceptibility Analysis")

    uploaded_file = st.file_uploader(
        "Upload a GeoTIFF DEM file", type=["tif", "tiff"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_contents = uploaded_file.read()

        # Open the GeoTIFF using BytesIO
        dem_data = rasterio.open(BytesIO(file_contents))
        dem_array = dem_data.read(1)

        # Add sliders to adjust elevation values
        min_elevation = int(np.min(dem_array))
        max_elevation = int(np.max(dem_array))

        # Slider for flood susceptibility
        flood_threshold = st.slider(
            "Flood Threshold Elevation", min_value=min_elevation, max_value=max_elevation, value=min_elevation, step=1)

        # Slider for landslide susceptibility
        landslide_threshold = st.slider(
            "Landslide Threshold Slope", min_value=0.1, max_value=45.0, value=10.0, step=0.1)

        # Clip elevation values based on sliders
        dem_array = np.clip(dem_array, min_elevation, max_elevation)

        # Normalize data to [0, 255]
        normalized_data = normalize_to_255(dem_array)

        # Display 2D Terrain, Flood Susceptibility, and Landslide Susceptibility
        plot_2d_terrain(normalized_data)
        plot_flood_susceptibility(dem_array, flood_threshold)
        plot_landslide_susceptibility(dem_array, landslide_threshold)


def normalize_to_255(data):
    # Normalize data to [0, 255]
    min_val, max_val = np.min(data), np.max(data)
    normalized_data = 255 * (data - min_val) / (max_val - min_val)
    return normalized_data.astype(np.uint8)


def plot_2d_terrain(data):
    # Create a 2D Terrain plot using Plotly
    fig_2d = go.Figure(go.Surface(z=data, colorscale='Viridis'))

    # Update layout for 2D Terrain
    fig_2d.update_layout(scene=dict(
        aspectratio=dict(x=2, y=2, z=0.8),
        camera=dict(up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.25, y=1.25, z=1.25))),
        title_text="2D Terrain"
    )

    # Show the plot
    st.subheader("2D Terrain")
    st.plotly_chart(fig_2d, use_container_width=True)


def plot_flood_susceptibility(data, threshold):
    # Create a Flood Susceptibility plot using Plotly
    flood_susceptibility = np.zeros_like(data)
    # Set areas below the threshold to 1
    flood_susceptibility[data <= threshold] = 1

    fig_flood = go.Figure(go.Surface(
        z=flood_susceptibility, colorscale='Blues'))

    # Update layout for Flood Susceptibility
    fig_flood.update_layout(scene=dict(
        aspectratio=dict(x=2, y=2, z=0.8),
        camera=dict(up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.25, y=1.25, z=1.25))),
        title_text="Flood Susceptibility"
    )

    # Show the plot
    st.subheader("Flood Susceptibility")
    st.plotly_chart(fig_flood, use_container_width=True)


def plot_landslide_susceptibility(data, threshold):
    # Calculate slope using central difference method
    slope_x, slope_y = np.gradient(data)
    slope = np.sqrt(slope_x**2 + slope_y**2)

    # Create a Landslide Susceptibility plot using Plotly
    landslide_susceptibility = np.zeros_like(data)
    # Set areas with slope greater than the threshold to 1
    landslide_susceptibility[slope >= threshold] = 1

    fig_landslide = go.Figure(go.Surface(
        z=landslide_susceptibility, colorscale='Reds'))

    # Update layout for Landslide Susceptibility
    fig_landslide.update_layout(scene=dict(
        aspectratio=dict(x=2, y=2, z=0.8),
        camera=dict(up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.25, y=1.25, z=1.25))),
        title_text="Landslide Susceptibility"
    )

    # Show the plot
    st.subheader("Landslide Susceptibility")
    st.plotly_chart(fig_landslide, use_container_width=True)


if __name__ == "__main__":
    main()
