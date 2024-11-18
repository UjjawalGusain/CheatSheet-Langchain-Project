import json
import logging 

def extract_column_options(df):
    return list(df.columns)

def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model as a JSON-formatted string.

    Returns:
        dict: dictionary with response data or an error message.
    """
    try:
        # Attempt to decode the JSON response
        return json.loads(response)
    except json.JSONDecodeError as e:
        # Log an error message if decoding fails
        logging.error(f"Failed to decode JSON response: {e}")
        logging.debug(f"Response content that failed to decode: {response}")
        return {"answer": "Invalid JSON response"}

