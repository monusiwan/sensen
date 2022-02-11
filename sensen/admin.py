from django.contrib import admin
from .models import *

@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    list_display=['title','blog_body','created_date']
    
