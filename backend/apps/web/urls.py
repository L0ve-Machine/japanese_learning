from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('past-exams/', views.past_exams_view, name='past_exams'),
    path('past-exams/<int:year>/<int:session_number>/', views.past_exam_detail_view, name='past_exam_detail'),
    path('quiz/<int:year>/<int:session_number>/', views.quiz_view, name='quiz'),
    # 応急処置: 古いセッション番号を正しいセッション番号にリダイレクト
    path('quiz/2025/1/', views.redirect_to_correct_session, name='quiz_redirect'),
]