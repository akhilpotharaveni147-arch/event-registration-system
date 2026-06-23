from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


@api_view(['GET'])
def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def register_event(request):

    if request.method == 'GET':
        return Response({
            "message": "Use POST request to register for an event"
        })

    user = User.objects.get(id=request.data['user_id'])
    event = Event.objects.get(id=request.data['event_id'])

    # Prevent duplicate registrations
    existing_registration = Registration.objects.filter(
        user=user,
        event=event
    ).exists()

    if existing_registration:
        return Response({
            "message": "User already registered for this event"
        })

    # Check event capacity
    current_count = Registration.objects.filter(
        event=event,
        status="Registered"
    ).count()

    if current_count >= event.capacity:
        return Response({
            "message": "Event is full"
        })

    registration = Registration.objects.create(
        user=user,
        event=event,
        status="Registered"
    )

    serializer = RegistrationSerializer(registration)

    return Response(serializer.data)


@api_view(['GET'])
def user_registrations(request, user_id):

    registrations = Registration.objects.filter(
        user_id=user_id
    )

    serializer = RegistrationSerializer(
        registrations,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def cancel_registration(request, registration_id):

    registration = Registration.objects.get(
        id=registration_id
    )

    registration.status = "Cancelled"
    registration.save()

    serializer = RegistrationSerializer(
        registration
    )

    return Response(serializer.data)