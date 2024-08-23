from rest_framework import generics, permissions, viewsets, status

from sumsubapp.compliances.api.v1.serializers import DocumentSerializer, ApplicantSerializer
from sumsubapp.compliances.models import Document, Applicant


class ApplicantCreateView(generics.CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DocumentCreateView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)
