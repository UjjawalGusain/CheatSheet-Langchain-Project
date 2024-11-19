
# AI Agent Project: Automated Data Extraction

This project leverages an AI agent for automated data extraction and processing. The system allows users to upload a CSV file or connect to a Google Sheet, then interact with the data using natural language queries. The agent generates Python code based on the query, executes the code to manipulate the data, and presents the result in various formats such as a table, plot, or string, or scrapes useful data for your file.




## Table of Content

- Introduction
- Features
- Installation
- Usage
- Project Structure
- Error Handling
- Licenses



## Features

- Data Source Selection: Choose between uploading a CSV file or connecting a Google Sheet.
- Natural Language Queries: Interact with the data using natural language queries (e.g., "Get me the email address of {company}").
- Dynamic Code Generation: The system generates Python code based on the query, which is then executed to manipulate the data.
- Output Formats: Results are displayed in different formats such as tables, plots (bar/pie), or strings, depending on the query.
- Error Handling: Robust error handling ensures smooth user interaction even in case of issues like invalid file formats or data manipulation errors.

## Deployment link
- [Cheatsheet App on Streamlit](https://cheatsheet-app.streamlit.app/)

## Installation

To run this project, you need Python 3.7 or later. The project uses several third-party libraries that can be installed via pip.

- Clone the repo
```bash
    git clone https://github.com/UjjawalGusain/CheatSheet-Langchain-Project.git
    cd Langchain-Web-Agent
```

- Install dependencies: Create a virtual environment and install the required libraries:
```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
```

- Set up Google Sheets API:
    - Obtain your Google API credentials by following the steps in Google Sheets API documentation.
    - Download the credentials.json file and place it in the root directory of the project.

- Run the application:
```bash
    streamlit run dashboard.py
```

After running this command, the application will start, and you can access it through your browser.

## API
This project utilizes multiple APIs to handle different operations, including data scraping and interaction with the model. The APIs integrated are:

- Groq API:

    - Model: llama-3.1-70b-versatile

    - Purpose: The Groq API is used to interact with the large language model for generating responses, executing operations on the dataset, and handling complex queries. The model llama-3.1-70b-versatile is utilized for efficient natural language understanding and generation, helping process queries and produce actionable results.

    - Usage: 
        - The API is called to process queries related to the data, including operations like extraction, filtering, and generating summaries. The response from the model helps in shaping the operations applied to the dataset.

        - The prompts used for the model are structured in a specific format to ensure the desired response and avoid errors during execution.

- Scraper API:

    - Purpose: The Scraper API is used to gather additional data from external sources and append this data to the dataset.

    - Usage:
        - Once the dataset is processed and the necessary operations are performed, the Scraper API helps to enrich the data with additional columns scraped from external resources. This is done by adding a "scraped" column to the DataFrame.

## Usage

### Upload Data:

- Select a data source from the sidebar: either Upload CSV or Connect Google Sheets.
    - If uploading a CSV, choose a file to upload. If connecting to Google Sheets, provide the URL of the sheet.

- Enter a Query:
    - In the main area of the app, enter a natural language query in the input box. For example, "Get me the email address of {company}".

- View Results:
    - Based on the query, the AI agent will generate Python code, apply it to the data, and return the result. Results can be displayed as tables, plots, or strings.
      
## Challenges Encountered
- Prompt Formatting and Complexity: A significant challenge was ensuring that the prompts passed to the model were correctly formatted and handled by the system. The model needed to generate accurate responses based on the structure and complexity of the queries. It was also important to maintain clarity and consistency in the way information was extracted and presented to the user, especially with complex queries.

- Managing Security Risks with LLMs: Leveraging large language models (LLMs) introduced potential security risks, particularly concerning data privacy and the handling of sensitive information. Ensuring that no confidential or private data was inadvertently exposed while interacting with the model was a critical aspect of the development process. We had to implement safeguards to minimize these risks while using LLMs for generating code and processing data.

## Demo video of the project:



https://github.com/user-attachments/assets/4c15fa45-ca7c-40ae-a142-3d6c7c5e7595

