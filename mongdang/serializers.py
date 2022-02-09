from rest_framework import serializers
from .models import User, Note, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User        # User 모델 사용
        fields = '__all__'  # 모든 필드 포함


class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Note        # Note 모델 사용
        fields = '__all__'  # 모든 필드 포함


class CommentSerializer(serializers.ModelSerializer):
    note = NoteSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment     # Comment 모델 사용
        fields = '__all__'  # 모든 필드 포함
