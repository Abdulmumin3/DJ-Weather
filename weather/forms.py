from django import forms
from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):

	class Meta:
		model = City
		fields = ['name']
		widgets = {'name': TextInput(attrs={'class' : "w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500 required", "placeholder" : "Enter location"})}