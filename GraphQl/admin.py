from django.contrib import admin
from .models import Shipping, State, Issue, FlowType


admin.site.register(Shipping)
admin.site.register(State)
admin.site.register(Issue)
admin.site.register(FlowType)