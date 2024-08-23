from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response

from decouple import config

from sumsubapp.accounts.models import Account
from sumsubapp.compliances.api.v1.serializers import DocumentSerializer, ApplicantSerializer, ApplicantReadSerializer
from sumsubapp.compliances.models import Document, Applicant
from sumsubapp.sumsubapi.sumsub_api import SumSubAPI


api = SumSubAPI(app_token=config('SUMSUB_APP_TOKEN'), secret_key=config('SUMSUB_SECRET_KEY'))


class ApplicantCreateView(generics.CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DocumentCreateView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class VerificationStatusView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ApplicantReadSerializer

    def get(self, request, *args, **kwargs):
        account = Account.objects.get(pk=request.user.id)
        applicant = Applicant.objects.get(account=account)
        response = api.get_verification_status(applicant_id=applicant.applicant_id)
        data = {'data': response}
        serializer = self.serializer_class(data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
