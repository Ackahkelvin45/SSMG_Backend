from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Service, CustomerUser
from campaigns.models import CampaignManagerAssignment
from django.contrib.contenttypes.models import ContentType


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that includes user information in the token response.
    Adds user details like role, service, and profile information.
    """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom user data to the response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'full_name': self.user.full_name,
            'role': self.user.role,
            'phone_number': self.user.phone_number,
            'password_changed': self.user.password_changed,
            'profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
        }
        
        # Add service information if user has a service
        if self.user.service:
            data['user']['service'] = {
                'id': self.user.service.id,
                'name': self.user.service.name,
                'location': self.user.service.location,
                'total_members': self.user.service.total_members,
            }
        else:
            data['user']['service'] = None
        
        # Add role-specific information
        if self.user.is_campaign_manager:
            # For Campaign Managers, include assigned campaigns count
            data['user']['is_campaign_manager'] = True
            data['user']['assigned_campaigns_count'] = self.user.campaign_assignments.count() if hasattr(self.user, 'campaign_assignments') else 0
        else:
            data['user']['is_campaign_manager'] = False
        
        return data


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
        
        # Use the custom manager to create the user with a default password of "kelvin"
        user = CustomerUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password="kelvin",
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


class CampaignAssignmentSerializer(serializers.Serializer):
    """Serializer for campaign assignment - just provide the campaign name"""
    campaign_name = serializers.CharField(help_text="Campaign name (from any campaign type)")


class CampaignManagerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a campaign manager with campaign assignments.
    
    Note: Campaign Managers are NOT assigned to a specific service.
    They can fill data for their assigned campaigns across ALL services.
    Password is auto-generated (not exposed in the API).
    """
    profile_picture = serializers.ImageField(write_only=True, required=False, allow_null=True, use_url=True)
    campaign_assignments = serializers.CharField(write_only=True, required=True)  # Accept as string for multipart
    
    # Read-only fields for response
    assigned_campaigns = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomerUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'profile_picture',
            'campaign_assignments',
            'assigned_campaigns',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_campaign_assignments(self, value):
        """Parse and validate campaign assignments - handles both JSON string and list"""
        import json
        
        # If it's a string (from multipart/form-data), parse it
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError("campaign_assignments must be valid JSON.")
        
        # Now validate as before
        if not value or not isinstance(value, list):
            raise serializers.ValidationError("At least one campaign assignment is required.")
        
        # Import all campaign models
        from campaigns.models import (
            StateOfTheFlockCampaign, SoulWinningCampaign, ServantsArmedTrainedCampaign,
            AntibrutishCampaign, HearingSeeingCampaign, HonourYourProphetCampaign,
            BasontaProliferationCampaign, IntimateCounselingCampaign, TechnologyCampaign,
            SheperdingControlCampaign, MultiplicationCampaign, UnderstandingCampaign,
            SheepSeekingCampaign, TestimonyCampaign, TelepastoringCampaign,
            GatheringBusCampaign, OrganisedCreativeArtsCampaign, TangerineCampaign,
            SwollenSundayCampaign, SundayManagementCampaign
        )
        
        # All campaign models to check
        campaign_models = [
            StateOfTheFlockCampaign, SoulWinningCampaign, ServantsArmedTrainedCampaign,
            AntibrutishCampaign, HearingSeeingCampaign, HonourYourProphetCampaign,
            BasontaProliferationCampaign, IntimateCounselingCampaign, TechnologyCampaign,
            SheperdingControlCampaign, MultiplicationCampaign, UnderstandingCampaign,
            SheepSeekingCampaign, TestimonyCampaign, TelepastoringCampaign,
            GatheringBusCampaign, OrganisedCreativeArtsCampaign, TangerineCampaign,
            SwollenSundayCampaign, SundayManagementCampaign,
        ]
        
        # Validate each campaign name
        for assignment in value:
            if not isinstance(assignment, dict):
                raise serializers.ValidationError("Each assignment must be an object with campaign_name.")
            
            campaign_name = assignment.get('campaign_name')
            
            if not campaign_name:
                raise serializers.ValidationError("campaign_name is required for each assignment.")
            
            # Search for campaign by name in all campaign models
            campaign_found = False
            for campaign_model in campaign_models:
                if campaign_model.objects.filter(name__iexact=campaign_name).exists():
                    campaign_found = True
                    break
            
            if not campaign_found:
                raise serializers.ValidationError(
                    f"Campaign with name '{campaign_name}' does not exist in any campaign type."
                )
        
        return value


    def get_assigned_campaigns(self, obj):
        """Return list of assigned campaigns"""
        assignments = CampaignManagerAssignment.objects.filter(user=obj).select_related('content_type')
        return [
            {
                'id': assignment.id,
                'campaign_type': assignment.content_type.model_class().__name__,
                'campaign_id': assignment.object_id,
                'campaign_name': str(assignment.campaign) if assignment.campaign else None,
                'created_at': assignment.created_at
            }
            for assignment in assignments
        ]

    def create(self, validated_data):
        campaign_assignments = validated_data.pop('campaign_assignments')
        profile_picture = validated_data.pop('profile_picture', None)
        
        # Create campaign manager user with CAMPAIGN_MANAGER role
        # Note: service is intentionally set to None as Campaign Managers work across all services
        # Explicitly set password to "kelvin" for new Campaign Managers
        user = CustomerUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password="kelvin",
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            role='CAMPAIGN_MANAGER',
            service=None,  # Campaign Managers are not tied to a specific service
            profile_picture=profile_picture
        )
        
        # Import all campaign models
        from campaigns.models import (
            StateOfTheFlockCampaign, SoulWinningCampaign, ServantsArmedTrainedCampaign,
            AntibrutishCampaign, HearingSeeingCampaign, HonourYourProphetCampaign,
            BasontaProliferationCampaign, IntimateCounselingCampaign, TechnologyCampaign,
            SheperdingControlCampaign, MultiplicationCampaign, UnderstandingCampaign,
            SheepSeekingCampaign, TestimonyCampaign, TelepastoringCampaign,
            GatheringBusCampaign, OrganisedCreativeArtsCampaign, TangerineCampaign,
            SwollenSundayCampaign, SundayManagementCampaign
        )
        
        # All campaign models to search
        campaign_models = [
            StateOfTheFlockCampaign, SoulWinningCampaign, ServantsArmedTrainedCampaign,
            AntibrutishCampaign, HearingSeeingCampaign, HonourYourProphetCampaign,
            BasontaProliferationCampaign, IntimateCounselingCampaign, TechnologyCampaign,
            SheperdingControlCampaign, MultiplicationCampaign, UnderstandingCampaign,
            SheepSeekingCampaign, TestimonyCampaign, TelepastoringCampaign,
            GatheringBusCampaign, OrganisedCreativeArtsCampaign, TangerineCampaign,
            SwollenSundayCampaign, SundayManagementCampaign,
        ]
        
        # Create campaign assignments - automatically detect campaign type from name
        for assignment_data in campaign_assignments:
            campaign_name = assignment_data['campaign_name']
            
            # Find which campaign model this name belongs to
            for campaign_model in campaign_models:
                campaign = campaign_model.objects.filter(name__iexact=campaign_name).first()
                if campaign:
                    content_type = ContentType.objects.get_for_model(campaign_model)
                    
                    CampaignManagerAssignment.objects.create(
                        user=user,
                        content_type=content_type,
                        object_id=campaign.id
                    )
                    break  # Found the campaign, move to next assignment
        
        return user


class CampaignManagerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Campaign Manager users.
    Allows updating basic info and campaign assignments.
    
    Note: 
    - Cannot change role (must remain CAMPAIGN_MANAGER)
    - Cannot assign a service (Campaign Managers work across all services)
    - Can update campaign assignments (add/remove campaigns)
    """
    profile_picture = serializers.ImageField(write_only=True, required=False, allow_null=True, use_url=True)
    campaign_assignments = serializers.CharField(write_only=True, required=False)  # Accept as string for multipart
    
    # Read-only fields for response
    assigned_campaigns = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomerUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'profile_picture',
            'campaign_assignments',
            'assigned_campaigns',
            'updated_at'
        ]
        read_only_fields = ['id', 'username', 'updated_at']  # Username cannot be changed
    
    def validate_campaign_assignments(self, value):
        """Parse and validate campaign assignments - handles both JSON string and list"""
        import json
        
        # If it's a string (from multipart/form-data), parse it
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError("campaign_assignments must be valid JSON.")
        
        # Now validate as before
        if not value or not isinstance(value, list):
            raise serializers.ValidationError("At least one campaign assignment is required.")
        
        # Import all campaign models
        from campaigns.models import (
            StateOfTheFlockCampaign, SoulWinningCampaign, ServantsArmedTrainedCampaign,
            AntibrutishCampaign, HearingSeeingCampaign, HonourYourProphetCampaign,
            BasontaProliferationCampaign, IntimateCounselingCampaign, TechnologyCampaign,
            SheperdingControlCampaign, MultiplicationCampaign, UnderstandingCampaign,
            SheepSeekingCampaign, TestimonyCampaign, TelepastoringCampaign,
            GatheringBusCampaign, OrganisedCreativeArtsCampaign, TangerineCampaign,
            SwollenSundayCampaign, SundayManagementCampaign, EquipmentCampaign
        )
        
        # All campaign models to check
        campaign_models = [
            StateOfTheFlockCampaign, SoulWinningCampaign, ServantsArmedTrainedCampaign,
            AntibrutishCampaign, HearingSeeingCampaign, HonourYourProphetCampaign,
            BasontaProliferationCampaign, IntimateCounselingCampaign, TechnologyCampaign,
            SheperdingControlCampaign, MultiplicationCampaign, UnderstandingCampaign,
            SheepSeekingCampaign, TestimonyCampaign, TelepastoringCampaign,
            GatheringBusCampaign, OrganisedCreativeArtsCampaign, TangerineCampaign,
            SwollenSundayCampaign, SundayManagementCampaign, EquipmentCampaign,
        ]
        
        # Validate each campaign name
        for assignment in value:
            if not isinstance(assignment, dict):
                raise serializers.ValidationError("Each assignment must be an object with campaign_name.")
            
            campaign_name = assignment.get('campaign_name')
            
            if not campaign_name:
                raise serializers.ValidationError("campaign_name is required for each assignment.")
            
            # Search for campaign by name in all campaign models
            campaign_found = False
            for campaign_model in campaign_models:
                if campaign_model.objects.filter(name__iexact=campaign_name).exists():
                    campaign_found = True
                    break
            
            if not campaign_found:
                raise serializers.ValidationError(
                    f"Campaign with name '{campaign_name}' does not exist in any campaign type."
                )
        
        return value

    def get_assigned_campaigns(self, obj):
        """Return list of assigned campaigns"""
        assignments = CampaignManagerAssignment.objects.filter(user=obj).select_related('content_type')
        return [
            {
                'id': assignment.id,
                'campaign_type': assignment.content_type.model_class().__name__,
                'campaign_id': assignment.object_id,
                'campaign_name': str(assignment.campaign) if assignment.campaign else None,
                'created_at': assignment.created_at
            }
            for assignment in assignments
        ]

    def update(self, instance, validated_data):
        """Update Campaign Manager and their campaign assignments"""
        campaign_assignments = validated_data.pop('campaign_assignments', None)
        profile_picture = validated_data.pop('profile_picture', None)
        
        # Update basic user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if profile_picture:
            instance.profile_picture = profile_picture
        
        instance.save()
        
        # Update campaign assignments if provided
        if campaign_assignments is not None:
            # Import all campaign models
            from campaigns.models import (
                StateOfTheFlockCampaign, SoulWinningCampaign, ServantsArmedTrainedCampaign,
                AntibrutishCampaign, HearingSeeingCampaign, HonourYourProphetCampaign,
                BasontaProliferationCampaign, IntimateCounselingCampaign, TechnologyCampaign,
                SheperdingControlCampaign, MultiplicationCampaign, UnderstandingCampaign,
                SheepSeekingCampaign, TestimonyCampaign, TelepastoringCampaign,
                GatheringBusCampaign, OrganisedCreativeArtsCampaign, TangerineCampaign,
                SwollenSundayCampaign, SundayManagementCampaign, EquipmentCampaign
            )
            
            campaign_models = [
                StateOfTheFlockCampaign, SoulWinningCampaign, ServantsArmedTrainedCampaign,
                AntibrutishCampaign, HearingSeeingCampaign, HonourYourProphetCampaign,
                BasontaProliferationCampaign, IntimateCounselingCampaign, TechnologyCampaign,
                SheperdingControlCampaign, MultiplicationCampaign, UnderstandingCampaign,
                SheepSeekingCampaign, TestimonyCampaign, TelepastoringCampaign,
                GatheringBusCampaign, OrganisedCreativeArtsCampaign, TangerineCampaign,
                SwollenSundayCampaign, SundayManagementCampaign, EquipmentCampaign,
            ]
            
            # Delete existing assignments
            CampaignManagerAssignment.objects.filter(user=instance).delete()
            
            # Create new assignments
            for assignment in campaign_assignments:
                campaign_name = assignment.get('campaign_name')
                
                # Find the campaign by name across all models
                for campaign_model in campaign_models:
                    try:
                        campaign = campaign_model.objects.get(name__iexact=campaign_name)
                        content_type = ContentType.objects.get_for_model(campaign_model)
                        
                        CampaignManagerAssignment.objects.create(
                            user=instance,
                            content_type=content_type,
                            object_id=campaign.id
                        )
                        break  # Found and assigned, move to next
                    except campaign_model.DoesNotExist:
                        continue
        
        return instance
