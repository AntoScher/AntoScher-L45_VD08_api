# импортируем Flask и библиотеку Request
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

# загружаем переменные окружения
load_dotenv()
api_key1 = os.getenv('API_KEY1')
api_key2 = os.getenv('API_KEY2')
api_key3 = os.getenv('API_KEY3')

# импортируем объект класса Flask
app = Flask(__name__)

# формируем путь и методы GET и POST
@app.route('/', methods=['GET', 'POST'])
# создаем функцию с переменной weather, где мы будем сохранять погоду
def index():
    weather = None
    news = None
    quote = None
    # формируем условия для проверки метода. Форму мы пока не создавали, но нам из неё необходимо будет взять только город.
    if request.method == 'POST':
        # этот определенный город мы будем брать для запроса API
        city = request.form['city']
        weather = get_weather(city)
        news = get_news()
    quote = get_random_quote()
    print(f"Quote: {quote}")  # Проверка данных цитаты
    return render_template("index.html", weather=weather, news=news, quote=quote)

# в функции прописываем город, который мы будем вводить в форме
def get_weather(city):
    api_key = os.getenv('API_KEY1')
    # адрес, по которому мы будем отправлять запрос. Не забываем указывать f-строку.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    # для получения результата нам понадобится модуль requests
    response = requests.get(url)
    # прописываем формат возврата результата
    return response.json()

def get_news():
    api_key = os.getenv('API_KEY2')
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    return response.json().get('articles', [])

def get_random_quote():
    url = "https://favqs.com/api/qotd"
    response = requests.get(url)
    #print(f"Status code: {response.status_code}")  # Проверка статуса ответа
    if response.status_code == 200:
        #print(f"Response JSON: {response.json()}")  # Проверка полного ответа JSON
        quote = response.json().get('quote', {})
        #print(f"Quote: {quote}")  # Проверка данных
        return quote
    else:
        print("Failed to fetch quote")
    return {}

if __name__ == '__main__':
    app.run(debug=True)
