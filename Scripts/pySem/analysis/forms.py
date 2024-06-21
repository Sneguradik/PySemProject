import django.forms as forms
from .models import DataSet


class CreateDatasetForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}), max_length=128, label='Name')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-dark border-primary text-white'}), label='Description')
    file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control bg-dark border-primary text-white',
        'accept': ".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"}),
        label='File')


class AddDataForm(forms.Form):
    dataset = forms.ModelChoiceField(queryset=DataSet.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control bg-dark border-primary text-white'}), label='Dataset')
    file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control bg-dark border-primary text-white',
        'accept': ".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"}),
        label='File')


class ReportForm(forms.Form):
    dataset = forms.ModelChoiceField(queryset=DataSet.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control bg-dark border-primary text-white'}), label='Dataset')
    type = forms.ChoiceField(choices=[('csv', 'CSV file'), ('txt', 'Text file')],
                             widget=forms.Select(attrs={'class': 'form-control bg-dark border-primary text-secondary'}))
