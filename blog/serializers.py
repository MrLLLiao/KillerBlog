from rest_framework import serializers
from .models import Category, Tag, Post, BlogSetting


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, allow_null=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, source='tags', write_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'slug', 'excerpt', 'content', 'cover_image',
            'category', 'category_id', 'tags', 'tag_ids',
            'status', 'allow_comment', 'views', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'author', 'views', 'created_at', 'updated_at']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance


class BlogSettingSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BlogSetting
        fields = ['id', 'owner', 'title', 'subtitle', 'description', 'hero_image', 'theme', 'updated_at']
        read_only_fields = ['id', 'owner', 'updated_at']
