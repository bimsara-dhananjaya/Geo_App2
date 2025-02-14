import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt


def plot_color_distribution(image):
    # Convert BGR to RGB (OpenCV reads images in BGR format)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert image to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reshape the image to a 2D array of pixels (height * width, 3)
    pixels_rgb = image_rgb.reshape((-1, 3))
    pixels_gray = image_gray.reshape(-1)

    # Plot the color distribution for Red, Green, Blue, and Grayscale channels
    plt.figure(figsize=(15, 7))

    # Original Image
    plt.subplot(2, 3, 1)
    plt.imshow(image_rgb)
    plt.title('Original Image')
    plt.axis('off')

    # RGB Color Distribution
    plt.subplot(2, 3, 2)
    for i, color in enumerate(['Red', 'Green', 'Blue']):
        plt.plot(range(256), np.histogram(pixels_rgb[:, i], bins=256, range=(0, 256))[0],
                 label=f'{color} Channel', alpha=0.7, color=color.lower())
    plt.xlabel('Pixel Intensity (0 to 255)')
    plt.ylabel('Frequency')
    plt.title('RGB Color Distribution')
    plt.legend()

    # Grayscale Image
    plt.subplot(2, 3, 4)
    plt.imshow(image_gray, cmap='gray')
    plt.title('Grayscale Image')
    plt.axis('off')

    # Grayscale Color Distribution
    plt.subplot(2, 3, 5)
    plt.plot(range(256), np.histogram(pixels_gray, bins=256, range=(0, 256))[0],
             label='Grayscale', alpha=0.7, color='gray')
    plt.xlabel('Pixel Intensity (0 to 255)')
    plt.ylabel('Frequency')
    plt.title('Grayscale Color Distribution')
    plt.legend()

    plt.tight_layout()
    st.pyplot()


def display_image(image):
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
             caption='Uploaded Image', use_column_width=True)

# Streamlit app


def main():
    st.title('Color Distribution Line Graph and Grayscale Image App')

    # File uploader for image
    uploaded_file = st.file_uploader(
        "Choose an image file", type=["jpg", "jpeg", "png"])

    # Button to trigger color distribution and grayscale image display
    if st.button('Show Color Distribution and Grayscale Image'):
        if uploaded_file is not None:
            # Read the image
            image = cv2.imdecode(np.fromstring(
                uploaded_file.read(), np.uint8), 1)

            # Display the original image
            display_image(image)

            # Plot color distribution and grayscale image
            plot_color_distribution(image)


if __name__ == "__main__":
    main()
