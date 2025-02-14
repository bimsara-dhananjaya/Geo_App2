import streamlit as st
import numpy as np
import tifffile
from PIL import Image
from skimage import exposure, img_as_ubyte
from skimage.filters import unsharp_mask


def main():
    st.title("RGB Composite TIFF Image Viewer")

    # File upload section
    red_tif_file = st.file_uploader(
        "Upload Red Grayscale TIFF Image", type=["tif", "tiff"])
    green_tif_file = st.file_uploader(
        "Upload Green Grayscale TIFF Image", type=["tif", "tiff"])
    blue_tif_file = st.file_uploader(
        "Upload Blue Grayscale TIFF Image", type=["tif", "tiff"])

    if red_tif_file and green_tif_file and blue_tif_file:
        # Load TIFF images
        red_image = tifffile.imread(red_tif_file)
        green_image = tifffile.imread(green_tif_file)
        blue_image = tifffile.imread(blue_tif_file)

        # Normalize pixel values to [0, 255] range
        normalized_red = (red_image - red_image.min()) / \
            (red_image.max() - red_image.min()) * 255
        normalized_green = (green_image - green_image.min()) / \
            (green_image.max() - green_image.min()) * 255
        normalized_blue = (blue_image - blue_image.min()) / \
            (blue_image.max() - blue_image.min()) * 255

        # Stack normalized images to create RGB composite
        rgb_image = np.stack(
            [normalized_red, normalized_green, normalized_blue], axis=-1).astype(np.uint8)

        # Display the RGB composite image
        st.subheader("Original RGB Composite Image")
        st.image(rgb_image, use_column_width=True)

        # Enhancement sliders
        st.subheader("Enhancement Controls")
        enhancement_level = st.slider(
            "Enhancement Level", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
        brightness_adjustment = st.slider(
            "Brightness Adjustment", min_value=0, max_value=10, value=5, step=1)
        histogram_equalization = st.slider(
            "Histogram Equalization", min_value=0, max_value=1, value=0, step=1)
        gamma_correction = st.slider(
            "Gamma Correction", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
        sharpness = st.slider(
            "Sharpness", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
        contrast_stretching = st.slider(
            "Contrast Stretching", min_value=0, max_value=10, value=0, step=1)

        # Apply brightness adjustment
        enhanced_image = exposure.adjust_gamma(
            rgb_image, brightness_adjustment / 10)

        # Apply histogram equalization
        if histogram_equalization == 1:
            enhanced_image = exposure.equalize_hist(enhanced_image)

        # Apply gamma correction
        enhanced_image = exposure.adjust_gamma(
            enhanced_image, gamma_correction)

        # Apply sharpness enhancement
        enhanced_image = img_as_ubyte(unsharp_mask(
            enhanced_image, radius=1, amount=sharpness))

        # Apply contrast stretching
        if contrast_stretching > 0:
            p2, p98 = np.percentile(
                enhanced_image, (contrast_stretching, 100 - contrast_stretching))
            enhanced_image = exposure.rescale_intensity(
                enhanced_image, in_range=(p2, p98))

        # Apply enhancement to the image
        enhanced_image = exposure.adjust_gamma(
            enhanced_image, enhancement_level)

        # Display the enhanced RGB composite image
        st.subheader("Enhanced RGB Composite Image")
        st.image(enhanced_image, use_column_width=True)


if __name__ == '__main__':
    main()
