from .models import Product
from rest_framework import generics, mixins
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from api.mixins import StaffEditorPermissionMixin
from api.authentication import TokenAuthentication

class ProductListCreateAPIView(StaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication
    # ]
    # permission_classes = [permissions.IsAuthenticated] 
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] 

    def perform_create(self, serializer): 
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

product_detail_view = ProductDetailAPIView.as_view()

class ProductEditAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    lookup_field = 'pk' 

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_edit_view = ProductEditAPIView.as_view()

class ProductDestroyAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    lookup_field = 'pk' 

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()

class ProductListAPIView(StaffEditorPermissionMixin, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

product_list_view = ProductListAPIView.as_view()

@api_view(["GET", "POST"])
def product_alt_view(requests, pk=None, *args, **kwargs):
    method = requests.method
    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=requests.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid":"not good data"}, status=400)

class CreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    pass

class ProductMixinView(
    mixins.CreateModelMixin, 
    mixins.ListModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin, 
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.update(request, *args, **kwargs)
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.destroy(request, *args, **kwargs)
        return self.destroy(request, *args, **kwargs)
    
product_mixin_view = ProductMixinView.as_view()