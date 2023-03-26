import requests

city = "Krasnoyarsk,RU"
appid = "c46564d10a1f5fd5a404bb74b58ee294"
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()

print("Город:", city)

print(f'Текущая видимость: {data["visibility"]} м')
print(f'Текущая скорость ветра: {data["wind"]["speed"]} м/c')

res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()

for i in data['list']:
    print(f"Дата: {i['dt_txt']}")
    print(f'Видимость: {i["visibility"]} м')
    print(f'Текущая скорость ветра: {i["wind"]["speed"]} м/c')
    print("____________________________")
    
