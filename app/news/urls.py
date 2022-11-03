from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsCategory.as_view(), name='category'),
    path('view_news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('createuser/', RegisterUser, name='createuser'),
    path('loginuser/', LoginUser, name='loginuser'),
    path('quite/', QuiteUser, name='quite'),

    # ------------------------------ Админка -------------------------------
    path('admin-panel/', HomeAdmin, name='admin-panel'),

    path('admin-panel/createnews/', CreateNews.as_view(), name='admin-panel-createnews'),
    path('admin-panel/listnews/', ListNews.as_view(), name='admin-panel-listnews'),
    path('admin-panel/editnews/<int:pk>/', EditNews.as_view(), name='admin-panel-editnews'),
    path('admin-panel/deletenews/<int:pk>/', DeleteNews.as_view(), name='admin-panel-deletenews'),

    path('admin-panel/createcategory/', CreateCategory.as_view(), name='admin-panel-createcategory'),
    path('admin-panel/listcategory/', ListCategory.as_view(), name='admin-panel-listcategory'),
    path('admin-panel/editcategory/<int:pk>/', EditCategory.as_view(), name='admin-panel-editcategory'),
    path('admin-panel/deletecategory/<int:pk>/', DeleteCategory.as_view(), name='admin-panel-deletecategory'),

    path('admin-panel/createuser/', CreateUser, name='admin-panel-createuser'),
    path('admin-panel/listuser/', ListUsers.as_view(), name='admin-panel-listuser'),
    path('admin-panel/edituser/<int:pk>/', EditUsers.as_view(), name='admin-panel-edituser'),
    path('admin-panel/deleteuser/<int:pk>/', DeleteUser.as_view(), name='admin-panel-deleteuser'),
]