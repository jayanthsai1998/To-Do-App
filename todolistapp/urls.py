from django.contrib import admin
from django.urls import path
from todolistapp.views import *
from todolistapp.apiviews import *

urlpatterns = [
    path('', HomeRedirectView.as_view()),

    path('signup/', SignUpController.as_view(), name='signup'),
    path('login/', LoginController.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('todolists/', ToDoListView.as_view(), name='todolists'),
    path('todolists/add/', ToDoListCreateView.as_view(), name='add_todolist'),

    path('todolists/<int:pk>/edit/', ToDoListUpdateView.as_view(), name='edit_todolist'),
    path('todolists/<int:pk>/delete/', ToDoListDeleteView.as_view(), name='delete_todolist'),

    path('todolists/<int:todolist_id>/', ToDoListItemListView.as_view(), name='todolistitem_list'),
    path('todolists/<int:todolist_id>/add/', ToDoListItemCreateView.as_view(), name='add_todolistitem'),
    path('todolists/<int:todolist_id>/items/<int:pk>/edit/', ToDoListItemUpdateView.as_view(),
         name='edit_todolistitem'),
    path('todolists/<int:todolist_id>/items/<int:pk>/delete/', ToDoListItemDeleteView.as_view(),
         name='delete_todolistitem'),

    # API URLS

    path('api/todolists/', ApiToDoListView.as_view(), name='api_todolists'),
    path('api/todolists/<int:pk>/', ApiToDoListDetails.as_view(), name='api_todolists_details'),
    path('api/todolists/<int:todolist_id>/items/', ApiToDoListItemListView.as_view(), name='api_todolistitem_list'),
    path('api/todolists/<int:todolist_id>/items/<int:pk>/', ApiToDoListItemDetails.as_view(),
         name='api_edit_todolistitem'),
]