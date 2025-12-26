from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'parent', 'is_approved', 'likes', 'created_at', 'replies']
        read_only_fields = ['id', 'author', 'likes', 'created_at', 'replies']

    def get_replies(self, obj):
        qs = obj.replies.filter(is_approved=True)
        return CommentSerializer(qs, many=True, read_only=True).data

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user if request else None
        return Comment.objects.create(author=author, **validated_data)
