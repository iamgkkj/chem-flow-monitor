import os

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dataset
from .reports import build_dataset_report_pdf
from .serializers import DatasetSerializer
from .services import compute_summary, parse_equipment_csv


def _delete_dataset_files(dataset: Dataset) -> None:
    if not dataset.csv_file:
        return
    try:
        path = dataset.csv_file.path
    except Exception:
        return
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


class DatasetUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        upload = request.FILES.get('file') or request.FILES.get('csv')
        if upload is None:
            return Response({'detail': 'Missing file. Use form field `file`.'}, status=status.HTTP_400_BAD_REQUEST)

        df, error = parse_equipment_csv(upload)
        if error:
            return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            upload.seek(0)
        except Exception:
            pass

        summary = compute_summary(df)

        dataset = Dataset.objects.create(
            original_filename=getattr(upload, 'name', 'uploaded.csv'),
            csv_file=upload,
            total_count=summary['total_count'],
            avg_flowrate=summary['avg_flowrate'],
            avg_pressure=summary['avg_pressure'],
            avg_temperature=summary['avg_temperature'],
            type_distribution=summary['type_distribution'],
        )

        qs = Dataset.objects.order_by('-created_at')
        extras = list(qs[5:])
        for old in extras:
            _delete_dataset_files(old)
            old.delete()

        return Response(DatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)


class DatasetHistoryView(generics.ListAPIView):
    serializer_class = DatasetSerializer

    def get_queryset(self):
        return Dataset.objects.order_by('-created_at')[:5]


class DatasetDetailView(generics.RetrieveAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class DatasetReportView(APIView):
    def get(self, request, pk: int):
        dataset = generics.get_object_or_404(Dataset, pk=pk)
        pdf_bytes = build_dataset_report_pdf(dataset)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="dataset_{dataset.id}_report.pdf"'
        return response
