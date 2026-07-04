"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ninja import NinjaAPI
from courses.api import router as courses_router # Import router yang baru dibuat
from ninja_simple_jwt.auth.views.api import mobile_auth_router

api = NinjaAPI(
    title="Simple LMS Extended API",
    description="API documentation for Simple LMS Final Project",
    version="1.0.0"
)

api.add_router("/auth/", mobile_auth_router)

@api.get("/ping")
def ping(request):
    return {"message": "LMS Backend is up and running!"}

# Daftarkan router courses ke path /api/courses/
api.add_router("/courses", courses_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
