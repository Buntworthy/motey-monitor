import requests

root = 'http://api.openweathermap.org/data/2.5/weather'
query = {'q': 'Cambridge,uk'}

# Make the request
r = requests.get(root, params=query)
if r.status_code is 200:
	# Interpret the response
	result = r.json()
	print('Curent temp is: %f' % result['main']['temp'])
else:
	print('Something went wrong')