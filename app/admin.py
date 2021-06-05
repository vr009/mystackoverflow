from django.contrib import admin

# Register your models here.
from .models import Answer, Question, Like, Profile, Tag

admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Answer)
admin.site.register(Tag)
