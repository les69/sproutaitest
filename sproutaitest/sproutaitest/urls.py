"""sproutaitest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from modelingestion.views import (blog_post_details_by_id,
                                  blog_post_details_by_title, ingest_blogpost)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', ingest_blogpost, name="ingest-blogpost"),
    path('posts/<int:blog_post_id>', blog_post_details_by_id, name="view_blogpost_by_id"),
    path('posts/<str:blog_title>', blog_post_details_by_title, name="view_blogpost_by_title")
]
