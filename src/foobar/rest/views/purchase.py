from rest_framework import viewsets, status
from rest_framework.response import Response
from authtoken.permissions import HasTokenScope

from foobar import api
from ..serializers.purchase import PurchaseSerializer
from wallet.exceptions import InsufficientFunds


class PurchaseAPI(viewsets.ViewSet):
    permission_classes = (HasTokenScope('purchases'),)

    def create(self, request):
        serializer = PurchaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            api.purchase(**serializer.as_purchase_kwargs())
        except InsufficientFunds:
            return Response(
                'Insufficient funds',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_200_OK)
