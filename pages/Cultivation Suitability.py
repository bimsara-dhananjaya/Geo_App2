import streamlit as st
import rasterio
from io import BytesIO
import numpy as np
import plotly.graph_objects as go


def main():
    st.title("DEM Viewer: Cultivation Suitability Analysis")

    uploaded_file = st.file_uploader(
        "Upload a GeoTIFF DEM file", type=["tif", "tiff"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_contents = uploaded_file.read()

        # Open the GeoTIFF using BytesIO
        with BytesIO(file_contents) as byte_io:
            dem_data = rasterio.open(byte_io)
            dem_array = dem_data.read(1)

            # Add sliders to adjust elevation values
            min_elevation = int(np.min(dem_array))
            max_elevation = int(np.max(dem_array))
            elevation_threshold = st.slider(
                "Cultivation Suitability Elevation", min_value=min_elevation, max_value=max_elevation, value=max_elevation, step=1)

            # Clip elevation values based on sliders
            dem_array = np.clip(dem_array, min_elevation, max_elevation)

            # Normalize data to [0, 255]
            normalized_data = normalize_to_255(dem_array)

            # Display 2D Terrain and Cultivation Suitability
            plot_2d_terrain(normalized_data)
            plot_cultivation_suitability(dem_array, elevation_threshold)


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


def plot_cultivation_suitability(data, threshold):
    # Create a Cultivation Suitability plot using Plotly
    cultivation_suitability = np.zeros_like(data)
    # Set areas below the threshold to 1 (suitable for cultivation)
    cultivation_suitability[data <= threshold] = 1

    fig_cultivation = go.Figure(go.Surface(
        z=cultivation_suitability, colorscale='Greens'))

    # Update layout for Cultivation Suitability
    fig_cultivation.update_layout(scene=dict(
        aspectratio=dict(x=2, y=2, z=0.8),
        camera=dict(up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.25, y=1.25, z=1.25))),
        title_text="Cultivation Suitability"
    )

    # Show the plot
    st.subheader("Cultivation Suitability")
    st.plotly_chart(fig_cultivation, use_container_width=True)


if __name__ == "__main__":
    main()
