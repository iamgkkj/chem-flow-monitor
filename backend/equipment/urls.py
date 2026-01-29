from django.urls import path

from .views import DatasetDetailView, DatasetHistoryView, DatasetReportView, DatasetUploadView

urlpatterns = [
    path('datasets/upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('datasets/history/', DatasetHistoryView.as_view(), name='dataset-history'),
    path('datasets/<int:pk>/', DatasetDetailView.as_view(), name='dataset-detail'),
    path('datasets/<int:pk>/report/', DatasetReportView.as_view(), name='dataset-report'),
]
