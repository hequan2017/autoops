from  rest_framework import serializers
from  .models import asset


class AssetSerializer(serializers.ModelSerializer):
    assets_amount = serializers.SerializerMethodField()
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=asset.objects.all())

    class Meta:
        model = asset
        fields = '__all__'

