from django.urls import path, include


urlpatterns = [
    path('accounts/', include("accounts.urls")),
    path('app/', include("app.urls"))
]

