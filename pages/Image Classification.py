import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image  # Import the Image class from Pillow


def classify_image_colors(uploaded_file, num_colors):
    # Read the image from BytesIO
    img = Image.open(uploaded_file).convert('RGB')
    # Normalize pixel values to [0.0, 1.0]
    original_image = np.array(img) / 255.0

    # Reshape the image to a 2D array of pixels
    pixels = original_image.reshape((-1, 3))

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_

    # Assign each pixel to its nearest dominant color
    labels = kmeans.predict(pixels)
    classified_image = dominant_colors[labels].reshape(original_image.shape)

    return original_image, classified_image, dominant_colors.astype(int)


def display_color_classification(original_image, classified_image, dominant_colors):
    # Display the original image
    st.image(original_image, caption='Original Image', use_column_width=True)

    # Display the classified image
    st.image(classified_image, caption='Classified Image',
             use_column_width=True, clamp=True)

    # Display the dominant colors as color patches
    color_patches = np.zeros(
        (100, len(dominant_colors) * 100, 3), dtype=np.uint8)
    for i, color in enumerate(dominant_colors):
        # Normalize to [0.0, 1.0]
        color_patches[:, i * 100:(i + 1) * 100, :] = color / 255.0

    st.image(color_patches, caption='Dominant Colors',
             use_column_width=True, clamp=True)

# Streamlit app


def main():
    st.title('Image Color Classification App')

    # File uploader for image
    uploaded_file = st.file_uploader(
        "Choose an image file", type=["jpg", "jpeg", "png"])

    # Slider for selecting the number of dominant colors
    num_colors = st.slider(
        'Select the number of dominant colors', min_value=1, max_value=10, value=5)

    # Button to trigger color classification
    if st.button('Classify Image Colors'):
        if uploaded_file is not None:
            # Classify image colors
            original_image, classified_image, dominant_colors = classify_image_colors(
                uploaded_file, num_colors)

            # Display the results
            display_color_classification(
                original_image, classified_image, dominant_colors)


if __name__ == "__main__":
    main()
