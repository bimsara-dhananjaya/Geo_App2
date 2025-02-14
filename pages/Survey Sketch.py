import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


@st.cache(allow_output_mutation=True)
def get_session_state():
    return {'bearings': [], 'distances': []}


def dms_to_decimal(degrees, minutes, seconds):
    return degrees + minutes / 60 + seconds / 3600


def calculate_total_distance_and_angle(bearings, distances):
    total_distance = sum(distances)
    initial_bearing_decimal = dms_to_decimal(*bearings[0])
    final_bearing_decimal = dms_to_decimal(*bearings[-1])

    # Calculate angle between initial and final bearings
    angle = final_bearing_decimal - initial_bearing_decimal

    return total_distance, np.degrees(angle)


def calculate_displacement(bearings, distances):
    total_distance, _ = calculate_total_distance_and_angle(bearings, distances)
    displacement_x = total_distance * np.cos(np.radians(bearings[-1][0]))
    displacement_y = total_distance * np.sin(np.radians(bearings[-1][0]))

    return displacement_x, displacement_y


def calculate_area(bearings, distances):
    x, y = 0, 0
    area = 0

    for bearing, distance in zip(bearings, distances):
        bearing_decimal = dms_to_decimal(*bearing)
        dx = distance * np.cos(np.radians(bearing_decimal))
        dy = distance * np.sin(np.radians(bearing_decimal))

        area += x * dy - y * dx
        x, y = x + dx, y + dy

    return 0.5 * np.abs(area)


def visualize_bearings(bearings, distances):
    fig, ax = plt.subplots()

    x, y = 0, 0  # Starting point at (0, 0)

    for bearing, distance in zip(bearings, distances):
        bearing_decimal = dms_to_decimal(*bearing)
        dx = distance * np.cos(np.radians(bearing_decimal))
        dy = distance * np.sin(np.radians(bearing_decimal))
        ax.arrow(x, y, dx, dy, head_width=0.1,
                 head_length=0.1, fc='red', ec='red')
        ax.text(x + dx / 2, y + dy / 2,
                f'{bearing[0]}° {bearing[1]}\' {bearing[2]}"', ha='center', va='center')

        x, y = x + dx, y + dy  # Update the current position

    # Calculate and plot the area covered
    area_polygon = plt.Polygon(
        [(0, 0)] + visualize_bearings_area(bearings, distances))
    ax.add_patch(area_polygon)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    return fig


def visualize_bearings_area(bearings, distances):
    x, y = 0, 0
    points = []

    for bearing, distance in zip(bearings, distances):
        bearing_decimal = dms_to_decimal(*bearing)
        dx = distance * np.cos(np.radians(bearing_decimal))
        dy = distance * np.sin(np.radians(bearing_decimal))

        x, y = x + dx, y + dy
        points.append((x, y))

    return points


def main():
    st.title("Bearing Sketch Visualization")

    session_state = get_session_state()

    # User input for Bearings in degrees, minutes, and seconds
    degrees_input = st.text_input("Enter Degrees", "45")
    minutes_input = st.text_input("Enter Minutes", "0")
    seconds_input = st.text_input("Enter Seconds", "0")

    bearing = (float(degrees_input), float(
        minutes_input), float(seconds_input))

    # User input for Distance
    distance_input = st.text_input("Enter Distance", "1")
    distance = float(distance_input)

    # Button to add point and save
    if st.button("Add Point"):
        if 'bearings' not in session_state:
            session_state['bearings'] = []
        if 'distances' not in session_state:
            session_state['distances'] = []

        session_state['bearings'].append(bearing)
        session_state['distances'].append(distance)

    # Display entered data
    st.header("Entered Data")
    if 'bearings' in session_state and 'distances' in session_state:
        data = pd.DataFrame({'Bearings (DMS)': [f'{d[0]}° {d[1]}\' {d[2]}"' for d in session_state['bearings']],
                             'Distances': session_state['distances']})
        st.write(data)

    # Button to visualize data
    if st.button("Visualize Data") and 'bearings' in session_state and 'distances' in session_state:
        # Visualize sketch with bearings, angles, and distances
        fig = visualize_bearings(
            session_state['bearings'], session_state['distances'])
        st.pyplot(fig)

        # Display total distance, angle, displacement, and area between first and last points
        total_distance, angle = calculate_total_distance_and_angle(
            session_state['bearings'], session_state['distances'])
        displacement_x, displacement_y = calculate_displacement(
            session_state['bearings'], session_state['distances'])
        area = calculate_area(
            session_state['bearings'], session_state['distances'])

        st.subheader(f"Total Distance: {total_distance:.2f}")
        st.subheader(
            f"Angle between First and Last Bearings: {angle:.2f} degrees")
        st.subheader(f"Displacement (X): {displacement_x:.2f}")
        st.subheader(f"Displacement (Y): {displacement_y:.2f}")
        st.subheader(f"Area Covered: {area:.2f} square meters")

    # Button to clear entered data
    if st.button("Clear Data"):
        session_state.clear()


if __name__ == "__main__":
    main()
