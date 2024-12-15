from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),

    path('add_subject/', views.add_subject, name='add_subject'),
    path('subject/<int:id>/', views.subject_detail, name='subject_detail'),
    path('delete_subject/<int:id>/', views.delete_subject, name='delete_subject'),
]
