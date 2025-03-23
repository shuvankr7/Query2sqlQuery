import requests
import json

def send_query(text):
    url = 'http://localhost:5000/convert'
    headers = {'Content-Type': 'application/json'}
    data = {'text': text}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if response.status_code != 200:
            print(f"\nError Status Code: {response.status_code}")
            print(f"Error Details: {result.get('error', 'Unknown error')}")
            return
        
        print("\nInput Query:", result['natural_language'])
        print("\nGenerated SQL:", result['sql_query'])
        print("\n" + "="*50)
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure api.py is running.")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid response from server")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def main():
    # Example queries to test the API
    test_queries = [
        "How much did I spend on drinks last month?",
        "Show me all my shopping transactions from Amazon this month",
        "What's my total food spending in last year?",
        "When did I last use my credit card for entertainment?",
        "Show me all transactions above 1000 rupees from last month",
    ]
    
    print("Starting API queries...\n")
    
    for query in test_queries:
        send_query(query)
    
    # Interactive mode
    while True:
        print("\nEnter your query (or 'quit' to exit):")
        user_input = input("> ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        send_query(user_input)

if __name__ == "__main__":
    main()
