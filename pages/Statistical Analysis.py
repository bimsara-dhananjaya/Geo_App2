import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go


def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None


def perform_t_test(sample, reference, confidence_interval=0.95):
    _, p_value = stats.ttest_ind(sample, reference)
    confidence_level = 1 - (1 - confidence_interval) / 2
    confidence_interval_values = stats.t.interval(confidence_level, len(
        sample) - 1, loc=np.mean(sample), scale=stats.sem(sample))
    return p_value, confidence_interval_values


def perform_anova(data, group_column, value_column):
    try:
        groups = [data[value_column][data[group_column] == group]
                  for group in data[group_column].unique()]
        _, p_value = stats.f_oneway(*groups)
        return p_value
    except Exception as e:
        st.error(f"Error performing ANOVA: {e}")
        return None


def perform_chi_square_test(observed, expected):
    _, p_value, _, _ = stats.chi2_contingency(observed, correction=False)
    return p_value


def perform_linear_regression(data, x_column, y_column):
    try:
        model = LinearRegression()
        x = data[x_column].values.reshape(-1, 1)
        y = data[y_column].values
        model.fit(x, y)
        return model.coef_[0], model.intercept_
    except Exception as e:
        st.error(f"Error performing Linear Regression: {e}")
        return None


def plot_histogram(data, column):
    fig = px.histogram(data, x=column, nbins=30, marginal="rug",
                       opacity=0.7, title=f"Histogram for {column}")
    return fig


def plot_boxplot(data, group_column, value_column):
    fig = px.box(data, x=group_column, y=value_column,
                 title=f"Boxplot for {value_column} by {group_column}")
    return fig


def plot_bar_chart(data, column1, column2):
    observed_values = pd.crosstab(data[column1], data[column2])
    fig = px.bar(observed_values, x=observed_values.index, y=observed_values.columns,
                 title=f"Bar Chart for {column1} vs {column2}")
    return fig


def plot_regression_scatter(data, x_column, y_column, slope, intercept):
    scatter_fig = px.scatter(data, x=x_column, y=y_column,
                             title=f"Scatter Plot for {x_column} vs {y_column}")
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=data[x_column], y=slope * data[x_column] + intercept, mode='lines', name='Regression Line'))
    line_fig.update_layout(
        title=f"Linear Regression Line for {x_column} vs {y_column}")
    return scatter_fig, line_fig


def main():
    st.title("CSV Statistical Analysis App")

    # File upload section
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    # Read CSV
    if uploaded_file is not None:
        df = read_csv(uploaded_file)

        # Display the DataFrame
        st.write("CSV Data:")
        st.dataframe(df)

        # Statistical Analysis Options
        st.subheader("Statistical Analysis Options:")
        analysis_type = st.selectbox("Choose Statistical Analysis", [
                                     't-Test', 'ANOVA', 'Chi-Square Test', 'Linear Regression'])

        if analysis_type in ['t-Test', 'ANOVA', 'Chi-Square Test']:
            column1 = st.selectbox('Select the first column', df.columns)
            column2 = st.selectbox('Select the second column', df.columns)

        elif analysis_type == 'Linear Regression':
            x_column = st.selectbox(
                'Select the independent variable (X)', df.columns)
            y_column = st.selectbox(
                'Select the dependent variable (Y)', df.columns)

        # Perform statistical analysis
        st.subheader('Statistical Analysis Result')

        if analysis_type == 't-Test':
            confidence_interval = st.slider(
                "Select Confidence Interval for T-Test", 0.01, 0.99, 0.95, 0.01)
            p_value_t_test, confidence_interval_t_test = perform_t_test(
                df[column1], df[column2], confidence_interval)
            st.write(f"P-Value (T-Test): {p_value_t_test}")
            st.write(
                f"Confidence Interval ({confidence_interval * 100}%): {confidence_interval_t_test}")

            # Plot histogram for t-Test
            histogram_fig = plot_histogram(df, column1)
            st.plotly_chart(histogram_fig)

        elif analysis_type == 'ANOVA':
            p_value_anova = perform_anova(df, column1, column2)
            if p_value_anova is not None:
                st.write(f"P-Value (ANOVA): {p_value_anova}")

                # Plot boxplot for ANOVA
                boxplot_fig = plot_boxplot(df, column1, column2)
                st.plotly_chart(boxplot_fig)

        elif analysis_type == 'Chi-Square Test':
            observed_values = pd.crosstab(df[column1], df[column2])
            expected_values = df[column2].value_counts(
            ).sort_index().values
            p_value_chi_square = perform_chi_square_test(
                observed_values, expected_values)
            st.write(f"P-Value (Chi-Square Test): {p_value_chi_square}")

            # Plot bar chart for Chi-Square Test
            bar_chart_fig = plot_bar_chart(df, column1, column2)
            st.plotly_chart(bar_chart_fig)

        elif analysis_type == 'Linear Regression':
            slope, intercept = perform_linear_regression(
                df, x_column, y_column)
            if slope is not None:
                st.write(
                    f"Linear Regression Equation: Y = {slope:.4f}X + {intercept:.4f}")

                # Plot scatter plot and regression line for Linear Regression
                scatter_fig, line_fig = plot_regression_scatter(
                    df, x_column, y_column, slope, intercept)
                st.plotly_chart(scatter_fig)
                st.plotly_chart(line_fig)


if __name__ == "__main__":
    main()
