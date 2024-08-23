from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import views

from sumsubapp.accounts.models import Account
from sumsubapp.accounts.api.v1.serializers import AccountSerializer, AccountCreateSerializer, TokenCreateSerializer
from sumsubapp.accounts.utils import login_user, logout_user


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return AccountSerializer
        return AccountCreateSerializer


class TokenCreateAPIView(generics.GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """
    serializer_class = TokenCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token = login_user(request=request, user=user)
        data = {
            'auth_token': token.key,
            'email': user.email,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class TokenDestroyView(views.APIView):
    """
    Use this endpoint to logout user (remove user authentication token).
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TotalUsersDetailAPIView(generics.GenericAPIView):
    queryset = Account.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        total_users = self.queryset.count()
        data = {'total_users': total_users}
        return Response(data=data, status=status.HTTP_200_OK)
