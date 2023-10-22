from typing import Any
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from django_resized import ResizedImageField
from hitcount.models import HitCountMixin,HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.shortcuts import reverse
from taggit.managers import TaggableManager
User=get_user_model()

class Author(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fullname=models.CharField(max_length=40,blank=True)
    slug=models.SlugField(max_length=400,unique=True,blank=True)
    bio=HTMLField()
    points=models.IntegerField(default=0)

    profile_pic=ResizedImageField(size=[50,80],quality=100,upload_to="authors",default=None,null=True,blank=True)
    def num_posts(self):
        return Post.objects.filter(user=self).count()
    def __str__(self):
        return self.fullname
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.fullname)
        super(Author,self).save(*args, **kwargs)
    

class Category(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=400,unique=True,blank=True)
    description=models.TextField(default="description")
    class Meta:
        verbose_name_plural="categories"
    def __str__(self):
        return self.title   
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Category,self).save(*args, **kwargs)

    def get_url(self):
        return reverse("posts",kwargs={
            "slug":self.slug
        })
    @property
    def num_posts(self):
        return Post.objects.filter(categories=self).count()

    @property
    def last_posts(self):
        return Post.objects.filter(categories=self).latest("date")
class Reply(models.Model):
    user=models.ForeignKey(Author,on_delete=models.CASCADE)
    content =models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content[:100]
    class Meta:
        verbose_name_plural="replies"
    

class Comment(models.Model):
    user=models.ForeignKey(Author,on_delete=models.CASCADE)
    content =models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    replies=models.ManyToManyField(Reply,blank=True)

    def __str__(self):
        return self.content[:100]
    
    

    
    
class Post(models.Model):

    title=models.CharField(max_length=400)
    slug=models.SlugField(max_length=400,unique=True,blank=True)
    user=models.ForeignKey(Author,on_delete=models.CASCADE)
    content=HTMLField()
    categories=models.ManyToManyField(Category)
    date=models.DateTimeField(auto_now_add=True)
    approved=models.BooleanField(default=False)
    hit_count_generic=GenericRelation(HitCount,object_id_field='object_pk',related_query_name='hit_count_generic_relation')

    tag=TaggableManager()
    comments=models.ManyToManyField(Comment,blank=True)
    approved = models.BooleanField(default=True)
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Post,self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse("detail",kwargs={
            "slug":self.slug
        })
    @property

    def num_comments(self):
        return self.comments.count()
    @property

    def last_reply(self):
        return self.comments.latest("date")