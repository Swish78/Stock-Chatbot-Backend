# from fastapi import FastAPI
# import requests
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json
import os
import re
from dotenv import load_dotenv
from stock_functions import function_mapping

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("API_KEY")

app = FastAPI()

class UserInput(BaseModel):
    selected_stock: str
    user_input: str

def generate_response(messages):
    """
    Generate a response using the OpenAI API.

    Args:
        messages (List[Dict[str, str]]): The messages to send to the API.

    Returns:
        str: The generated response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        max_tokens=150,  # Adjust the max_tokens parameter as needed
        temperature=0.7,  # Adjust the temperature parameter as needed
        stop=["\n", "User:", "System:"]  # Stop generation at certain tokens
    )

    return response.choices[0].message.content

def find_matching_function(prompt):
    """
    Find the matching stock function based on the user prompt using regex.

    Args:
        prompt (str): The user's prompt related to the stock.

    Returns:
        str: The name of the matching stock function.
    """
    patterns = {
        "get_stock_price": r"price|current price|stock price|price of",
        "get_stock_volume": r"volume|stock volume|trading volume|number of shares traded",
        "calculate_sma": r"SMA|simple moving average",
        "calculate_ema": r"EMA|exponential moving average",
        "calculate_rsi": r"RSI|relative strength index",
        "calculate_macd": r"MACD|moving average convergence divergence"
    }

    for func_name, pattern in patterns.items():
        if re.search(pattern, prompt, re.IGNORECASE):
            return func_name

    return None

def handle_user_input(selected_stock, prompt):
    """
    Handle user input and call the appropriate stock function based on the prompt.

    Args:
        selected_stock (str): The selected stock ticker.
        prompt (str): The user's prompt related to the stock.

    Returns:
        str: The result of the called function.
    """
    function_name = find_matching_function(prompt)

    if function_name:
        if function_name in function_mapping:
            result = function_mapping[function_name](selected_stock)
            return result
        else:
            return f"Error: Unknown function '{function_name}'."
    else:
        return "Error: No matching function found for the given prompt."

@app.post("/stock-info/")
async def get_stock_info(user_input: UserInput):
    selected_stock = user_input.selected_stock
    user_input_text = user_input.user_input

    if user_input_text.strip():
        result = handle_user_input(selected_stock, user_input_text)

        # Check if the user is comparing two stocks
        if "better than" in user_input_text.lower() or "worse than" in user_input_text.lower():
            comparison_result = compare_stocks(user_input_text, selected_stock, result)
            return {"result": comparison_result}
        else:
            function_context = get_function_context(user_input_text)
            messages = [
                {"role": "system", "content": f"You are asking about {selected_stock} stock."},
                {"role": "user", "content": f"Explain this result: {result} {function_context}"}
            ]
            response = generate_response(messages)
            return {"response": response}
    else:
        raise HTTPException(status_code=400, detail="Error: Please provide a valid input.")

def get_function_context(user_input):
    """
    Get additional context based on the function selected by the user.

    Args:
        user_input (str): The user input indicating the selected function.

    Returns:
        str: Additional context or commentary based on the function.
    """
    function_context = ""
    if "sma" in user_input.lower():
        function_context = "(Simple Moving Average is a commonly used indicator to analyze stock trends. A higher SMA value may indicate a bullish trend, while a lower value may suggest a bearish trend.)"
    # Add additional context for other functions as needed
    return function_context

def compare_stocks(user_input, selected_stock, result):
    """
    Compare two stocks based on the user input.

    Args:
        user_input (str): The user input containing the comparison query.
        selected_stock (str): The selected stock ticker.
        result (str): The result of the called function for the selected stock.

    Returns:
        str: The comparison result.
    """
    other_stock = None
    comparison_operator = None

    # Extract the other stock ticker and comparison operator from the user input
    for stock in ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]:
        if stock != selected_stock and stock.lower() in user_input.lower():
            other_stock = stock
            break

    if "better than" in user_input.lower():
        comparison_operator = "better than"
    elif "worse than" in user_input.lower():
        comparison_operator = "worse than"

    # Provide a simple comparison message
    if other_stock and comparison_operator:
        if result:
            return f"The {selected_stock} stock {result} is {comparison_operator} the {other_stock} stock."
        else:
            return f"Sorry, I couldn't retrieve the information to perform the comparison."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
