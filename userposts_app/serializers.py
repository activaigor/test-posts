from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from userposts_app.models import Post
from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            data.update({"user": user})
            if not user:
                raise serializers.ValidationError("Authorization error. Check you credentials")
        else:
            raise serializers.ValidationError("Not all fields were provided")
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("username",)

    def create(self, data):
        data.update({"username": data.get("email")})
        data = dict(filter(lambda (x, y): x not in ("password",), data.iteritems()))
        user = User.objects.create(**data)
        user.set_password(data.get("password"))
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'



