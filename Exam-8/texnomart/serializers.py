from rest_framework import serializers
from .models import Category, Image, Comment, Product, ProductAttribute, Attribute, AttributeValue
from django.db.models import Avg
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.db.models.functions import Round
from django.contrib.auth.models import User


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'key']

class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value']


class ProductAttributeSerializer(serializers.ModelSerializer):
    key = AttributeSerializer(read_only=True)
    value = AttributeValueSerializer(read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['id', 'product', 'key', 'value']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attributes = ProductAttribute.objects.filter(product=instance).values_list('key_id', 'key__key',
                                                                                   'value_id',
                                                                                   'value__value')

        characters = [
            {
                'attribute_id': key_id,
                'key': key_name,
                'attribute_value_id': value_id,
                'value': value_name
            }
            for key_id, key_name, value_id, value_name in attributes]
        return characters



    def get_avg_rating(self, obj):
        avg_rating = Comment.objects.filter(product=obj).aggregate(avg_rating=Round(Avg('rating')))
        if avg_rating.get('avg_rating'):
            return avg_rating.get('avg_rating')
        return 0

    def get_comments_count(self, instance):
        count = Comment.objects.filter(product=instance).count()
        return count

    def get_is_liked(self, instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        return False
    

    def get_all_images(self, instance):
        images = Image.objects.all().filter(product=instance)
        all_images = []
        request = self.context.get('request')

        for image in images:
            all_images.append(request.build_absolute_uri(image.image.url))

        return all_images

    def get_primary_image(self, instance):
        image = Image.objects.filter(product=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

    class Meta:
        model = Product
        exclude = ('users_like',)



class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'updated_at', 'created_at']



class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'products']



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_primary', 'product']


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']



class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "password2"]
        extra_kwargs = {
            'password': {"write_only": True},
            'password2': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError({"detail": "User already exists!"})
        return username

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        
        if password != password2:
            raise ValidationError({"password2": "Both passwords must match"})
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user



