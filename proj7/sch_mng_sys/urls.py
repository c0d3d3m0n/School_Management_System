from django.urls import path, include
from . import views
from rest_framework import routers
from .views import StudentViewSet, ResultViewSet

router=routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'results', ResultViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_student, name='register_student'),
    path('list/', views.list_students, name='list_students'),
    path('list/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('list/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('list/view/<int:student_id>/', views.view_student, name='view_student'),
    path('list/upload_result/<int:student_id>/', views.upload_result, name='upload_result'),
    path('list/show_result/<int:student_id>/', views.show_result, name='show_result'), 
    path('api/', include(router.urls)), 
]