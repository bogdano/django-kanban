from django.db import models
from django.urls import reverse

# the base Item model, for all board items
class Item(models.Model):
    # text content
    content = models.CharField(max_length=200)
    # boolean to indicate if item is checked off (we can use this with HTML checkboxes)
    checked = models.BooleanField(default=False)
    # automatic timestamp for when item was created
    date_added = models.DateTimeField(auto_now_add=True)  
    # an author field which is a foreign key to the User model which Terrin created
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # an automatic timestamp for when item was last updated by a user (will take care of this in views.py)
    last_updated = models.DateTimeField(auto_now=True)
    # a foreign key to the User model which Terrin created, updated each time an item is moved to a new board
    updated_by = models.ForeignKey('auth.User', related_name='updated_by', null=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})
    
# this is a class for all the boards
class BoardList(models.Model):
    # these are the types of boards we'll have
    LIST_TYPES = [
        ('IDEAS', 'Ideas'),
        ('TODO', 'Todo'),
        ('DOING', 'Doing'),
        ('DONE', 'Done'),
    ]
    # the name of the board, a string
    name = models.CharField(max_length=200)
    # the type of board, from the array above
    list_type = models.CharField(max_length=5, choices=LIST_TYPES)
    # defining a many-to-many relationship between the Item model and the BoardList model
    items = models.ManyToManyField(Item, related_name="boardlist")

    def __str__(self):
        return f"{self.get_list_type_display()} - {self.name}"
    
class Activity(models.Model):
    # different types of actions which can be taken on an item
    ACTION_CHOICES = [
        ('CREATED', 'Created'),
        ('UPDATED', 'Updated'),
        ('MOVED', 'Moved'),
        ('DELETED', 'Deleted'),
    ]
    # activity records which user moved, updated, or deleted an item
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # activity records which item was acted upon
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # empty string which will store the name of the board from which an item was moved
    source_board = models.CharField(max_length=200)
    # empty string which will store the name of the board to which an item was moved
    destination_board = models.CharField(max_length=200)
    # automatic timestamp for when activity was created
    timestamp = models.DateTimeField(auto_now_add=True)

    # the string representation of an Activity object, based on the action taken
    def __str__(self):
        match self.action:
            case 'MOVED':
                return f"{self.user.username} moved {self.item.content} from {self.source_board} to {self.destination_board} at {self.timestamp}"
            case 'CREATED':
                return f"{self.user.username} created item {self.item.content} at {self.timestamp}"
            case 'UPDATED':
                return f"{self.user.username} updated item {self.item.content} at {self.timestamp}"
            case 'DELETED':
                return f"{self.user.username} deleted an item at {self.timestamp}"
