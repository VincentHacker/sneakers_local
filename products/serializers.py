from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, CommentRating, Image, Brand, SneakersType, Like, Favorites

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class SnekersTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SneakersType
        fields = ['name']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['author', 'product', 'like']


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['author', 'product', 'favorites']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = CommentRating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['author'] = user

        return super().create(validated_data)
    

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['boots', 'image']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = ImageSerializer(instance.boots_image.all(), many=True).data
        rep['like'] = LikeSerializer(instance.like.all(), many=True).data
        rep['favorites'] = FavoritesSerializer(instance.favorites.all(), many=True).data
        rep['rating'] = ReviewSerializer(instance.comments.all(), many=True).data
        rep['comments'] = ReviewSerializer(instance.comments.all(), many=True).data

        rating = [dict(i)['rating'] for i in rep['rating']]
        like = sum([dict(i)['like'] for i in rep['like']])
        rep['like'] = like
        favorites = sum([dict(i)['favorites'] for i in rep['favorites']])
        rep['favorites'] = favorites
        if rating:
            rep['rating'] = round((sum(rating) / len(rating)), 2)
            return rep
        else:
            rep['rating'] = None
            return rep
