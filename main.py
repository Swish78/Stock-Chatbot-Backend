# from fastapi import FastAPI
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
from fastapi import FastAPI, Request
from llm import generate_response
from stock_functions import function_mapping

app = FastAPI()


# @app.post("/stock-analysis")
# async def stock_analysis(request: Request):
#     data = await request.json()
#     ticker = data.get("ticker")
#     analysis_type = data.get("analysis_type")
#
#     # Call the appropriate stock-related function
#     function_output = function_mapping[analysis_type](ticker)
#
#     # Generate a response using the OpenAI API
#     prompt = f"Based on the following stock data: {function_output}, provide an analysis and insights."
#     response = generate_response(prompt)
#
#     return {"analysis": response}

def terminal_test():
    ticker = input("Enter stock ticker: ")
    analysis_type = input("Enter analysis type (e.g., get_stock_price, calculate_rsi): ")

    if analysis_type not in function_mapping:
        print("Invalid analysis type")
        return

    # Call the appropriate stock-related function
    function_output = function_mapping[analysis_type](ticker)

    # Generate a response using the OpenAI API
    prompt = f"Based on the following stock data: {function_output}, provide an analysis and insights."
    response = generate_response(prompt)

    print(response)