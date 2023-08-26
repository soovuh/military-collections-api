from rest_framework import serializers
from .models import MilitaryCollections, Contributors


class ContributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['user_name', 'amount']


class MilitaryCollectionsSerializer(serializers.ModelSerializer):
    contributors = ContributorsSerializer(many=True, read_only=True)

    class Meta:
        model = MilitaryCollections
        fields = ['id', 'title', 'description', 'target_amount', 'link', 'contributors']

