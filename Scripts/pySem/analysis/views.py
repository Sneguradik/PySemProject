import datetime
import io
import os
import numpy as np
import pandas
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import CreateDatasetForm, AddDataForm, ReportForm
from .models import DataSet, DataSetValue
import matplotlib.pyplot as plt


# Create your views here.
def index(request):
    datasets = DataSet.objects.all()
    return render(request, 'index.html', {'datasets': datasets})


def add_data(request):
    return render(request, 'add_dataset.html', {'addDataForm': CreateDatasetForm, 'insertDataForm': AddDataForm})


def get_dataset_view(request, dataset_id, page):
    per_page = 10

    dataset = DataSet.objects.get(id=dataset_id)
    pg = Paginator(DataSetValue.objects.filter(dataSet=dataset), per_page)

    page_data = {
        'dataset': dataset,
        'values': pg.page(page),
        'pages': list(range(1, pg.num_pages + 1)),
        'offset': (page - 1) * per_page
    }
    return render(request, 'dataset_page.html', page_data)


def calc_population(value, growth_rate, cary_capacity=125):
    return growth_rate * value * (1 - value / cary_capacity)


def avg_slide(arr, period):
    sma_array = []
    for i in range(len(arr) - period):
        sum_var = 0
        for j in range(period):
            sum_var += arr[i + j]

        sma_array.append(sum_var / period)

    return sma_array


def get_chart(request, dataset_id):
    r = request.GET.get('r')
    period = request.GET.get('period')

    dataset = DataSet.objects.get(id=dataset_id)
    vals = DataSetValue.objects.filter(dataSet=dataset).order_by('timestamp')

    plt.figure(figsize=(10, 5))
    dates = [val.timestamp for val in vals]
    values = [val.value for val in vals]

    plt.plot(dates, values, marker='o', label='Dataset')

    if r:
        if not period:
            period = 3

        r = float(r)
        data = [values[0]]

        for i in range(1, len(values)):
            data.append(calc_population(values[i], r))

        data = avg_slide(data, period)

        part = (data[0] - values[0]) / 5

        temp_data = [values[0]]

        for i in range(1, period):
            temp_data.append(part + temp_data[i-1])

        data = temp_data+data

        plt.plot(dates, data, marker='s', label='Prediction')

    plt.gcf().autofmt_xdate()

    plt.xlabel('Date')
    plt.ylabel('Population (thousands of heads)')
    plt.title('Population analysis')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="chart.png"'

    return response


def get_chart_data(request, dataset_id):
    dataset = DataSet.objects.get(id=dataset_id)
    vals = DataSetValue.objects.filter(dataSet=dataset).order_by('timestamp')

    resp = {
        'values': [val.value for val in vals],
        'labels': [val.timestamp.strftime('%m/%Y') for val in vals]
    }

    return JsonResponse(resp)


def create_dataset_values(f, dataset):
    print(dataset.id)
    extension = os.path.splitext(f.name)[1]
    match extension:
        case ".csv":
            ds = pandas.read_csv(f)
        case ".xlsx":
            ds = pandas.read_excel(f)
    print(ds)
    for val in ds.values:
        DataSetValue.objects.create(
            dataSet=dataset,
            value=val[3],
            timestamp=datetime.date(month=int(val[0][1:]), year=int(val[2]), day=1),
            country=val[1]
        )


def create_dataset(request):
    form = CreateDatasetForm(request.POST, request.FILES)

    if form.is_valid():
        id = np.random.randint(0, 2 ** 31 - 1)
        ds = DataSet.objects.create(name=form.cleaned_data['name'], description=form.cleaned_data['description'], id=id)
        ds.save()
        create_dataset_values(request.FILES['file'], ds)
        return HttpResponse()
    return None


def insert_dataset(request):
    form = AddDataForm(request.POST, request.FILES)
    if form.is_valid():
        ds = form.cleaned_data['dataset']
        create_dataset_values(request.FILES["file"], ds)

    return HttpResponse()


def get_report(request):
    if request.method == 'GET':
        return render(request, "report.html", {"form": ReportForm})
    if request.method == 'POST':

        form = ReportForm(request.POST)
        if form.is_valid():
            return get_file_report(request, form.cleaned_data['type'], form.cleaned_data['dataset'])


def get_file_report(request, report_type, ds):
    items = list(DataSetValue.objects.filter(dataSet=ds))

    buffer = io.BytesIO()
    dataframe = pandas.DataFrame(
        np.array(list(map(lambda a: np.array([a.timestamp.month, a.country, a.timestamp.year, a.value]), items))),
        columns=['month', 'geo', 'year', 'value'])

    match report_type:
        case "xlsx":
            dataframe.to_excel(buffer, index=False)
            buffer.seek(0, 0)
            return FileResponse(buffer, content_type="application/vnd.openxmlformats-officedocument")
        case "txt":
            strbuf = io.StringIO()
            strbuf.write(f"Name: {ds.name}\nDescription: {ds.description}\n")
            strbuf.write("\n" + "#" * 20 + "\n")
            dataframe.info(buf=strbuf)
            strbuf.write("\n" + "#" * 20 + "\n")
            strbuf.write(dataframe.describe().to_string())
            strbuf.write("\n" + "#" * 20 + "\n")
            strbuf.write(dataframe["value"].describe().to_string())
            strbuf.seek(0)

            return HttpResponse(strbuf, content_type=".txt")
        case "csv":
            dataframe.to_csv(buffer, index=False)
            buffer.seek(0, 0)
            return FileResponse(buffer, content_type=".csv")
