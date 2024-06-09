from django.urls import path
from .views import index, add_data, get_report, get_dataset_view, get_chart, create_dataset, insert_dataset

urlpatterns = [
    path('', index, name='index'),
    path('add_data', add_data, name='add_data'),
    path('get_report', get_report, name='get_report'),
    path('dataset/<int:dataset_id>/page/<int:page>', get_dataset_view, name='get_dataset'),
    path('dataset/chart/<int:dataset_id>', get_chart, name='get_chart'),
    path('dataset/create', create_dataset, name='create_dataset'),
    path('dataset/insert', insert_dataset, name='insert_dataset')
]
