from django import forms
from .models import Crawler_Filter
class Generate_Crawling(forms.ModelForm):

    class Meta:
        model = Crawler_Filter
        fields = ('ptag','ntag')