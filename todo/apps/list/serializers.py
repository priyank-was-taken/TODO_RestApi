from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email']

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
        fields = ["id", "first_name", "last_name", "email", "password", "password2"]
        # extra_kwargs = {}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "password fields didn't match."})
        return attrs    

    def create(self, validated_data):
        user = models.User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                          last_name=validated_data['last_name'])

        user.set_password(validated_data['password'])
        # user.is_active = True
        user.save()
        return user    

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TodoList
        fields = ["id", "user", "task", "created", "modified", "completed"]

class ReadTodoListSerializer(serializers.ModelSerializer):
    completed = serializers.BooleanField(read_only=True)
    class Meta:
        model = models.TodoList
        fields = ["id", "task", "created", "modified", "completed"]

