from django.urls import path

from . import views

app_name="wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/",views.view, name="view"),
    path("wiki/<str:title>/edit",views.edit, name="edit"),
    path("search",views.search, name="search"),
    path("view",views.view, name="view"),
    path("new_page",views.new_page, name= "new_page"),    
    path("random_page",views.random_select , name = "random_select"),
]
'''path("<str:title>",views.view, name="view"),
    path("existing_page_error",views.existing_page_error, name = "existing_page_error"),
'''