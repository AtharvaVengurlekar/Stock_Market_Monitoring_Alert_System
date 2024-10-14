import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "Your Virtual Twilio Number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

STOCK_NAME = "TSLA"
COMPANY_NAME = "TESLA INC"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

# Get yesterday's stock market price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

# Get yesterday and day before yesterday's closing price
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# Calculate the difference
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = "🔺" if difference > 0 else "🔻"

# Calculate the percentage difference
diff_percentage = round((difference / float(yesterday_closing_price)) * 100, 2)
print(f"Percentage difference: {diff_percentage}%")

# If difference is significant, fetch news
if abs(diff_percentage) > 0:  # Changed to >= 0
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Get top 3 articles
    three_articles = articles[:3]

    # Format message for each article
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percentage}%\nHeadline: {article['title']}\nBrief: {article['description']}"
        for article in three_articles
    ]

    # Send messages using Twilio
    client = Client(TWILIO_SID, AUTH_TOKEN)

    for article in formatted_articles:
        try:
            message = client.messages.create(
                body=article,
                from_=VIRTUAL_TWILIO_NUMBER,
                to=VERIFIED_NUMBER
            )
            print(f"Message sent with SID: {message.sid}")
        except Exception as e:
            print(f"Error sending message: {e}")
