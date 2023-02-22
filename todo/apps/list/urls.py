from django.urls import path, include
from . import views
from . import cron
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
router = DefaultRouter()
# router.register('otp', views.OtpView, basename='otp')
urlpatterns = [
    path('', include(router.urls)),
    path('', views.apiOverview, name="api-overview"),
    # path('task-list/', views.apiList, name="api-list"),
    # path('task-list/', views.ApiListView.as_view(), name="api-list"),
    path('task-list/', views.ApiListGenericView.as_view(), name="api-list"),
    # path('task-detail/<int:pk>', views.apiDetail, name="api-detail"),
    # path('task-detail/<int:pk>', views.APiRetrieveView.as_view(), name="api-detail"),
    path('task-detail/<int:pk>', views.ApiRetrieveGenericView.as_view(), name="api-detail"),
    # path('task-create/', views.apiCreate, name="api-create"),
    # path('task-create/', views.TaskCreateView.as_view(), name="api-create"),
    path('task-create/', views.TaskCreateGenericView.as_view(), name="api-create"),
    # path('task-update/<int:pk>', views.apiUpdate, name="api-update"),
    # path('task-update/<int:pk>', views.APiUpdateView.as_view(), name="api-update"),
    path('task-update/<int:pk>', views.ApiUpdateGenericView.as_view(), name="api-update"),
    # path('task-delete/<int:id>', views.apiDelete, name="api-Delete"),
    # path('task-delete/<int:id>', views.ApiDeleteView.as_view(), name="api-Delete"),
    path('task-delete/<int:id>', views.ApiDeleteGenericView.as_view(), name="api-Delete"),
    path('register/', views.ApiRegisterView.as_view(), name="register"),
    path('login/', views.LoginApiView.as_view(), name="login"),
    # path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signin/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('custom/', views.CustomTokenObtainPairView.as_view(), name='custom'),
    # path('otp/', views.OtpView.as_view(), name="otp"),    
    path('test/', cron.send_smd_whatsapp, name="test"),
    path('verify/', views.UserVerifyView.as_view(), name="verify"),
    
]
