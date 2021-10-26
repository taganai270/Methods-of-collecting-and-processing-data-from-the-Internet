import requests
import json

"""
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
   Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

url = 'https://api.nasa.gov/planetary/apod'
token = 'PAWKkcgETYGlxuIZRstN627rykVdWjoJVm1Xsk3j'

param_dict = {'param': 'data'}
response = requests.post(url, data=json.dumps(param_dict))
print(response)