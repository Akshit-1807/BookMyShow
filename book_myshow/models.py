from datetime import timezone
from msilib import Feature

from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True

class User(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)

class Region(BaseModel):
    name = models.CharField(max_length=120)

class Theater(BaseModel):
    name = models.CharField(max_length=120)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class Screen(BaseModel):
    name = models.CharField(max_length=120)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature, through='Feature')

class ScreenFeature(BaseModel):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('screen','feature'))

class Movie(BaseModel):
    title = models.CharField(max_length=120)
    release_date = models.DateField
    runtime = models.IntegerField

class Show(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

class ShowFeature(BaseModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

class SeatType(models.TextChoices):
    GOLD = 'GOLD', 'gold'
    SILVER = 'SILVER', 'silver'
    PLATINUM = 'PLATINUM', 'platinum'

class Seat(BaseModel):
    row_number = models.IntegerField()
    col_number = models.IntegerField()
    number = models.CharField(max_length=50)
    seat_type = models.TextField(choices =SeatType.choices)

class ShowSeatStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'available'
    LOCKED = 'LOCKED', 'locked'

class ShowSeat(BaseModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show_seat_status = models.TextField(choices =ShowSeatStatus.choices)

class ShowSeatType(BaseModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat_type = models.ForeignKey(SeatType, on_delete=models.CASCADE)
    price = models.IntegerField()


class Ticket(BaseModel):
    ticket_number = models.IntegerField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    show_seat = models.ForeignKey(ShowSeat, on_delete=models.CASCADE)
    amount = models.IntegerField()
    booking_status = models.CharField(max_length=50)
    # payments = models.ManyToManyField(Payment)

class Payment(BaseModel):
    ref_number = models.IntegerField()
    amount = models.IntegerField()
    mode = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

