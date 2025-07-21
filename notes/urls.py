from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.NoteListView.as_view(), name="note_list"),
    path('create/', views.NoteCreateView.as_view(), name="note_create"),
    path('details/<int:pk>/', views.NoteDetailView.as_view(), name="note_details"),
    path('save_comment/', views.save_comment, name="save_comment"),   
    path('update/<int:pk>/', views.NoteUpdate.as_view(), name="note_update"),
]