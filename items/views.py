from django.shortcuts import render

# will need a view to capture sortable events and update boardlist models with new item order, and add and remove items
# will need a view to capture checkbox events to move items from boardlist to boardlist
# will need a simpler view for deletion events
# will need a view to capture new item creation events
# will need a view to capture item update events

# all of the above views will create one of four types of activity records
# all views will return HTML snippets to update the DOM with HTMX

# worst case scenario, HTMX can just return the entire DIV for the boardlist, and we can replace the entire DIV in the DOM
# this would be simplest considering we're using sortable.js