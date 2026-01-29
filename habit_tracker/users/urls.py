from django.urls import path

from .views import UserProfileEditView, UserRegisterView, UserListView, UserDetailView, UserDeleteView, LoginView

app_name = "users"

urlpatterns = [
    path("profile/edit/", UserProfileEditView.as_view(), name="user_edit"),
    path("users/", UserListView.as_view(), name="user_list"),  # Список пользователей
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),  # Детальный просмотр пользователя
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),  # Удаление пользователя
    path("register/", UserRegisterView.as_view(), name="user_register"),  # Эндпоинт для регистрации пользователя
    path("api/login/", LoginView.as_view(), name="token_obtain_pair"),  # Эндпоинт для авторизации пользователя
]
