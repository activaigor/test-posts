from django.conf.urls import url
from rest_framework import routers
from userposts_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'users')
router.register(r'posts', views.PostsViewSet, 'posts')

urlpatterns = [
    url(r'^signup/', views.CreateProfile.as_view(), name="signup"),
    url(r'^signin/', views.AuthTokenView.as_view(), name="signin")
]

urlpatterns += router.urls
