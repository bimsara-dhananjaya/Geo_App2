import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Set title for the Streamlit app
st.title("Machine Learning Web App")

# File upload section
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Read CSV
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame
    st.write("CSV Data:")
    st.dataframe(df)

    # Data Cleaning
    st.subheader("Data Cleaning")

    # Handle Missing Values
    missing_values = df.isnull().sum()
    st.write("Missing Values:")
    st.write(missing_values)

    # Drop Rows with Missing Values
    drop_missing_rows = st.checkbox("Drop Rows with Missing Values")
    if drop_missing_rows:
        df = df.dropna()
        st.write("Rows with missing values have been dropped.")

    # Identify non-numeric columns
    non_numeric_columns = df.select_dtypes(exclude=['number']).columns.tolist()

    # Choose the target column
    target_column = st.selectbox("Select the target column", df.columns)

    # Preprocess the data
    if non_numeric_columns:
        st.warning("Non-numeric columns found. Preprocessing data...")

        # Encode categorical columns using LabelEncoder
        label_encoders = {}
        for col in non_numeric_columns:
            label_encoders[col] = LabelEncoder()
            df[col] = label_encoders[col].fit_transform(df[col])

    # Train-test split ratio
    train_test_split_ratio = st.slider(
        "Select Train-Test Split Ratio", 0.1, 0.9, 0.8, 0.05)

    # Feature Scaling
    scaler_choice = st.selectbox("Choose feature scaling method", [
                                 "None", "Standard Scaler", "Min-Max Scaler"])
    if scaler_choice == "Standard Scaler":
        scaler = StandardScaler()
    elif scaler_choice == "Min-Max Scaler":
        scaler = MinMaxScaler()

    # Splitting the data into features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Feature scaling
    if scaler_choice != "None":
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=1 - train_test_split_ratio, random_state=42)

    # Option to choose evaluation metric
    evaluation_metric = st.selectbox("Choose evaluation metric", [
                                     "Accuracy", "Precision", "Recall", "F1-score"])

    # Option to choose machine learning algorithm
    ml_algorithm = st.selectbox("Select the machine learning algorithm", [
                                'Random Forest', 'Logistic Regression', 'SVM'])

    # Option for hyperparameter tuning
    hyperparameter_tuning = st.checkbox("Enable Hyperparameter Tuning")

    # Machine Learning Algorithm
    st.subheader(f"Results for {ml_algorithm}")
    if ml_algorithm == 'Random Forest':
        if hyperparameter_tuning:
            # Hyperparameter tuning using GridSearchCV
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['auto', 'sqrt', 'log2']
            }
            clf = RandomForestClassifier()
            grid_search = GridSearchCV(clf, param_grid, cv=5, n_jobs=-1)
            grid_search.fit(X_train, y_train)
            clf = grid_search.best_estimator_
        else:
            clf = RandomForestClassifier()
    elif ml_algorithm == 'Logistic Regression':
        clf = LogisticRegression()
    elif ml_algorithm == 'SVM':
        clf = SVC()

    clf.fit(X_train, y_train)
    train_predictions = clf.predict(X_train)
    test_predictions = clf.predict(X_test)
    train_accuracy = accuracy_score(y_train, train_predictions)
    test_accuracy = accuracy_score(y_test, test_predictions)
    overall_accuracy = (train_accuracy + test_accuracy) / 2
    st.write(f"Training Accuracy (User Accuracy): {train_accuracy:.2f}")
    st.write(f"Test Accuracy (Production Accuracy): {test_accuracy:.2f}")
    st.write(f"Overall Accuracy: {overall_accuracy:.2f}")

    # Confusion Matrix
    st.subheader("Confusion Matrix - Test Data")
    cm_test = confusion_matrix(y_test, test_predictions)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_test, annot=True, fmt="d", cmap="Blues",
                xticklabels=label_encoders[target_column].classes_, yticklabels=label_encoders[target_column].classes_)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    st.pyplot(plt)

    # Prediction on new data
    st.subheader("Predict on New Data")

    # Create a form for entering new data
    new_data_form = st.form(key="new_data_form")
    new_data_features = {}
    for feature in df.columns:
        if feature != target_column:
            new_data_features[feature] = new_data_form.text_input(
                f"Enter {feature} for new data"
            )

    submitted = new_data_form.form_submit_button("Predict")

    if submitted:
        # Convert input to DataFrame
        new_data = pd.DataFrame([new_data_features])

        # Preprocess and scale the new data
        for col in non_numeric_columns:
            if col in new_data.columns:
                if new_data[col][0] in label_encoders[col].classes_:
                    new_data[col] = label_encoders[col].transform(
                        new_data[col])
                else:
                    # Handle unseen labels
                    new_data[col] = len(label_encoders[col].classes_)

        # Make sure new data has the same columns as the training data
        if scaler_choice != "None":
            new_data_scaled = scaler.transform(new_data)
        else:
            new_data_scaled = new_data
        column_names = df.drop(columns=[target_column]).columns
        new_data = pd.DataFrame(new_data_scaled, columns=column_names)

        # Make predictions on new data
        new_predictions = clf.predict(new_data)

        # Map numerical predictions to their corresponding class labels
        decoded_predictions = label_encoders[target_column].inverse_transform(
            new_predictions)

        # Display the predicted result
        st.subheader("Predicted Result:")
        st.write(decoded_predictions[0])
