from django.http.response import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import AnonymousUser
from .models import User, Series, Event
from .serializers import UserSerializer, SeriesSerializer, EventSerializer
from rest_framework.permissions import IsAdminUser

# Naming convention: OBJECT(List) + CRUD-options + View

# Users
class UserMixin:
  def get_queryset(self):
    user = self.request.user
    # give all admin permissions to see everything
    if user.is_staff:
      return User.objects.all()
    # give logged-in users the ability to see themselves as a user
    if not isinstance(user, AnonymousUser):
      return User.objects.filter(username=user.username)
    # not admin or logged in, you get nothing
    return None

class UserListCreateView(UserMixin, ListCreateAPIView):
  serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(UserMixin, RetrieveUpdateDestroyAPIView):
  serializer_class = UserSerializer


# Series
class SeriesMixin:
  def get_queryset(self):
    user = self.request.user
    # give all admin permissions to see everything
    if user.is_staff:
      return Series.objects.all()
    # give logged-in users the ability to see what they are an organizer or particpant of
    if not isinstance(user, AnonymousUser):
      series_organizer = Series.objects.filter(organizer__username=user.username)
      series_participant = Series.objects.filter(participants__username=user.username)
      return series_organizer.union(series_participant)
    # not admin or logged in, you get nothing
    return None

class SeriesListCreateView(SeriesMixin, ListCreateAPIView):
  serializer_class = SeriesSerializer

class SeriesRetrieveUpdateDestroyView(SeriesMixin, RetrieveUpdateDestroyAPIView):
  serializer_class = SeriesSerializer


# Events
class EventMixin:
  def get_queryset(self):
    user = self.request.user
    # give all admin permissions to see everything
    if user.is_staff:
      return Event.objects.all()
    # give logged-in users the ability to see what events they in if:
    # 1) are a host
    # or
    # 2) participant of a series the events is in
    if not isinstance(user, AnonymousUser):
      event_host = Event.objects.filter(host__username=user.username)
      event_in_series = Event.objects.filter(series__participants__username=user.username)
      return event_host.union(event_in_series)
    # not admin or logged in, you get nothing
    return None

class EventListCreateView(EventMixin, ListCreateAPIView):
  serializer_class = EventSerializer
  
class EventRetrieveUpdateDestroyView(EventMixin, RetrieveUpdateDestroyAPIView):
  serializer_class = EventSerializer

def GenerateDraftOrderView(request):
  '''
  Overall Steps:
  When viewing a single series with all of the events and participant users added, the series organizer can click a one-time button to generate a "draft order".
  When clicked, the url is sent to the API to call a "function based view".
  The function based view retrieves the user/participants for this series using a database call and filter.
  The function based view retrieves the events for this series using a database call and filter.
  The function calls the drafting helper function (or just living inside of it as a part of this function) with the user/participant and event info.  (Event info could just be number of events... aka length.)
  The function based view calculates the draft order as an array of arrays.
    - The randomizer draft function (contained within the function based view) was created by Yoni.  Conducts only full rounds, randomizes odd rounds of draft, reverses odd rounds as the next even rounds, tries to add fairness with attempts to not repeat identical rounds, may or may not return random numbers for the leftover/remainder rounds.
    - Each inner array represents a "round" in the "draft".  Each element in an inner array represents a "pick" in that "round".
  The function stores the resulting array in the database as an attribute of the "series".
  The function sets the "round" and "pick" attributes of the "series" to 1.
  The "remainder" attribute of the "series" should be set to the value calculated by total_events-participants*rounds.
  The "draft_generation_complete" boolean attribute of the series should be updated to be True.
  The function based view then redirects the page to be a view that shows the overall draft order.
  The view for the overall draft order, then sends the draft order and current draft round and pick numbers to React for rendering.
    - Could possibly instead just send it to the single series review screen.
    - A test case will be done first to just show simple html message showing the function based view is being called.

  django docs about views:  https://docs.djangoproject.com/en/3.1/topics/http/views/
  Helpful terms and hints:
    - object relational mapper (ORM)  --so that we don't have to write SQL
    - Object Manager:  <ourObject>.objects

  # target_series = Series.objects.all().filter(title="Season 2021")

  # request.params.pk = pk ?
  # target_series.round += 1
  
  # target_series.save()

  '''

# Yoni's code for figuring out the draft order; will be put in here once we know the routes are connected and his inputs are available.
# import random
# import copy
# user_IDs = [1,2,3,4,5]
# event_IDs = [6,7,8,9,10]

# def random_draft(user_IDs, event_IDs):

#   full_draft = []
#   max_rounds = (len(event_IDs)//len(user_IDs))
#   while len(full_draft) < max_rounds:
#     current_order = copy.copy(user_IDs)
#     shuffle = random.shuffle(current_order)
#     if current_order not in full_draft:
#       full_draft += [current_order]
#       if len(full_draft) < max_rounds:
#         reverse_order = []
#         for i in range(len(current_order)):
#           reverse_index = len(current_order) - 1 -i
#           reverse_order += [current_order[reverse_index]]
#         full_draft += [reverse_order]
#   return full_draft

# print('one round:',random_draft(user_IDs, event_IDs))
# print('more rounds:',random_draft(user_IDs, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]))
# print('uneven rounds:',random_draft([1,2], [1,2,3,4,5,6,7,8,9,10,11,12,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]))





  # RESPONSE ------
  # sounds like a response of html or redirect will not work because it requires the use of django front end... therefore, just return JSON

  # no longer using redirect
  # this code will hopefully perform the redirect
  # if not work, likely need to combine next two lines or figure out how to identify series id
  # desired_path = 'series/' + series.id + '/'
  # response = redirect(desired_path)
  # return response

  # no longer using html response
  # html = "<html><body>The view to generate a draft order has been reached.</body></html>"
  # return HttpResponse(html)

  #respond with json
  # should we use "JsonResponse"?
  remainder = 2
  message_to_return = "The draft order has been calculated.  There will be " + remainder + "game(s) not included in the draft.  Visit the individual Series page to view the draft order."
  return {"message": message_to_return}


def ClaimEventAsHostView(request):
  # confirm it is the user's turn to claim an event

  # confirm the event is currently available

  # update the Event in the database to assign the current user as the Host of the Event

  # increment the Pick counter by 1
  
  # if the Pick count is higher than the number of Participants, reset it to 1 and increment the Round count by 1

  # if Round count is higher than the number of draft rounds, somehow mark the draft as complete in database

  # create a response message
  figure_out_user = "USERNAME"
  figure_out_event = "EVENT-DESCRIPTION"
  round_holder = 22
  pick_holder = 22
  message_to_return = "Congrats!  " + figure_out_user + " has successfully claimed " + figure_out_event + ".  It is now the next person's turn in the draft.  We are at Pick number " + pick_holder + " of Round " + round_holder + "."
  return {"message": message_to_return}
