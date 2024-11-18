import os
from dotenv import load_dotenv
import requests
from app.components.llm_initializer import llm
import pandas as pd
from bs4 import BeautifulSoup
import time

# Load your API key from environment variables
load_dotenv()
api_key = os.getenv("SCRAPER_API_KEY")

import json

def get_most_relevant_link_snippet(search_results, query):
    """
    Uses the LLM to process a list of search results and find the most relevant link and snippet.
    Returns the relevant link and snippet in JSON format.
    """
    links_and_snippets = "\n".join([f"Link: {item['link']}, Snippet: {item['snippet']}" for item in search_results])
    
    # Include response format example in the prompt
    prompt = f"""
    I have conducted a search with the query "{query}" and gathered the top 10 search results.
    Each result includes a link and a snippet.

    Task: Please analyze the following links and snippets to identify the most relevant link and snippet for the provided query. If none of the results are relevant, return "N/A".

    You can create the snippet by yourself using the link justifying why that link is important.
    
    Search Results:
    {links_and_snippets}

    Response Format:
    Your response should be in the following JSON format:
    {{
        "link": "<Most Relevant Link>",
        "snippet": "<Corresponding Snippet>"
    }}

    Example Response:
    {{
        "link": "https://example.com",
        "snippet": "This is a relevant snippet from the search result."
    }}

    If no relevant link is found, respond with:
    {{
        "link": "N/A",
        "snippet": "N/A"
    }}

    Dont send anything except the JSON. Nothing else should be written.

    Most Relevant Link and Snippet:
    """

    try:
        response = llm.invoke(prompt)
        parsed_data = response.content.strip()
        parsed_data = json.loads(parsed_data)
        
        print(f"LLM Parsed Content: {type(parsed_data)}")

        # Check if the parsed data is 'N/A' or valid, and return in JSON format
        if "N/A" in parsed_data:
            return {"link": "N/A", "snippet": "N/A"}
        
        # If the data is valid, format it into JSON
        # Example: "Link: [url], Snippet: [snippet]"
        link = parsed_data['link'] or "N/A"
        snippet = parsed_data['snippet'] or "N/A"
        return {"link": link, "snippet": snippet}


    except Exception as e:
        print(f"Error during LLM parsing: {e}")
        return json.dumps({"link": "Error", "snippet": str(e)})


def find_data_for_each_row(row, target_data, result):
    """
    Finds and scrapes data for each row based on the target_data.
    """
    context_info = " ".join(f"{key}: {value}" for key, value in row.items() if key != target_data and pd.notna(value))
    query = f"{context_info} {target_data}"
    print(f"Constructed Query: {query}")

    # Initial search request
    url = "http://api.scraperapi.com"
    params = {
        "api_key": api_key,
        "url": f"https://www.google.com/search?q={query}"
    }
    
    response = requests.get(url, params=params)
    print(f"Response status code (initial search): {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Compile the top 10 results
        search_results = []
        for result_item in soup.find_all('div', class_='g')[:10]:  # Top 10 results
            link = result_item.find('a')['href'] if result_item.find('a') else None
            snippet = result_item.find('span').get_text() if result_item.find('span') else None
            if link:
                search_results.append({"link": link, "snippet": snippet})
        
        # Send search results to LLM to determine the most relevant link and snippet
        if search_results:
            parsed_data = get_most_relevant_link_snippet(search_results, query)
            return parsed_data if parsed_data else "N/A"
        else:
            return "Error: No valid links found in search results."
    else:
        return "Error: Could not fetch the data from the search results page."

def add_scraped_column(df, result):
    """
    Adds scraped columns to the original dataframe based on the 'result' dictionary.
    Populates 'link' and 'snippet' columns for each row with the most relevant information.
    """
    df = pd.DataFrame(df)
    target_data_list = result.get('target_data', [])
    if isinstance(target_data_list, str):
        target_data_list = [target_data_list]

    # Ensure 'link' and 'snippet' columns are present
    if 'link' not in df.columns:
        df['link'] = ""
    if 'snippet' not in df.columns:
        df['snippet'] = ""

    print(f"Target data list: {target_data_list}")
    
    for target_column in target_data_list:
        for index, row in df.iterrows():
            print(f"Index: {index}, Row: {row}")
            relevant_info = find_data_for_each_row(row, target_column, result)
            print(f'Link for this: {relevant_info['link']}')
            print(f'Snippet for this: {relevant_info['snippet']}')
            # Check if relevant_info has link and snippet structure
            if isinstance(relevant_info, dict) and 'link' in relevant_info and 'snippet' in relevant_info:
                df.at[index, 'link'] = relevant_info['link']
                df.at[index, 'snippet'] = relevant_info['snippet']
            else:
                df.at[index, 'link'] = "N/A"
                df.at[index, 'snippet'] = "N/A"
    
    return df
