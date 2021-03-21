from django import forms

# class editCharacter(forms.Form):
#     name = forms.CharField(help_text="Enter the character's name")
from django.contrib.auth.models import User
from django.forms import ModelForm

from characterSheets.models import Character, Saga


class editCharacter(ModelForm):
    class Meta:
        model = Character
        fields = ['name']

class changeSaga(ModelForm):
    class Meta:
        model = Saga
        fields = '__all__'

    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    storyGuide = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)

class changeCharacter(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'


