from rest_framework import viewsets, status
from rest_framework.response import Response
from authtoken.permissions import HasTokenScope

from foobar import api
from ..serializers.purchase import (
    PurchaseRequestSerializer,
    PurchaseSerializer
)
from wallet.exceptions import InsufficientFunds


class PurchaseAPI(viewsets.ViewSet):
    permission_classes = (HasTokenScope('purchases'),)

    def create(self, request):
        serializer = PurchaseRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            purchase_obj = api.create_purchase(
                **serializer.as_purchase_kwargs()
            )

            if request.data.get('status', 'finalized') != 'pending':
                purchase_obj = api.finalize_purchase(purchase_obj.pk)

        except InsufficientFunds:
            return Response(
                'Insufficient funds',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PurchaseSerializer(purchase_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
