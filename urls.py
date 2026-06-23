from django.urls import path
from .views import (
    event_list,
    event_detail,
    register_event,
    user_registrations,
    cancel_registration
)

urlpatterns = [
    path('events/', event_list),
    path('events/<int:event_id>/', event_detail),

    path('register/', register_event),

    path(
        'my-registrations/<int:user_id>/',
        user_registrations
    ),

    path(
        'cancel-registration/<int:registration_id>/',
        cancel_registration
    ),
]