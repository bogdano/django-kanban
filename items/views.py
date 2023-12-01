from django.shortcuts import render, redirect
from .models import Item, BoardList, Activity
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.views import View
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

# will need a view to capture sortable events and update boardlist models with new item order, and add and remove items
# will need a view to capture checkbox events to move items from boardlist to boardlist
# will need a simpler view for deletion events
# will need a view to capture new item creation events

# will need a view to capture item update events 

# all of the above views will create one of four types of activity records
# all views will return HTML snippets to update the DOM with HTMX

# worst case scenario, HTMX can just return the entire DIV for the boardlist, and we can replace the entire DIV in the DOM
# this would be simplest considering we're using sortable.js

def home_view(request):
  # insantiate boards
  if not BoardList.objects.filter(list_type='IDEAS').exists():
    BoardList.objects.create(list_type='IDEAS', name='Ideas')
  if not BoardList.objects.filter(list_type='TODO').exists():
    BoardList.objects.create(list_type='TODO', name='Todo')
  if not BoardList.objects.filter(list_type='DOING').exists():
    BoardList.objects.create(list_type='DOING', name='Doing')
  if not BoardList.objects.filter(list_type='DONE').exists():
    BoardList.objects.create(list_type='DONE', name='Done')
    
  board_lists = BoardList.objects.prefetch_related('items').all()
  # Modify each board list's items to be in reverse order
  for board_list in board_lists:
    board_list.ordered_items = board_list.items.all().order_by('-order')
  return render(request, 'home.html', {'board_lists': board_lists})

def board_view(request):
  return render(request, 'partials/board.html')

# create_item view will create a new item and add it to the ideas list
def create_item(request):
  if request.method == 'POST':
    content = request.POST.get('content')
    board = request.POST.get('board')
    # Get or create the 'IDEAS' board list
    board_list = BoardList.objects.get(list_type=board.upper())
    # Add the item to the board list
    order = board_list.items.all().count()+1
    item = Item.objects.create(content=content, author=request.user, date_added=timezone.now(), order=order)
    board_list.items.add(item)

    Activity.objects.create(item=item, user=request.user, action='CREATED', source_board='', destination_board='Ideas')

    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.all().order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists})

def delete_item(request, pk):
  if request.method == 'DELETE':
    item = Item.objects.get(pk=pk)
    Activity.objects.create(item=item, user=request.user, action='DELETED', source_board=item.boardlist.get().list_type, destination_board='')
    item.delete()
    return JsonResponse({'message': 'deleted successfully'})

def edit_item(request, pk):
  if request.method == 'GET':
    item = Item.objects.get(pk=pk)
    context = {
      'item': item
    }
    return render(request, 'partials/edit_item.html', context)

def cancel_edit_item(request, pk):
  if request.method == 'GET':
    item = Item.objects.get(pk=pk)
    context = {
      'item': item
    }
    return render(request, 'partials/item.html', context)

def update_item(request, pk):
  if request.method == 'POST':
    item = Item.objects.get(pk=pk)
    content = request.POST.get('content')
    item.content = content
    item.save()
    Activity.objects.create(item=item, user=request.user, action='UPDATED', source_board=item.boardlist.get().list_type, destination_board='')
    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.all().order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists})

def update_item_position(request):
  if request.method == 'POST':
    pk = request.POST.get('item_id')
    item = Item.objects.get(pk=pk)

    new_position = int(request.POST.get('new_position'))
    old_position = item.order

    new_board = request.POST.get('new_board')
    old_board = item.boardlist.get().list_type

    # shift order of items in boards
    items_to_shift = BoardList.objects.get(list_type=old_board).items.filter(order__gte=old_position).order_by('-order')
    for item_to_shift in items_to_shift:
      item_to_shift.order -= 1
      item_to_shift.save()
    items_to_shift = BoardList.objects.get(list_type=new_board).items.filter(order__gte=new_position).order_by('-order')
    for item_to_shift in items_to_shift:
      item_to_shift.order += 1
      item_to_shift.save()

    BoardList.objects.get(list_type=old_board).items.remove(item)
    item.order = new_position
    BoardList.objects.get(list_type=new_board).items.add(item)
    if new_board == 'DONE':
      item.checked = True
    item.save()

    Activity.objects.create(item=item, user=request.user, action='MOVED', source_board=old_board, destination_board=new_board)
    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.all().order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists})


def update_item_position_checked(request, pk):
  if request.method == 'POST':
    item = Item.objects.get(pk=pk)

    old_board = item.boardlist.get().list_type
    # set new board to be next board in list
    if old_board == 'IDEAS':
      new_board = 'TODO'
    elif old_board == 'TODO':
      new_board = 'DOING'
    elif old_board == 'DOING':
      new_board = 'DONE'
    elif old_board == 'DONE':
      new_board = 'DOING'

    new_position = BoardList.objects.get(list_type=new_board).items.count()+1
    old_position = item.order

    # shift order of items in boards
    items_to_shift = BoardList.objects.get(list_type=old_board).items.filter(order__gte=old_position).order_by('-order')
    for item_to_shift in items_to_shift:
      item_to_shift.order -= 1
      item_to_shift.save()

    # remove item from boardlist
    BoardList.objects.get(list_type=old_board).items.remove(item)
    item.order = new_position
    BoardList.objects.get(list_type=new_board).items.add(item)
    if new_board == 'DONE':
      item.checked = True
    item.save()

    Activity.objects.create(item=item, user=request.user, action='MOVED', source_board=old_board, destination_board=new_board)
    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.all().order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists})