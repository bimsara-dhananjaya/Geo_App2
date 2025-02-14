import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV file


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


def main():
    st.title("Interactive 3D Graphs from CSV")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        # Load data
        data = load_data(uploaded_file)

        # Display the loaded data
        st.dataframe(data)

        # Select columns for 3D graph
        x_col = st.selectbox("Select X-axis column", data.columns)
        y_col = st.selectbox("Select Y-axis column", data.columns)
        z_col = st.selectbox("Select Z-axis column", data.columns)

        # Optional color column
        color_col = st.selectbox(
            "Select Color column (Optional)", data.columns.insert(0, "None"))

        # Choose 3D graph type
        graph_type_3d = st.selectbox("Select 3D Graph Type", [
                                     "3D Scatter Plot", "3D Line Chart", "3D Surface Plot"])

        # Create and display the selected 3D graph
        if color_col == "None":
            color_col = None

        if graph_type_3d == "3D Scatter Plot":
            fig_3d = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, color=color_col,
                                   size_max=18, opacity=0.7, title="3D Scatter Plot")
        elif graph_type_3d == "3D Line Chart":
            fig_3d = px.line_3d(data, x=x_col, y=y_col, z=z_col,
                                color=color_col, title="3D Line Chart")
        elif graph_type_3d == "3D Surface Plot":
            fig_3d = px.surface(data, x=x_col, y=y_col, z=z_col,
                                color=color_col, title="3D Surface Plot")

        st.plotly_chart(fig_3d)


if __name__ == "__main__":
    main()
