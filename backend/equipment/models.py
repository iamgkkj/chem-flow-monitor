from django.db import models

 
class Dataset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255)
    csv_file = models.FileField(upload_to='datasets/')

    total_count = models.PositiveIntegerField(default=0)
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    type_distribution = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Dataset {self.id} ({self.original_filename})'
