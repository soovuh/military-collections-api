from rest_framework import serializers
from .models import MilitaryCollections, Contributors


class ContributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['user_name', 'amount', "collection_id"]


class MilitaryCollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilitaryCollections
        fields = ['id', 'title', 'description', 'target_amount', 'link']
