from rest_framework import serializers
from .models import Note, Comment


class NoteSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Note        # Note 모델 사용
        fields = '__all__'  # 모든 필드 포함


class CommentSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Comment     # Comment 모델 사용
        fields = '__all__'  # 모든 필드 포함
