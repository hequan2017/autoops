from rest_framework import generics
from .models import asset
from .serializers import AssetSerializer
from rest_framework import permissions


class AssetList(generics.ListCreateAPIView):
	queryset = asset.objects.all()
	serializer_class = AssetSerializer
	permission_classes = (permissions.IsAdminUser,)
	

class AssetDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = asset.objects.all()
	serializer_class = AssetSerializer
	permission_classes = (permissions.IsAdminUser,)

