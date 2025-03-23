from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import groq
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client with debug info
api_key = os.environ.get('GROQ_API_KEY')
if not api_key:
    print("Warning: GROQ_API_KEY not found in environment variables")

groq_client = groq.Groq(api_key=api_key)

class SQLQueryGenerator:
    def __init__(self):
        self.table_schema = """
Table: transactions
Columns:
- Amount (numeric)
- user_id
- Transaction_Type (debit/credit)
- Bank_Name (string)
- Card_Type (sttring - debit card/credit card)
- Paid_To (string- paid to whome)
- Merchant(string- company name)
- Transaction_Mode()
- Transaction_Date (format: dd/mm/yy)
- Reference_Number
- Tag (string- shopping, food, travel,entertainment,health, utilities, drinks,
  rent, groceries, education, services,gift, others)
"""

    def generate_sql_query(self, user_question):
        prompt = f"""
Given this database schema:
{self.table_schema}

Convert this question to a SQL query: "{user_question}"

Important rules:
2. respond only if input is related to transactions
3. if question is not related to transactions, respond with 'Not a transaction related question'
4. if question is related to transactions, generate the SQL query
1. Use proper date format (dd/mm/yy)
2. For spending queries, use Transaction_Type = 'debit'
3. Include relevant columns only
4. Use proper aggregations when needed (SUM, AVG, etc.)
5. Return only the SQL query, no explanations

Example categories in Tag column:
- shopping (for Amazon, retail stores)
- food (for restaurants, Zomato)
- drinks (for bars, beverages)
- travel (for transportation)
- entertainment (for movies, events)
"""

        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a SQL expert. Generate only SQL queries without any explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-70b-8192",
            temperature=0.1,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()

@app.route('/convert', methods=['POST'])
def convert_query():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        if not api_key:
            return jsonify({'error': 'GROQ_API_KEY not configured'}), 500

        generator = SQLQueryGenerator()
        sql_query = generator.generate_sql_query(data['text'])
        
        return jsonify({
            'natural_language': data['text'],
            'sql_query': sql_query
        })

    except groq.GroqError as e:
        print(f"Groq API Error: {str(e)}")
        return jsonify({'error': f'Groq API Error: {str(e)}'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
