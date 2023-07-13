from django.contrib import admin
from .models import Portrait, Comment, Vote
# Register your models here.

admin.site.register(Portrait)
admin.site.register(Vote)
admin.site.register(Comment)
