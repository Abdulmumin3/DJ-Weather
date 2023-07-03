import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.

def index(request):
	url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=586826f1cf7aad44ead4626853174eb3"
	# city = "London"
	err_messg = ''
	message = ''
	message_class = ''


	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing_city_count = City.objects.filter(name=new_city).count()

			if existing_city_count == 0:
				r = requests.get(url.format(new_city)).json()

				if r['cod'] == 200:
					form.save()
				else:
					err_messg = 'City does not exist in the world!'

			else:
				err_messg = 'The City already exists in the database!'

		if err_messg:
			message = err_messg
			message_class = 'bg-red-500'
		else:
			message = 'City added successfully'
			message_class = 'bg-green-500'

	print(err_messg)

	form = CityForm()

	weather_data = []

	cities = City.objects.all()
	for city in cities:
		r = requests.get(url.format(city)).json()
		
		city_weather = {
			'city': city.name,
			'temp': r["main"]["temp"],
			'code': r["sys"]["country"],
			'description': r['weather'][0]['description'],
			'icon': r['weather'][0]['icon'],
		}

		weather_data.append(city_weather)


	return render(request, 'index.html', {'city_weather': city_weather, 'weather_data': weather_data, 'form': form, 'message' : message, 'message_class' : message_class})