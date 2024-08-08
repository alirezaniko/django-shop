from rest_framework import serializers
from .models import Attribute, Product, ProductAttribute, Tag, Category, Image
from django.contrib.auth.models import User


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name']


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'value']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']  # فرض می‌کنیم `image_url` فیلدی است که URL تصویر را برمی‌گرداند


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(source='product_attributes', many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'body', 'price', 'discount', 'images', 'created_at', 'updated_at',
            'tag', 'slug', 'sold', 'view', 'attributes'
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    sub = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'image', 'slug', 'show_in_home', 'show_in_home_no_product', 'products', 'sub']
