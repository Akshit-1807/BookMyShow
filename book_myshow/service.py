from book_myshow.models import User,Show,ShowSeat,ShowSeatStatus,Ticket
from django.utils import timezone
class BookShowService():
    def create_booking(self,user_id, show_seat_ids, show_id):
        if len(show_seat_ids>10):
            raise ValueError("show seat id cannot be more than 10")
        try:
            user = User.objects.get(id = user_id)
            if user is None:
                raise User.DoesNotExist
            show = Show.objects.get(id = show_id)
            if show is None:
                raise Show.DoesNotExist

            show_seats = ShowSeat.objects.filter(id__in=show_seat_ids)
            for show_seat in show_seats:
                if show_seat.show_seat_status != ShowSeatStatus.AVAILABLE:
                    raise ValueError('show seat status is not avaiable')

            for show_seat in show_seats:
                show_seat.show_seat_status = ShowSeatStatus.LOCKED
                show_seat.save()
        #Create Booking
            booking = Ticket(
                user = user,
                show = show,
                amount = 100,
                booking_status='PENDING',
                ticket_number=timezone.now(),
            )
            booking.save()

        # Create Payment
            for show_seat in show_seats:
                show_seat.show_seat_status = ShowSeatStatus.RESERVED
                show_seat.save()

            booking.show_seats = show_seats
            booking.save()
            return booking
        except Exception as e:
            print(e)

