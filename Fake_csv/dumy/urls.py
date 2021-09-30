from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # previous login view
    # path('login/', views.user_login, name='login'),
    path('new_schema', views.new_schema, name="new_schema"),
    path('hendler', views.hendler, name="hendler"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('<int:schema_id>/<str:username>/', views.edit_schema, name='edit_schema'),
    path('sets/<int:schema_id>/<str:username>/', views.schema_sets, name='schema_sets'),
]