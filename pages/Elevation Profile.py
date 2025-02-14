import streamlit as st
import rasterio
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt


def main():
    st.title("Line of Sight Analysis with Terrain Profile")

    uploaded_file = st.file_uploader(
        "Upload a TIF image", type=["tif", "tiff"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_contents = uploaded_file.read()

        # Open the image using BytesIO
        dem_data = rasterio.open(BytesIO(file_contents))
        dem_array = dem_data.read(1)
        transform = dem_data.transform

        # Get the coordinates of the two points for the line of sight analysis
        x1 = st.number_input("Enter the X coordinate of Point 1:", value=0.0)
        y1 = st.number_input("Enter the Y coordinate of Point 1:", value=0.0)
        x2 = st.number_input("Enter the X coordinate of Point 2:", value=100.0)
        y2 = st.number_input("Enter the Y coordinate of Point 2:", value=100.0)

        # Calculate the terrain profile along the line of sight
        profile = calculate_terrain_profile(
            dem_array, transform, x1, y1, x2, y2)

        # Plot DEM data with the line of sight
        plt.imshow(dem_array, cmap='gray')
        plt.plot([x1, x2], [y1, y2], color='red',
                 linewidth=2, label='Line of Sight')
        plt.colorbar()
        plt.title('Digital Elevation Model with Line of Sight')
        plt.legend()
        st.pyplot()

        # Plot terrain profile
        plt.figure()
        plt.plot(profile, label='Terrain Profile')
        plt.xlabel('Distance along Line of Sight')
        plt.ylabel('Elevation')
        plt.title('Terrain Profile along Line of Sight')
        plt.legend()
        st.pyplot()


def calculate_terrain_profile(dem_array, transform, x1, y1, x2, y2):
    # Calculate the number of steps for iteration based on the greater of dx or dy
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    # Calculate the increments for x and y
    x_inc = dx / steps
    y_inc = dy / steps

    # Start from the source point
    x = x1
    y = y1

    # Create an array to store the elevation values along the line of sight
    profile = []

    # Iterate over the cells between source and target
    for _ in range(int(steps)):
        x += x_inc
        y += y_inc

        # Append the elevation of the current point to the profile array
        elevation = dem_array[int(y), int(x)]
        profile.append(elevation)

    return profile


if __name__ == "__main__":
    main()
