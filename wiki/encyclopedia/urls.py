from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("new", views.create, name="create"),
    path("update/<str:title>", views.update, name="update"),
    path("random", views.random_page, name="random_page")
] 
