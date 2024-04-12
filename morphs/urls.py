from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('keywords/', views.run_test_script, name='run-test-script'),
    path('dict/', views.read_csv_file, name='read_csv_file'),
]