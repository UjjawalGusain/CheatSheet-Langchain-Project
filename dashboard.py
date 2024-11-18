import streamlit as st
from app.components.data_loader import load_csv, load_google_sheet
import pandas as pd
from app.components.llm_handler import generate_resultant_df_from_model
from app.components.schema_creation import create_schema
import matplotlib.pyplot as plt

# Title
st.title("AI Agent Project: Automated Data Extraction")

# Side bar 
st.sidebar.header("Data Source")
data_source = st.sidebar.radio("Select data source", ("Upload CSV", "Connect Google Sheets"))

df = None

# Uploading CSV
try:
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            try:
                df = load_csv(uploaded_file)
            except FileNotFoundError:
                st.error("File not found. Please ensure the file exists.")
            except pd.errors.EmptyDataError:
                st.error("Uploaded CSV file is empty.")
            except pd.errors.ParserError:
                st.error("Error parsing the CSV file. Please check the file format.")
            except Exception as e:
                st.error(f"Error loading CSV file: {e}")
except Exception as e:
    st.error(f"An error occurred with the file upload: {e}")

# Connecting with Google Sheet
try:
    if data_source == "Connect Google Sheets":
        sheet_url = st.text_input("Enter Google Sheet URL")
        if sheet_url:
            try:
                df = load_google_sheet(sheet_url)
            except ValueError:
                st.error("Invalid Google Sheet URL provided.")
            except ConnectionError:
                st.error("Error connecting to Google Sheets. Please check your internet connection.")
            except Exception as e:
                st.error(f"Error connecting to Google Sheets: {e}")
except Exception as e:
    st.error(f"An error occurred with the Google Sheets connection: {e}")

# Previewing Data
if df is not None:
    try:
        st.write("Data Preview:")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error displaying data preview: {e}")

    query = st.text_input("Enter your prompt (e.g., 'Get me the email address of {company}')")

    schema = None
    try:
        schema = create_schema(df)
    except Exception as e:
        st.error(f"Error creating schema from data: {e}")

    if query:
        try:
            if schema is None:
                st.error("Schema creation failed. Cannot process the query.")
            else:
                format, result = generate_resultant_df_from_model(schema, query, df)

                if format == 'table' or format == 'truncated':
                    st.dataframe(result)  # Display DataFrame in Streamlit
                elif format == 'string':
                    st.write(result)  # Display the string
                elif format == 'bar' or format == 'pie':
                    st.pyplot(result)  # Display the bar plot
                else:
                    st.error(result)  # Display error message
        except ValueError as e:
            st.error(f"Error with the query processing: {e}")
        except TypeError as e:
            st.error(f"Data processing error: {e}")
        except Exception as e:
            st.error(f"Error processing the query with the AI agent: {e}")
    else:
        st.info("Please enter a query in the input box above.")
else:
    st.info("Please upload a file or connect a Google Sheet to begin.")
