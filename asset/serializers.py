from  rest_framework import serializers
from  .models import asset


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = asset
        fields = '__all__'
