from rest_framework import serializers
from .models import Service, CustomerUser

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'location', 'total_members']  


class UserSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = CustomerUser
        fields = [
            'id',
            'first_name',
            "username",
            'last_name',
            'email',
            'phone_number',
            'service',
            'created_at',
            'service',
            "role",
            "profile_picture",
            "password_changed"
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    service = serializers.IntegerField(write_only=True)
    profile_picture = serializers.ImageField(write_only=True,required=False,allow_null=True,use_url=True)


    class Meta:
        model = CustomerUser
        fields = [
            'first_name',
            'last_name',
            "username",
            'email',
            'phone_number',
            'service',
            'role',
            'profile_picture',
 ]

    def validate_service(self, value):
        if not Service.objects.filter(id=value).exists():
            raise serializers.ValidationError("Service does not exist.")
        return value

    def create(self, validated_data):
        service_id = validated_data.pop('service')
        service = Service.objects.get(id=service_id)
        profile_picture = validated_data.pop('profile_picture', None)
        
        # Use the custom manager to create the user
        user = CustomerUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            role=validated_data.get('role', 'PASTOR'),
            service=service,
            profile_picture=profile_picture
        )
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    service = serializers.IntegerField(required=False, write_only=True)
    profile_picture = serializers.ImageField(write_only=True,required=False,allow_null=True,use_url=True)      

    class Meta:
        model = CustomerUser
        fields = [
                    'first_name',
                    'last_name',
                    "username",
                    'email',
                    'phone_number',
                    'service',
                    'role',
                    'profile_picture',


                ]
       

    def validate_service(self, value):
        if not Service.objects.filter(id=value).exists():
            raise serializers.ValidationError("Service does not exist.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """Validate that the old password is correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        """Validate that new password and confirm password match"""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "New password and confirm password do not match."
            })
        
        # Ensure new password is different from old password
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({
                "new_password": "New password must be different from old password."
            })
        
        return data

    def save(self, **kwargs):
        """Update the user's password"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.password_changed = True  # Mark that password has been changed
        user.save()
        return user
