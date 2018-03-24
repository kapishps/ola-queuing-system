from django import forms


class userinput(forms.Form):
    q = forms.IntegerField(required=True,label='Customer ID')