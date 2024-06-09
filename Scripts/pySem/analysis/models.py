from django.db import models

class DataSet(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DataSetValue(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    value = models.FloatField()
    timestamp = models.DateField()
    dataSet = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    country = models.CharField(max_length=16)

    def __str__(self):
        return self.dataSet.name + "/ " + self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
