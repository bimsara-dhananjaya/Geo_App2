import streamlit as st
import numpy as np
import plotly.graph_objects as go
import rasterio
from io import BytesIO
import matplotlib.pyplot as plt


def read_dem(dem_path):
    with rasterio.open(dem_path) as dataset:
        elevation = dataset.read(1)
        transform = dataset.transform
        return elevation, transform


def plot_dem_2d(dem_array):
    plt.imshow(dem_array, cmap='terrain')
    plt.colorbar(label='Elevation (meters)')
    plt.title('Digital Elevation Model (DEM)')
    st.pyplot()


def plot_dem_3d(dem_array, transform):
    rows, cols = dem_array.shape
    x, y = np.meshgrid(np.arange(0, cols), np.arange(0, rows))
    z = dem_array

    trace = go.Surface(z=z, x=x, y=y, colorscale="Viridis")
    layout = go.Layout(
        scene=dict(
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=0.5),
        ),
        width=1000,  # Adjust the width
        height=1000,  # Adjust the height
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig


def main():
    st.title("2D and 3D DEM Visualization")

    uploaded_file = st.file_uploader(
        "Upload a TIF image", type=["tif", "tiff"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_contents = uploaded_file.read()

        # Open the image using BytesIO
        dem_array, transform = read_dem(BytesIO(file_contents))

        # Display the 2D DEM
        st.subheader("2D Digital Elevation Model (DEM)")
        plot_dem_2d(dem_array)

        # Display the option for 3D view
        if st.button("Switch to 3D View"):
            # Display the 3D DEM
            st.subheader("3D Digital Elevation Model (DEM)")
            fig = plot_dem_3d(dem_array, transform)
            st.plotly_chart(fig)


if __name__ == "__main__":
    main()
