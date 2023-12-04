from django.contrib import admin
from .models import Item, BoardList, Activity

# show item attributes in admin panel
class ItemAdmin(admin.ModelAdmin):
  readonly_fields = ('date_added', 'last_updated')
  list_display = ('__str__', 'boardlist', 'author', 'last_updated', 'updated_by', 'order', 'archived')
  list_filter = ('checked', 'date_added', 'author', 'last_updated', 'updated_by', 'order', 'archived')
  search_fields = ('__str__', 'date_added', 'author', 'last_updated', 'updated_by', 'order', 'archived')
  ordering = ['order']

class ActivityAdmin(admin.ModelAdmin):
  readonly_fields = ('timestamp',)
  list_display = ('item', 'action', 'user', 'source_board', 'destination_board', 'timestamp')
  list_filter = ('action', 'user', 'timestamp')
  search_fields = ('item', 'action', 'user', 'timestamp')
  ordering = ['timestamp']

# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(BoardList)
admin.site.register(Activity, ActivityAdmin)