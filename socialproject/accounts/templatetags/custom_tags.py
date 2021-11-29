'''
Create custom logic to get notifications without creating another view.
We can get users their context and can filter the notifications by user and
if it has not been seen. These notifications are then returned in the context
and can be accessed them from any
'''

from django import template
from accounts.models import Notification

register = template.Library()

@register.inclusion_tag('accounts/show_notifications.html', takes_context=True)
def show_notifications(context):
    '''Shows notifications to users and excludes seen notifcations and orders
    by date. Notifications are returned via context to show_notifications.html'''
    request_user = context['request'].user
    notifications = Notification.objects.filter(to_user=request_user).exclude(
    user_has_seen=True).order_by('-date')
    return {'notifications': notifications}
