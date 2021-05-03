"""movie_quotes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from apps.movie_quotes.views.LoginView import LoginView
from apps.movie_quotes.views.RegistrationView import RegistrationView
from apps.movie_quotes.views.MatchHistoryView import MatchHistoryView
from apps.movie_quotes.views.SearchByQuoteView import SearchByQuoteView
from apps.movie_quotes.views.UpdateHistoryView import UpdateHistoryView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('session/login/', LoginView.as_view()),
    path('session/registration/', RegistrationView.as_view()),

    path('movies/quote/', SearchByQuoteView.as_view()),
    path('movies/update-history/', UpdateHistoryView.as_view()),

    path('user/<slug:username>/', MatchHistoryView.as_view())
]
