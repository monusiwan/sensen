from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    full_name= models.CharField(max_length=50)
    email = models.EmailField()

class BlogPage(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    blog_body = models.TextField(max_length=200000)
    image = models.ImageField(upload_to='myblogs')
    view_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=100,default='')
    author_user = models.ForeignKey(Author, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.title



