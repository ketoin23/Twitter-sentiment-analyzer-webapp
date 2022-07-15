from django import forms

class QueryForm(forms.Form):
	twitterquery = forms.CharField(max_length = 30)