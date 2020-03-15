from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views

router = DefaultRouter()
router.register('test-viewset', views.TestViewSet, base_name='test-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedItemViewSet)

urlpatterns = [
  path('test/', views.TestApiView.as_view()),
  path('login/', views.UserLoginApiView.as_view()),
  path('', include(router.urls))
]