import requests

data = ''

resultado = requests.get(''.format(data))
print(resultado.status_code)
print(resultado.json())