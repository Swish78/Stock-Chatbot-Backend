import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('API_KEY')


def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant to provide stock-related information and analysis."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content