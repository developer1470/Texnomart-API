from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from texnomart.models import Category,  Product
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Image, AttributeValue, Attribute, ProductAttribute
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
# from django.views.decorators.vary import vary_on_headers

from .serializers import (
    CategoryListSerializer,
    ProductSerializer,
    ImageSerializer,
    CategorySerializer, 
    AttributeSerializer, 
    AttributeValueSerializer,
    ProductAttributeSerializer
    )



class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        categories = Category.objects.all()
        serializers = CategoryListSerializer(categories, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class CategoryDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    model = Category
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    queryset = Category.objects.all()



class CategoryAdd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryChange(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class CategoryDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'



class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'



class ImageListView(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializers = ImageSerializer(images, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    
class ProductList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Product
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset
    
    # @method_decorator(cache_page(60*2))
    # def get(self, *args, **kwargs):
    #     return super().get(*args, **kwargs)
    



class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    model = Product
    serializer_class = ProductSerializer
    lookup_field = 'id'
    queryset = Product.objects.all()


class ProductEdit(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'


class ProductDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'



class AttributeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Attribute
    serializer_class = AttributeSerializer
    def get_queryset(self):
        queryset = Attribute.objects.all()
        return queryset


class AttributeValueView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    model = AttributeValue
    serializer_class = AttributeValueSerializer
    def get_queryset(self):
        queryset = AttributeValue.objects.all()
        return queryset



class ProductAttributesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductAttributeSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductAttribute.objects.filter(product_id=product_id)