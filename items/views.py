from django.shortcuts import render, redirect
from .models import Item, BoardList, Activity
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model

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

  User = get_user_model()
  users = User.objects.all()
  activities = Activity.objects.all().order_by('-timestamp')[:10]    
  board_lists = BoardList.objects.prefetch_related('items').all()
  for board_list in board_lists:
    board_list.ordered_items = board_list.items.filter(archived=False).order_by('-order')
  return render(request, 'home.html', {'board_lists': board_lists, 'activities': activities, 'users': users})

def board_view(request):
  return render(request, 'board.html')

# create_item view will create a new item and add it to the ideas list
def create_item(request):
  if request.method == 'POST':
    content = request.POST.get('content')
    board = request.POST.get('board')
    # Get or create the 'IDEAS' board list
    board_list = BoardList.objects.get(list_type=board.upper())
    # Add the item to the board list
    order = board_list.items.filter(archived=False).count()+1
    item = Item.objects.create(content=content, author=request.user, order=order)
    board_list.items.add(item)
    Activity.objects.create(item=item, user=request.user, action='CREATED', source_board='', destination_board=board.upper())

    activities = Activity.objects.all().order_by('-timestamp')[:10]
    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.filter(archived=False).order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists, 'activities': activities})

def delete_item(request, pk):
  if request.method == 'POST':
    item = Item.objects.get(pk=pk)
    item.archived = True
    item.order = 0
    item.save()
    # get items to shift, all items with order greater than the order of the item to be deleted, and not archived
    items_to_shift = item.boardlist.get().items.filter(order__gt=item.order, archived=False).order_by('-order')
    for item_to_shift in items_to_shift:
      item_to_shift.order -= 1
      item_to_shift.save(update_fields=['order'])

    Activity.objects.create(item=item, user=request.user, action='DELETED', source_board=item.boardlist.get().list_type, destination_board='')
    activities = Activity.objects.all().order_by('-timestamp')[:10]
    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.filter(archived=False).order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists, 'activities': activities})

def edit_item(request, pk):
  if request.method == 'GET':
    item = Item.objects.get(pk=pk)
    return render(request, 'partials/edit_item.html', {'item': item})

def cancel_edit_item(request, pk):
  if request.method == 'GET':
    item = Item.objects.get(pk=pk)
    return render(request, 'partials/item.html', {'item': item})

def update_item(request, pk):
  if request.method == 'POST':
    item = Item.objects.get(pk=pk)
    content = request.POST.get('content')
    if item.content != content:
      item.content = content
      item.updated_by = request.user
      item.save()
      Activity.objects.create(item=item, user=request.user, action='UPDATED', source_board=item.boardlist.get().list_type, destination_board='')
    activities = Activity.objects.all().order_by('-timestamp')[:10]
    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.filter(archived=False).order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists, 'activities': activities})

def update_item_position(request):
  if request.method == 'POST':
    pk = request.POST.get('item_id')
    item = Item.objects.get(pk=pk)

    new_position = int(request.POST.get('new_position'))
    old_position = item.order

    new_board = request.POST.get('new_board')
    old_board = item.boardlist.get().list_type

    # shift order of items in boards
    items_to_shift = BoardList.objects.get(list_type=old_board).items.filter(order__gte=old_position, archived=False).order_by('-order')
    for item_to_shift in items_to_shift:
      item_to_shift.order -= 1
      item_to_shift.save(update_fields=['order'])
    items_to_shift = BoardList.objects.get(list_type=new_board).items.filter(order__gte=new_position, archived=False).order_by('-order')
    for item_to_shift in items_to_shift:
      item_to_shift.order += 1
      item_to_shift.save(update_fields=['order'])

    BoardList.objects.get(list_type=old_board).items.remove(item)
    item.order = new_position
    BoardList.objects.get(list_type=new_board).items.add(item)
    if new_board == 'DONE':
      item.checked = True
    item.updated_by = request.user
    item.save()

    if new_board != old_board:
      Activity.objects.create(item=item, user=request.user, action='MOVED', source_board=old_board, destination_board=new_board)
    activities = Activity.objects.all().order_by('-timestamp')[:10]
    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.filter(archived=False).order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists, 'activities': activities})


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

    new_position = BoardList.objects.get(list_type=new_board).items.filter(archived=False).count()+1
    old_position = item.order

    # shift order of items in boards
    items_to_shift = BoardList.objects.get(list_type=old_board).items.filter(order__gte=old_position, archived=False).order_by('-order')
    for item_to_shift in items_to_shift:
      item_to_shift.order -= 1
      item_to_shift.save(update_fields=['order'])

    # remove item from boardlist
    BoardList.objects.get(list_type=old_board).items.remove(item)
    item.order = new_position
    BoardList.objects.get(list_type=new_board).items.add(item)
    if new_board == 'DONE':
      item.checked = True
    item.updated_by = request.user
    item.save()

    Activity.objects.create(item=item, user=request.user, action='MOVED', source_board=old_board, destination_board=new_board)
    activities = Activity.objects.all().order_by('-timestamp')[:10]
    board_lists = BoardList.objects.prefetch_related('items').all()
    for board_list in board_lists:
      board_list.ordered_items = board_list.items.filter(archived=False).order_by('-order')
    return render(request, 'partials/board.html', {'board_lists': board_lists, 'activities': activities})