#product/serializers.py
from rest_framework import serializers
from .models import  Video, Video_word

class VideoSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Video        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함

        
class VideoWordSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Video_word        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함