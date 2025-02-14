import streamlit as st
import pandas as pd
import plotly.express as px


def main():
    st.title(
        "Streamlit CSV Reader and Data Display with Enhanced Plotting and Statistics")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # Read CSV and plot options
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Display the DataFrame
        st.write("CSV Data:")
        st.dataframe(df)

        # Plotting options
        st.subheader("Plotting Options:")
        x_column = st.selectbox("Select x-axis column",
                                df.columns, key="x_column")
        y_column = st.selectbox("Select y-axis column",
                                df.columns, key="y_column")
        plot_type = st.selectbox("Select plot type", [
                                 "Line Plot", "Bar Plot", "Scatter Plot", "Box Plot", "Histogram"])
        color_column = st.selectbox(
            "Select color column (optional)", df.columns.insert(0, None), key="color_column")

        # Plot the selected columns using Plotly
        st.subheader("Plot:")
        if plot_type == "Line Plot":
            fig = px.line(df, x=x_column, y=y_column,
                          color=color_column, title="Line Plot")
        elif plot_type == "Bar Plot":
            fig = px.bar(df, x=x_column, y=y_column,
                         color=color_column, title="Bar Plot")
        elif plot_type == "Scatter Plot":
            fig = px.scatter(df, x=x_column, y=y_column,
                             color=color_column, title="Scatter Plot")
        elif plot_type == "Box Plot":
            fig = px.box(df, x=x_column, y=y_column,
                         color=color_column, title="Box Plot")
        elif plot_type == "Histogram":
            fig = px.histogram(
                df, x=x_column, color=color_column, title="Histogram")

        st.plotly_chart(fig)

        # Display statistics
        st.subheader("Statistics:")
        st.write(f"Mean of {y_column}: {df[y_column].mean()}")
        st.write(f"Median of {y_column}: {df[y_column].median()}")
        st.write(f"Standard Deviation of {y_column}: {df[y_column].std()}")
        st.write(f"Maximum of {y_column}: {df[y_column].max()}")
        st.write(f"Minimum of {y_column}: {df[y_column].min()}")


if __name__ == "__main__":
    main()
