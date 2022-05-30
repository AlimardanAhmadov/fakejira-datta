# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.authentication.urls")),
    path("", include("apps.home.urls")),
    path("", include("GraphQl.urls")),
    path('', include("river_admin.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
