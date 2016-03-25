from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from userposts_app.models import Post
from userposts_app.serializers import AuthSerializer, UserSerializer, PostSerializer
from userposts_app.pagination import PostsPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=["get"], url_path="my")
    def my_user(self, request):
        data = self.get_queryset().filter(email=request.user.email).first()
        serializer = self.get_serializer(data, many=False)
        return Response(serializer.data)

class AuthTokenView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    serializer_class = AuthSerializer
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"auth_token": token.key})

class CreateProfile(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        data.update({"username": data.get("email")})
        user_fields = map(lambda x: getattr(x, "name", None), User._meta.fields)
        data = dict(filter(lambda (x, y): x in user_fields, data.iteritems()))
        data["is_active"] = True
        user = User.objects.create(**data)
        user.set_password(data.get("password"))
        user.save()
        return Response(data)

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title",)
    pagination_class = PostsPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @list_route(methods=["get"], url_path="my")
    def list_my_data(self, request):
        queryset = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
