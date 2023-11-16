from django.db import models
from django.urls import reverse

# Create your models here.
class Item(models.Model):
    content = models.CharField(max_length=200)
    checked = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})
    
class IdeasList(models.Model):
    name = models.CharField(max_length=200)
    items = models.ManyToManyField(Item, related_name="ideaslist")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ideas_detail", kwargs={"pk": self.pk})

class TodoList(models.Model):
    name = models.CharField(max_length=200)
    items = models.ManyToManyField(Item, related_name="todolist")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("todo_detail", kwargs={"pk": self.pk})
    
class DoingList(models.Model):
    name = models.CharField(max_length=200)
    items = models.ManyToManyField(Item, related_name="doinglist")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("doing_detail", kwargs={"pk": self.pk})

class DoneList(models.Model):
    name = models.CharField(max_length=200)
    items = models.ManyToManyField(Item, related_name="donelist")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("done_detail", kwargs={"pk": self.pk})