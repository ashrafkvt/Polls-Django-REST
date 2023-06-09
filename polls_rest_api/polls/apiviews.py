from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.http import request
from rest_framework.exceptions import PermissionDenied

from .models import Poll, Choice
from  .serializers import PollSerializer, ChoiceSerializer, \
    VoteSerializer, UserSerializer

class PollList(generics.ListCreateAPIView):
    
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveDestroyAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_url_kwarg = 'poll_id'

class ChoiceList(generics.ListCreateAPIView):

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    
    def post(self, request, *args, **kwargs):
        # breakpoint()
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        choice = Choice(choice_text=request.data.get("choice_text"),
                        poll=poll)
        choice.save()
        return Response(self.get_serializer(choice).data)
    

class CreateVote(APIView):

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
