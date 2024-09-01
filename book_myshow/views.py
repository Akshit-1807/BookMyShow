from django.shortcuts import render
from rest_framework import viewsets

from book_myshow.serializers import CreatBookingRequestDto


# Create your views here.
class BookingViewSet(viewsets.ViewSet):
    def create_booking(self, request):
        req = CreatBookingRequestDto(request.data)
        req.is_valid(raise_exception=True)
        try:


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

