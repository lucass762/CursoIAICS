import requests

data = '2004-06-22' # Substitua por sua data de nascimento no formato AAAA-MM-DD

resultado = requests.get('https://api.nasa.gov/planetary/apod?api_key=vnMl7ciifUgMrnGdGgLP1rdffr0kF1sqYhIhroxM&date={}'.format(data))
print(resultado.status_code)
print(resultado.json())