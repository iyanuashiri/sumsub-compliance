from rest_framework import generics, permissions, viewsets, status

from sumsubapp.compliances.api.v1.serializers import DocumentSerializer
from sumsubapp.compliances.models import Document


class DocumentCreateView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)
