from django.contrib import admin
from .models import User, Note, Comment


admin.site.register(User)
admin.site.register(Note)
admin.site.register(Comment)
