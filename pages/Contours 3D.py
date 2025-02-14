import streamlit as st
import numpy as np
import rasterio
from io import BytesIO
import plotly.graph_objects as go


def read_dem(dem_path):
    with rasterio.open(dem_path) as dataset:
        elevation = dataset.read(1)
        transform = dataset.transform
        return elevation, transform


def plot_3d_contour(dem_array, contour_levels):
    rows, cols = dem_array.shape
    x, y = np.meshgrid(np.arange(0, cols), np.arange(0, rows))

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=x.flatten(),
        y=y.flatten(),
        z=dem_array.flatten(),
        mode='markers',
        marker=dict(
            size=2,
            color=dem_array.flatten(),
            colorscale='Viridis',  # Use a valid colorscale name
            opacity=0.8,
        )
    ))

    # Add contour lines
    fig.add_trace(go.Contour(
        z=dem_array,
        colorscale='Viridis',  # Use the same colorscale
        opacity=0.6,
        contours=dict(showlines=True, start=np.min(dem_array),
                      end=np.max(dem_array), size=contour_levels)
    ))

    fig.update_layout(scene=dict(aspectmode="manual",
                      aspectratio=dict(x=1, y=1, z=0.5)))

    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Elevation (meters)'),
                      title='3D Contour Plot with Contour Lines')

    st.plotly_chart(fig)


def main():
    st.title("3D Contour Plot with Contour Lines from DEM")

    uploaded_file = st.file_uploader(
        "Upload a TIF image", type=["tif", "tiff"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_contents = uploaded_file.read()

        # Open the image using BytesIO
        dem_array, transform = read_dem(BytesIO(file_contents))

        # Display the 3D contour plot with contour lines using Plotly
        st.subheader("3D Contour Plot with Contour Lines")

        # Add a slider for adjusting contour levels
        contour_levels = st.slider(
            "Contour Levels", min_value=1, max_value=50, value=10)

        plot_3d_contour(dem_array, contour_levels)


if __name__ == "__main__":
    main()
