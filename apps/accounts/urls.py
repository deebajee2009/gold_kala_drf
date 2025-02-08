from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, \
    LoginView, \
    LogoutView, \
    CustomTokenRefreshView, \
    UserWalletAssetViewSet 

router = DefaultRouter()
router.register(r'user', UserWalletAssetViewSet, basename='user')
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]
