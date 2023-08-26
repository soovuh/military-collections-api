from django.db.models import F, Sum, DecimalField
from django.db.models.functions import Coalesce, Cast
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import MilitaryCollections, Contributors
from .serializers import MilitaryCollectionsSerializer, ContributorsSerializer


class CollectionsViewSet(ModelViewSet):
    """
    API endpoint for managing military collections.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = MilitaryCollections.objects.all()
    serializer_class = MilitaryCollectionsSerializer

    @action(detail=True, methods=['get'])
    def get_info(self, request, pk):
        """
        Retrieve detailed information about a collection and its contributors.
        """
        collection = get_object_or_404(MilitaryCollections, pk=pk)
        contributors = collection.contributors_set.all()
        serializer = self.get_serializer(collection)
        return Response({
            'collection': serializer.data,
            'contributors': ContributorsSerializer(contributors, many=True).data
        })

    @action(detail=False, methods=['get'])
    def underfunded_collections(self, request):
        """
        Retrieve underfunded military collections.
        """
        underfunded_collections = MilitaryCollections.objects.annotate(
            total_contributions=Cast(Coalesce(Sum('contributors__amount'), 0), DecimalField())
        ).filter(total_contributions__lt=F('target_amount'))

        serializer = self.get_serializer(underfunded_collections, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def funded_collections(self, request):
        """
        Retrieve funded military collections.
        """
        funded_collections = MilitaryCollections.objects.annotate(
            total_contributions=Cast(Coalesce(Sum('contributors__amount'), 0), DecimalField())
        ).filter(total_contributions__gte=F('target_amount'))

        serializer = self.get_serializer(funded_collections, many=True)

        return Response(serializer.data)


class ContributorsViewSet(ModelViewSet):
    """
    API endpoint for managing contributors to military collections.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer

    @action(detail=False, methods=['post'])
    def create_contributor(self, request, collection_id):
        """
        Create a new contributor for a specific military collection.
        """
        collection = MilitaryCollections.objects.get(id=collection_id)
        data = request.data.copy()
        data["collection_id"] = collection.id
        serializer = ContributorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(collection_id=collection)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
