from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404

from .models import Poll, Choice
from  .serializers import PollSerializer, ChoiceSerializer, \
    VoteSerializer

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
    

class CreateVote(generics.CreateAPIView):

    serializer_class = VoteSerializer
