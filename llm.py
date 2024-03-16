import openai
import json
import os
import re
from dotenv import load_dotenv
from stock_functions import function_mapping

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("API_KEY")

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

def choose_stock():
    """
    Prompt the user to choose a stock ticker from a predefined list.

    Returns:
        str: The selected stock ticker.
    """
    stock_list = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]  # List of stock tickers

    print("Select a stock from the following list:")
    for i, ticker in enumerate(stock_list, start=1):
        print(f"{i}. {ticker}")

    choice = int(input("Enter the number corresponding to your choice: "))
    if 1 <= choice <= len(stock_list):
        return stock_list[choice - 1]
    else:
        print("Invalid choice. Please select a number within the range.")
        return choose_stock()

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

def main():
    selected_stock = choose_stock()

    while True:
        user_input = input(f"What would you like to know about {selected_stock} stock? (Type 'exit' to quit): ")

        if user_input.lower() in ["exit"]:
            print("Goodbye!")
            break

        if user_input.strip():
            result = handle_user_input(selected_stock, user_input)

            # Check if the user is comparing two stocks
            if "better than" in user_input.lower() or "worse than" in user_input.lower():
                comparison_result = compare_stocks(user_input, selected_stock, result)
                print(comparison_result)
            else:
                function_context = get_function_context(user_input)
                messages = [
                    {"role": "system", "content": f"You are asking about {selected_stock} stock."},
                    {"role": "user", "content": f"Explain this result: {result} {function_context}"}
                ]
                response = generate_response(messages)
                print(response)
        else:
            print("Error: Please provide a valid input.")

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
    main()
