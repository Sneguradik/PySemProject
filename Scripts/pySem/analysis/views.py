import datetime
import os
import numpy as np
import pandas
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateDatasetForm, AddDataForm
from .models import DataSet, DataSetValue


# Create your views here.
def index(request):
    return render(request, 'index.html')


def add_data(request):
    return render(request, 'add_dataset.html', {'addDataForm': CreateDatasetForm, 'insertDataForm': AddDataForm})


def get_report(request):
    pass


def get_dataset_view(request, dataset_id, page):
    dataset = DataSet.objects.get(id=dataset_id)
    pg = Paginator(DataSetValue.objects.filter(dataSet=dataset),25)



    page_data = {
        'dataset': dataset,
        'values': pg.page(page),
        'pages': list(range(1,pg.num_pages+1)),
        'offset': (page-1)*25
    }
    return render(request, 'dataset_page.html', page_data)


def get_chart(request, dataset_id):
    pass

def create_dataset_values(f, dataset):
    print(dataset.id)
    extension = os.path.splitext(f.name)[1]
    match extension:
        case ".csv":
            ds = pandas.read_csv(f)
        case ".xlsx":
            ds = pandas.read_excel(f)

    for val in ds.values:

        DataSetValue.objects.create(
            dataSet=dataset,
            value=val[3],
            timestamp= datetime.date(month=int(val[0][1:]), year=int(val[2]), day=1),
            country=val[1]
        )




def create_dataset(request):
    form = CreateDatasetForm(request.POST, request.FILES)

    if form.is_valid():
        id = np.random.randint(0,2**31-1)
        ds = DataSet.objects.create(name=form.cleaned_data['name'], description=form.cleaned_data['description'], id=id)
        ds.save()
        create_dataset_values(request.FILES['file'],ds)
        return HttpResponse()
    return None


def insert_dataset(request):
    form = AddDataForm(request.POST, request.FILES)
    if form.is_valid():
        ds = form.cleaned_data['dataset']
        create_dataset_values(request.FILES["file"],ds)

    return HttpResponse()

