from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, default=1, on_delete=models.CASCADE)
    #    name = models.CharField(max_length=128, null=True)
    #    password = models.CharField(('password'), max_length=128)
    #    last_login = models.DateTimeField(('last login'), blank=True, null=True)уч
    rating = models.IntegerField(default=1)

    def update_rating(self):
        qry = Post.objects.filter(author=self)
        qry2 = Comment.objects.filter(by_user=self.user)
        for i in range(0, len(qry)):
            self.rating += qry[i].rating * 3
        for a in range(0, len(qry2)):
            self.rating += qry2[a].rating
        self.save()


#    is_active = True

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    name = models.CharField(max_length=128, null=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    is_news = models.BooleanField(default=0)
    #password = models.CharField(('password'), max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    header = models.CharField(max_length=128, null=True)
    text = models.TextField(max_length=1024, null=True)
    rating = models.IntegerField(default=1)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
            self.save()
        else:
            pass

    def preview(self):
        return (str(self.text[0:124]) + '...')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commented_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=1024, null=True)
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    comment_rating = models.IntegerField(default=1)
    rating = models.IntegerField(default=1)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
            self.save()
        else:
            pass