from rest_framework import serializers

from .models import Product, CommentRating, Brand, SneakersType, Like, Favorites

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
        fields = ['product', 'like']


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['product', 'favorites']


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
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['like'] = LikeSerializer(instance.like.all(), many=True).data
        represent['favorites'] = FavoritesSerializer(instance.favorites.all(), many=True).data
        represent['rating'] = ReviewSerializer(instance.comments.all(), many=True).data
        represent['comments'] = ReviewSerializer(instance.comments.all(), many=True).data
        rating = [dict(i)['rating'] for i in represent['rating']]
        represent['like'] = sum([dict(i)['like'] for i in represent['like']])
        represent['favorites'] = sum([dict(i)['favorites'] for i in represent['favorites']])
        if rating:
            represent['rating'] = round((sum(rating) / len(rating)), 2)
            return represent
        else:
            represent['rating'] = None
            return represent
