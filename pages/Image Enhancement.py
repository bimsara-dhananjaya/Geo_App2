import streamlit as st
import numpy as np
import tifffile
from PIL import Image, ImageEnhance, ImageOps
import io
import matplotlib.pyplot as plt


def plot_histogram(image, title):
    # Flatten the image array and plot the histogram
    plt.hist(image.flatten(), bins=256, range=[
             0, 256], density=True, color='gray', alpha=0.7)
    plt.title(f'Grayscale Distribution Curve - {title}')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot()


def main():
    st.title("Single TIFF Image Viewer with Enhancement")

    # File upload section
    tif_file = st.file_uploader(
        "Upload Grayscale TIFF Image", type=["tif", "tiff"])

    if tif_file:
        # Load TIFF image
        tif_image = tifffile.imread(tif_file)

        # Normalize pixel values to [0, 255] range
        normalized_image = (tif_image - tif_image.min()) / \
            (tif_image.max() - tif_image.min()) * 255

        # Convert to uint8 for display
        uint8_image = normalized_image.astype(np.uint8)

        # Display the original image
        st.image(uint8_image, caption="Original TIFF Image",
                 use_column_width=True)

        # Image enhancement methods
        enhancement_method = st.selectbox("Select Enhancement Method", [
                                          "Original", "Contrast", "Brightness", "Sharpness", "Histogram Equalization"])

        # Apply selected enhancement method
        if enhancement_method == "Contrast":
            contrast_factor = st.slider(
                "Contrast Factor", min_value=0.1, max_value=3.0, value=1.0)
            enhanced_image = ImageEnhance.Contrast(
                Image.fromarray(uint8_image)).enhance(contrast_factor)
        elif enhancement_method == "Brightness":
            brightness_factor = st.slider(
                "Brightness Factor", min_value=0.1, max_value=3.0, value=1.0)
            enhanced_image = ImageEnhance.Brightness(
                Image.fromarray(uint8_image)).enhance(brightness_factor)
        elif enhancement_method == "Sharpness":
            sharpness_factor = st.slider(
                "Sharpness Factor", min_value=0.1, max_value=3.0, value=1.0)
            enhanced_image = ImageEnhance.Sharpness(
                Image.fromarray(uint8_image)).enhance(sharpness_factor)
        elif enhancement_method == "Histogram Equalization":
            enhanced_image = ImageOps.equalize(
                Image.fromarray(uint8_image), mask=None)
        else:
            enhanced_image = uint8_image

        # Display the enhanced image
        st.image(enhanced_image,
                 caption=f"{enhancement_method} Enhanced", use_column_width=True)

        # Download button for the enhanced image as TIFF
        if st.button("Download Enhanced Image as TIFF"):
            enhanced_image_uint16 = (enhanced_image.astype(
                np.uint16) * (2**16 - 1) / 255).astype(np.uint16)
            enhanced_image_uint16 = np.stack(
                [enhanced_image_uint16, enhanced_image_uint16, enhanced_image_uint16], axis=-1)

            # Save as TIFF
            buffer = io.BytesIO()
            tifffile.imsave(buffer, enhanced_image_uint16)
            st.download_button(
                label="Download Enhanced Image",
                data=buffer.getvalue(),
                file_name="enhanced_image.tif",
                mime="image/tiff"
            )

        # Grayscale distribution curve buttons
        st.subheader("Grayscale Distribution Curves:")
        if st.button("Show Original Image Distribution Curve"):
            plot_histogram(uint8_image, "Original")
        if st.button("Show Enhanced Image Distribution Curve"):
            enhanced_image_uint8 = np.asarray(enhanced_image)
            plot_histogram(enhanced_image_uint8,
                           f"{enhancement_method} Enhanced")


if __name__ == '__main__':
    main()


def main():
    st.title("Single TIFF Image Viewer with Enhancement")

    # File upload section
    tif_file = st.file_uploader(
        "Upload Grayscale TIFF Image", type=["tif", "tiff"])

    if tif_file:
        # Load TIFF image
        tif_image = tifffile.imread(tif_file)

        # Normalize pixel values to [0, 255] range
        normalized_image = (tif_image - tif_image.min()) / \
            (tif_image.max() - tif_image.min()) * 255

        # Convert to uint8 for display
        uint8_image = normalized_image.astype(np.uint8)

        # Display the original image
        st.image(uint8_image, caption="Original TIFF Image",
                 use_column_width=True)

        # Image enhancement methods
        enhancement_method = st.selectbox("Select Enhancement Method", [
                                          "Original", "Contrast", "Brightness", "Sharpness", "Histogram Equalization"])

        # Apply selected enhancement method
        if enhancement_method == "Contrast":
            contrast_factor = st.slider(
                "Contrast Factor", min_value=0.1, max_value=3.0, value=1.0)
            enhanced_image = ImageEnhance.Contrast(
                Image.fromarray(uint8_image)).enhance(contrast_factor)
        elif enhancement_method == "Brightness":
            brightness_factor = st.slider(
                "Brightness Factor", min_value=0.1, max_value=3.0, value=1.0)
            enhanced_image = ImageEnhance.Brightness(
                Image.fromarray(uint8_image)).enhance(brightness_factor)
        elif enhancement_method == "Sharpness":
            sharpness_factor = st.slider(
                "Sharpness Factor", min_value=0.1, max_value=3.0, value=1.0)
            enhanced_image = ImageEnhance.Sharpness(
                Image.fromarray(uint8_image)).enhance(sharpness_factor)
        elif enhancement_method == "Histogram Equalization":
            enhanced_image = ImageOps.equalize(
                Image.fromarray(uint8_image), mask=None)
        else:
            enhanced_image = uint8_image

        # Display the enhanced image
        st.image(enhanced_image,
                 caption=f"{enhancement_method} Enhanced", use_column_width=True)

        # Download button for the enhanced image as TIFF
        if st.button("Download Enhanced Image as TIFF"):
            enhanced_image_uint16 = (enhanced_image.astype(
                np.uint16) * (2**16 - 1) / 255).astype(np.uint16)
            enhanced_image_uint16 = np.stack(
                [enhanced_image_uint16, enhanced_image_uint16, enhanced_image_uint16], axis=-1)

            # Save as TIFF
            buffer = io.BytesIO()
            tifffile.imsave(buffer, enhanced_image_uint16)
            st.download_button(
                label="Download Enhanced Image",
                data=buffer.getvalue(),
                file_name="enhanced_image.tif",
                mime="image/tiff"
            )


if __name__ == '__main__':
    main()
