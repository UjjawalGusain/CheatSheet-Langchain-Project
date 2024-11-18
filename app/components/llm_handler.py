from app.components.scraper import add_scraped_column
from app.templates.prompt_template import get_system_prompt
from app.components.code_executioner import apply_operations
import logging
import json
import pandas as pd
from app.components.llm_initializer import llm

logging.basicConfig(level=logging.INFO)
logging.info("Streamlit app started")

MAX_REQUEST_LOAD = 3


def generate_resultant_df_from_model(schema, query, df):
    prompt = get_system_prompt(schema=schema, query=query)

    try:
        response = llm.invoke(prompt)
        
        # Ensure response content is valid
        if not hasattr(response, 'content') or response.content is None:
            raise ValueError("Response from model does not contain valid content")

        generated_code = response.content  # Access the content attribute

        try:
            generated_code = generated_code.strip('```python').strip('```').strip()

            try:
                result = json.loads(generated_code)
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                return "Error decoding JSON"

        except Exception as e:
            logging.error(f"Error cleaning up generated code: {e}")
            return "Error processing the generated code"

        # Handle different result formats
        if result.get('action') == 'extract':
            if result.get('format') not in ['error', None]:
                try:
                    result_formatted = apply_operations(df, result['code'])
                    return result['format'], result_formatted
                except Exception as e:
                    logging.error(f"Error applying operations: {e}")
                    return 'error', "Error applying operations to the data"
            else:
                return result['format'], "Error. Please try again"
            
        elif result.get('action') == 'find':
            try:
                new_df = apply_operations(df, result['code'][0])
                logging.info(f"Length of new df: {len(new_df)}")

                if len(new_df) > MAX_REQUEST_LOAD:
                    warning_message = f"Warning: More than {MAX_REQUEST_LOAD} values won't be searched. Only the first {MAX_REQUEST_LOAD} rows will be processed."
                    logging.warning(warning_message)
                    return 'error', warning_message

                scraped_data = add_scraped_column(new_df, result)
                logging.info("We got scraped column")
                logging.info(f"Length of scraped data: {len(scraped_data)}")
                
                return 'table', scraped_data
            except Exception as e:
                logging.error(f"Error processing 'find' action: {e}")
                return 'error', "Error processing the 'find' action"

    except Exception as e:
        logging.error(f"Error invoking the model: {e}")
        return "Sorry, I could not generate the code."
