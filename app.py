from flask import Flask, request, jsonify
import freecurrencyapi
import os

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY not set in environment variables")

client = freecurrencyapi.Client(api_key)

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()

        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        cf = fetch_conversion_factor(source_currency, target_currency)

        final_amount = round(amount * cf, 2)

        return jsonify({
            "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
        })

    except Exception as e:
        return jsonify({
            "fulfillmentText": "Sorry, something went wrong 😅"
        })


def fetch_conversion_factor(source, target):
    result = client.latest(base_currency=source, currencies=[target])
    return result['data'][target]


if __name__ == "__main__":
    app.run()
