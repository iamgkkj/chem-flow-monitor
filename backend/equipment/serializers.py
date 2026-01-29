from rest_framework import serializers

from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'id',
            'created_at',
            'original_filename',
            'csv_file',
            'total_count',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution',
        ]
