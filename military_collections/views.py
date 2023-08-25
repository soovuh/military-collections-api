from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import MilitaryCollections, Contributors
from .serializers import MilitaryCollectionsSerializer, ContributorsSerializer



class CollectionsViewSet(ModelViewSet):
    queryset = MilitaryCollections.objects.all()
    serializer_class = MilitaryCollectionsSerializer

    # @action(detail=False, methods=["get"])
    # def list_collections(self, request):
    #     queryset = MilitaryCollections.objects.all()
    #     serializer = MilitaryCollectionsSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # @action(detail=False, methods=['get'])
    # def collections_with_remaining_amount(self, request):
    #     queryset = MilitaryCollections.objects.filter(target_amount__gt=models.F('current_amount'))
    #     serializer = MilitaryCollectionsSerializer(queryset, many=True)
    #     return Response(serializer.data)


class ContributorsViewSet(ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer

    @action(detail=False, methods=['post'])
    def create_contributor(self, request, collection_id):
        collection = MilitaryCollections.objects.get(id=collection_id)
        data = request.data.copy()
        data["collection_id"] = collection.id
        serializer = ContributorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(collection_id=collection)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



