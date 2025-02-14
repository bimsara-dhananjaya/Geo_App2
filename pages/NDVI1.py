import streamlit as st
import numpy as np
import tifffile
import io
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def normalize_band(band):
    # Normalize the band to [0, 1]
    return (band - band.min()) / (band.max() - band.min())


def calculate_ndvi(red_band, nir_band):
    # Normalize Red and NIR bands
    red_band_norm = normalize_band(red_band)
    nir_band_norm = normalize_band(nir_band)

    # Ensure that the denominator is not zero
    denominator = np.where((nir_band_norm + red_band_norm)
                           == 0, 1, (nir_band_norm + red_band_norm))

    # Calculate NDVI
    ndvi = (nir_band_norm - red_band_norm) / denominator
    return ndvi


def classify_ndvi(ndvi):
    # Thresholds for water, vegetation, and soil classification
    water_threshold = 0.0
    vegetation_threshold = 0.2
    soil_threshold = 0.5

    # Classify based on NDVI values
    water_mask = ndvi < water_threshold
    vegetation_mask = (ndvi >= water_threshold) & (ndvi < vegetation_threshold)
    soil_mask = ndvi >= vegetation_threshold

    return water_mask, vegetation_mask, soil_mask


def plot_classified_image(image, mask, title, cmap):
    # Adjust vmin and vmax based on your data
    plt.imshow(image, cmap="viridis", vmin=-1, vmax=1)
    plt.imshow(np.ma.masked_where(~mask, mask), cmap=cmap,
               alpha=0.5)  # Adjust cmap as needed
    plt.colorbar(label="NDVI")
    plt.title(title)
    plt.axis('off')
    st.pyplot()


def main():
    st.title("NDVI Classification and Visualization")

    # File upload section for Red band image
    red_band_file = st.file_uploader(
        "Upload Red Grayscale TIFF Image", type=["tif", "tiff"])

    # File upload section for NIR band image
    nir_band_file = st.file_uploader(
        "Upload NIR Grayscale TIFF Image", type=["tif", "tiff"])

    if red_band_file and nir_band_file:
        # Load TIFF images
        red_band_image = tifffile.imread(red_band_file)
        nir_band_image = tifffile.imread(nir_band_file)

        # Calculate NDVI
        ndvi = calculate_ndvi(red_band_image, nir_band_image)

        # Display the normal NDVI plot
        plt.imshow(ndvi, cmap="viridis", vmin=-1, vmax=1)
        plt.colorbar(label="NDVI")
        plt.title("Normal NDVI Plot")
        plt.axis('off')
        st.pyplot()

        # Classify NDVI into water, vegetation, and soil
        water_mask, vegetation_mask, soil_mask = classify_ndvi(ndvi)

        # Create custom colormaps for water, vegetation, and soil
        water_cmap = ListedColormap(['blue'])
        vegetation_cmap = ListedColormap(['green'])
        soil_cmap = ListedColormap(['brown'])

        # Plot and display classified images with eye-catching colors
        plot_classified_image(ndvi, water_mask, "Water Bodies", water_cmap)
        plot_classified_image(ndvi, vegetation_mask,
                              "Vegetation", vegetation_cmap)
        plot_classified_image(ndvi, soil_mask, "Soil", soil_cmap)


if __name__ == '__main__':
    main()
