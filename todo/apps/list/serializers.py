from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import models
import base64
import pyotp
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(user):
    secret = base64.b32encode(user.encode())
    OTP = pyotp.TOTP(secret, interval=1000)
    return {'secret': secret, 'OTP': OTP.now()}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'is_verfied']

class LoginSerializer(TokenObtainPairSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data

        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = models.User
        fields = ["id", "first_name", "last_name", "email", "password", "password2", 'phone_number']
        # extra_kwargs = {}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "password fields didn't match."})
        key =  generate_otp(attrs['email'])  
        key1 = key['OTP']    
        send_mail(
                    'OTP Verification',
                    f"your otp is {key1}",
                    settings.EMAIL_HOST_USER,
                    ['priyank.sharma@consolebit.com'],
                    fail_silently=False,
        )         
        attrs['secret'] = key['secret']
        return attrs    


    def create(self, validated_data):
        user = models.User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                          last_name=validated_data['last_name'], phone_number=validated_data['phone_number'])
        
        user.set_password(validated_data['password'])
        # user.is_active = True
        user.save()
        return user    

# class UserVerificationSerializer(serializers.ModelSerializer):
#     email = serializers.CharField(max_length=225)

#     class Meta:
#         model = models.User
#         fields = ['email']

#     def validate_email_(self, attrs):
#         ModelClass = self.Meta.model
#         if not ModelClass.objects.filter(email_=attrs).exists():
#             raise serializers.ValidationError('user not exists')

#         return attrs  

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TodoList
        fields = ["id", "user", "task", "created", "modified", "completed"]

class ReadTodoListSerializer(serializers.ModelSerializer):
    completed = serializers.BooleanField(read_only=True)
    class Meta:
        model = models.TodoList
        fields = ["id", "task", "created", "modified", "completed"]

