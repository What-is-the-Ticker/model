import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('COINGECKO_API_KEY')

def fetch_coins():
    url = f'https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key={key}'
    headers = {
        'accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code {response.status_code}. Please check your API key.")
        return None

def fetch_data():
    coins = fetch_coins()
    if coins is None:
        return [] 

    dataset = []
    for coin in coins:
        coin_id = coin["id"]
        url = f'https://api.coingecko.com/api/v3/coins/{coin_id}?x_cg_demo_api_key={key}'
        headers = {
            'accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            coin_data = response.json()
            ticker = coin_data.get("symbol", "")  
            name = coin_data.get("name", "")  
            categories = ', '.join(coin_data.get("categories", []))  

            entry = {
                "input": f"{categories}",
                "output": f"Coin name: {name} Ticker: {ticker}",
                "instruction": "What is the ticker?"
            }

            dataset.append(entry)
        else:
            print(f"Request failed with status code {response.status_code} for coin {coin_id}")
            return dataset
    
    return dataset

def format_for_llm(dataset):
    formatted_data = []
    for entry in dataset:
        formatted_data.append({
            "input": entry["input"],
            "output": entry["output"],
            "instruction": entry["instruction"]
        })
    return formatted_data

def save_to_json(dataset, filename="dataset.json"):
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=4)
    print(f"Dataset saved to {filename}")

if __name__ == "__main__":
    data = fetch_data()
    if data:
        formatted_data = format_for_llm(data)
        save_to_json(formatted_data)
    else:
        print("No data available due to failed API request.")
