# User 모델
from django.contrib.auth.models import User
# Django의 기본 패스워드 검증 도구
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
# Token 모델
from rest_framework.authtoken.models import Token
# 이메일 중복 방지를 위한 검증 도구
from rest_framework.validators import UniqueValidator
# Django의 기본 authenticate 함수  
# 우리가 설정한 DefaultAuthBackend인 TokenAuth 방식으로 유저를 인증해줌  
from django.contrib.auth import authenticate

# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        # 이메일 중복 검증
        validators = [UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        # 비밀번호 검증
        validators = [validate_password],
    )
    # 비밀번호 확인 필드
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    # 추가적으로 비밀번호 일치 여부 확인
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data
    
    def create(self, validated_data):
        # CREATE 요청에 대해 create 메소드를 오버라이딩
        # 유저를 생성하고 토큰을 생성하게 함
        user = User.objects.create_user(
            username = validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user