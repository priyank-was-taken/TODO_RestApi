from django.urls import path
from . import views
from . import cron

urlpatterns = [
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
    path('test/', cron.send_smd_whatsapp, name="test"),
    
]