from rest_framework import serializers
from django.contrib.auth import get_user_model
from advertisements.serializers import AdvertisementShortListSerializer

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    verification_code = serializers.CharField(required=True, style={'input_type': 'verification_code'})


class SetPasswordSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(required=True, style={'input_type': 'password'})
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'role',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'Пользователь')
            )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)


# class AdvertisementProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Advertisement
#         fields = ['id', 'mark', 'model', 'price', 'is_active', 'created_at']  # укажи нужные поля

class UserProfileSerializer(serializers.ModelSerializer):
    active_advertisements = serializers.SerializerMethodField()
    inactive_advertisements = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'avatar', 'is_company',
            'registered_at', 'updated_at', 'registered_at',
            'active_advertisements', 'inactive_advertisements'
        ]

    def get_active_advertisements(self, obj):
        ads = obj.advertisements.filter(is_active=True)
        return AdvertisementShortListSerializer(ads, many=True).data

    def get_inactive_advertisements(self, obj):
        ads = obj.advertisements.filter(is_active=False)
        return AdvertisementShortListSerializer(ads, many=True).data
    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль указан неверно")
        return value

    # def validate_new_password(self, value):
    #     if len(value) < 8:
    #         raise serializers.ValidationError("Новый пароль должен содержать минимум 8 символов")
    #     return value