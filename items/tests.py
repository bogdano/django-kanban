from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.shortcuts import render
from .models import Item, BoardList, Activity
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model


# Tests for the Item model
class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.content = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.content = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.content, 'The first (ever) list item')
        self.assertEqual(second_saved_item.content, 'Item the second')

# Tests for the BoardList model
class BoardListModelTest(TestCase):
    def test_saving_and_retrieving_boardlists(self):
        first_boardlist = BoardList()
        first_boardlist.name = 'The first (ever) boardlist'
        first_boardlist.save()

        second_boardlist = BoardList()
        second_boardlist.name = 'Boardlist the second'
        second_boardlist.save()

        saved_boardlists = BoardList.objects.all()
        self.assertEqual(saved_boardlists.count(), 2)

        first_saved_boardlist = saved_boardlists[0]
        second_saved_boardlist = saved_boardlists[1]
        self.assertEqual(first_saved_boardlist.name, 'The first (ever) boardlist')
        self.assertEqual(second_saved_boardlist.name, 'Boardlist the second')

# Tests for the Activity model
class ActivityModelTest(TestCase):
    def test_saving_and_retrieving_activities(self):
        first_activity = Activity()
        first_activity.action = 'CREATED'
        first_activity.save()

        second_activity = Activity()
        second_activity.action = 'DELETED'
        second_activity.save()

        saved_activities = Activity.objects.all()
        self.assertEqual(saved_activities.count(), 2)

        first_saved_activity = saved_activities[0]
        second_saved_activity = saved_activities[1]
        self.assertEqual(first_saved_activity.action, 'CREATED')
        self.assertEqual(second_saved_activity.action, 'DELETED')


# Tests for the delete_item view
class DeleteItemTest(TestCase):
    def test_can_delete_an_item(self):
        item = Item()
        item.content = 'A new item'
        item.save()

        response = self.client.post(f'/delete_item/{item.id}/')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().archived, True)

# Tests for the edit_item view
class EditItemTest(TestCase):
    def test_can_edit_an_item(self):
        item = Item()
        item.content = 'A new item'
        item.save()

        response = self.client.post(f'/edit_item/{item.id}/', data={'content': 'An edited item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().content, 'An edited item')


# Tests for the update_item_position view
class UpdateItemPositionTest(TestCase):
    def test_can_update_item_position(self):
        item = Item()
        item.content = 'A new item'
        item.save()

        response = self.client.post('/update_item_position/', data={'item_id': item.id, 'order': 1})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().order, 1)


