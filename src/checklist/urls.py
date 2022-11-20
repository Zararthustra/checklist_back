from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users', views.UsersMethods.as_view()),
    # path('users/<int:pk>', views.UserMethods.as_view()),

    path('category', views.CategoriesMethods.as_view()),
    path('category/<str:categoryId>', views.CategoryMethods.as_view()),
    path('category/<str:categoryId>/tasks', views.CategoryTasksMethods.as_view()),

    path('tasks', views.TasksMethods.as_view()),
    path('tasks/<str:taskId>', views.TaskMethods.as_view()),
]
