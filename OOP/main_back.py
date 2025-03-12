from fasthtml.common import *
from hmac import compare_digest
from random import randint, choice
from datetime import datetime, timedelta

# ================================
#   LUGGAGE MANAGEMENT CLASSES
# ================================
class Luggage:
    def __init__(self, kilogram):
        self.kilogram = kilogram
        self.price = 15
        
    def calculate_price(self):
        # Check if kilogram is a Luggage object (recursive case)
        if isinstance(self.kilogram, Luggage):
            return self.kilogram.calculate_price()
            
        # Normal case - kilogram is a number
        if self.kilogram >= 30:
            self.price += (self.kilogram - 20) * 2.25
        elif self.kilogram >= 20:
            self.price += (self.kilogram - 15) * 1.75
        return self.price

class LuggagePricingSystem:
    def __init__(self):
        pass
    
    def calculate_luggage_price(self, luggage):
        return luggage.calculate_price()
class Promocode:
    def __init__(self, code, points, discount_percent, expiration_date, description):
        self.__code = code
        self.__points = points
        self.__discount_percent = discount_percent
        self.__expiration_date = expiration_date  # วันหมดอายุ
        self.__description = description  # คำอธิบาย
        
    @property
    def code(self):
        return self.__code
    @property
    def points(self):
        return self.__points
    @property
    def discount_percent(self):
        return self.__discount_percent
    @property
    def expiration_date(self):
        return self.__expiration_date 
    @property
    def description(self):
        return self.__description
    
    def can_redeem(self, user_points):
        # Check if the promocode has expired
        today = datetime.now().strftime("%Y-%m-%d")
        if today > self.expiration_date:
            return False
        # Check if user has enough points
        return user_points >= self.points

    def is_expired(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return today > self.expiration_date
    
    
        

# ================================
#   ACCOUNT MANAGEMENT CLASSES
# ================================
class UserDetail:
    def __init__(self, firstname, lastname, points=0):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__points = points  # Private variable for points
        self.__birthday = []
        self.__gender = []
        self.__identification = []
        self.__nationality = []
        self.__phone_number = []
        self.__address = []
        self.__promocode_list = []
        self.__booking_list = []
        self.__redeemed_codes = []      

    @property
    def firstname(self): return self.__firstname
    
    @property
    def lastname(self): return self.__lastname
    
    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, value):
        if value < 0:
            raise ValueError("Points cannot be negative")
        self.__points = value  # Update private points variable directly

    @property
    def birthday(self): return self.__birthday
    
    @property
    def gender(self): return self.__gender
    
    @property
    def identification(self): return self.__identification
    
    @property
    def nationality(self): return self.__nationality
    
    @property
    def phone_number(self): return self.__phone_number
    
    @property
    def address(self): return self.__address
    
    @property
    def promocode_list(self): return self.__promocode_list
    
    @property
    def booking_list(self): return self.__booking_list
    
    @property
    def redeemed_codes(self): return self.__redeemed_codes
    
    @lastname.setter
    def lastname(self, new_lastname): self.__lastname = new_lastname
    
    @phone_number.setter
    def phone_number(self, new_number): self.__phone_number = new_number
    
    @address.setter
    def address(self, address): self.__address = address
    
    @firstname.setter
    def firstname(self, firstname): self.__firstname = firstname
    
    @birthday.setter
    def birthday(self, birthday): self.__birthday = birthday
    
    @gender.setter
    def gender(self, gender): self.__gender = gender
    
    @nationality.setter
    def nationality(self, nation): self.__nationality = nation
            
    def edit_profile(self, firstname=None, lastname=None, phone_number=None, address=None, birthday=None, gender=None, nationality=None):
        if firstname: self.firstname = firstname
        if lastname: self.lastname = lastname
        if phone_number: self.phone_number = phone_number
        if address: self.address = address
        if birthday: self.birthday = birthday
        if gender: self.gender = gender
        if nationality: self.nationality = nationality

    def redeem_promocode(self, promo):
        """Redeem a promo code"""
        # Check if already redeemed
        if promo in self.redeemed_codes:
            print(f"Promo code {promo.code} already redeemed!")
            return True
            
        # Check if user can redeem (has enough points)
        if promo.points == 0 or promo.can_redeem(self.points):
            if promo.points > 0:
                self.points -= promo.points  # Deduct points via setter
            
            self.promocode_list.append(promo.code)
            self.redeemed_codes.append(promo)
            print(f"Promo code {promo.code} redeemed successfully!")
            print(f"Updated redeemed codes: {[code.code for code in self.redeemed_codes]}")
            return True
        
        print(f"Not enough points to redeem promo code {promo.code}")
        return False

    def get_owned_codes(self, promotion_codes):
        from fasthtml.common import Li, Ul
        
        owned_code_list = [
            Li(f"{code} - {next((p.discount_percent for p in promotion_codes if p.code == code), 0)}% off")  
            for code in self.promocode_list
        ]
        return Ul(*owned_code_list, id="owned-codes")
            
    def search_promo(self, code):
        print(f"Searching for promo code: {code}")
        
        for promocode in self.redeemed_codes:
            print(f"User's redeemed code: {promocode.code}")
            if code == promocode.code:
                print(f"Promo code {promocode.code} found in redeemed codes with {promocode.discount_percent}% off")
                return promocode.discount_percent
        
        print("Promo code not found")
        return 0

    def use_promo(self, code):
        for promocode in self.redeemed_codes:
            print(f"User's redeemed code: {promocode.code}")
            if code == promocode.code:
                self.redeemed_codes.remove(promocode)


class Seat:
    def __init__(self, seat_id, seat_type, price):
        self.seat_id = seat_id
        self.seat_type = seat_type
        self.seat_status = True  # Available by default
        self.price = price
      
    def update_seat_status(self, available=False):
        self.seat_status = available
        print(f"Seat {self.seat_id} status updated to: {'Available' if available else 'Unavailable'}")
      
    def is_available(self):
        return self.seat_status

class Airport:
    def __init__(self, name, code):
        self.name = name
        self.code = code
    
    def __str__(self):
        return f"{self.name} ({self.code})"
     
class Account:
    def __init__(self, email, password, userdetail):
        self.__email = email
        self.__password = password
        self.__userdetail = userdetail
        self.__booking_list = []
    
    @property
    def email(self): return self.__email
    @property
    def password(self): return self.__password
    @property
    def userdetail(self): return self.__userdetail
    @property
    def booking_list(self): return self.__booking_list

    @password.setter
    def password(self, new_password): self.__password = new_password
      
    def check_password(self, password):
        return compare_digest(self.password, password)
   
    def change_password(self, old_password, new_password, confirm_new_password):
        if old_password != self.password:
            return "Old password is incorrect"
        if new_password != confirm_new_password:
            return "New passwords do not match"
        if len(new_password) < 6:
            return "New password must be at least 6 characters long"
        if new_password == old_password:
            return "New password cannot be the same as the old password"

        self.password = new_password
        return "Password changed successfully"

class Plane:
    def __init__(self, plane_id, aircraft):
        self.plane_id = plane_id
        self.aircraft = aircraft
        self.seats = self._generate_seats()
    
    def _generate_seats(self):
        seats = []
        if self.aircraft == "Boeing 777":
            # First Class (rows 1-2, 2 seats per row)
            for row in range(1, 3):
                for col in ["A", "B"]:
                    seats.append(Seat(f"{row}{col}", "First Class", 2500))
            # Business Class (rows 3-7, 4 seats per row)
            for row in range(3, 8):
                for col in ["A", "B", "C", "D"]:
                    seats.append(Seat(f"{row}{col}", "Business", 1200))
            # Economy Class (rows 8-27, 6 seats per row)
            for row in range(8, 28):
                for col in ["A", "B", "C", "D", "E", "F"]:
                    seats.append(Seat(f"{row}{col}", "Economy", 500))
        
        elif self.aircraft == "Boeing 737":
            # Business Class (rows 1-3, 4 seats per row)
            for row in range(1, 4):
                for col in ["A", "B", "C", "D"]:
                    seats.append(Seat(f"{row}{col}", "Business", 1000))
            # Economy Class (rows 4-18, 6 seats per row)
            for row in range(4, 19):
                for col in ["A", "B", "C", "D", "E", "F"]:
                    seats.append(Seat(f"{row}{col}", "Economy", 400))
        
        elif self.aircraft == "Boeing 787":
            # Business Class (rows 1-3, 4 seats per row)
            for row in range(1, 4):
                for col in ["A", "B", "C", "D"]:
                    seats.append(Seat(f"{row}{col}", "Business", 1000))
            # Economy Class (rows 4-18, 6 seats per row)
            for row in range(4, 19):
                for col in ["A", "B", "C", "D", "E", "F"]:
                    seats.append(Seat(f"{row}{col}", "Economy", 400))

        elif self.aircraft == "Airbus A320":
            # First Class (rows 1-2, 2 seats per row)
            for row in range(1, 3):
                for col in ["A", "B"]:
                    seats.append(Seat(f"{row}{col}", "First Class", 2500))
            # Business Class (rows 3-7, 4 seats per row)
            for row in range(3, 8):
                for col in ["A", "B", "C", "D"]:
                    seats.append(Seat(f"{row}{col}", "Business", 1200))
            # Economy Class (rows 8-27, 6 seats per row)
            for row in range(8, 28):
                for col in ["A", "B", "C", "D", "E", "F"]:
                    seats.append(Seat(f"{row}{col}", "Economy", 500))

        elif self.aircraft == "Airbus A380":
            # First Class (rows 1-4, 4 seats per row)
            for row in range(1, 5):
                for col in ["A", "B", "C", "D"]:
                    seats.append(Seat(f"{row}{col}", "First Class", 3000))
            # Business Class (rows 5-15, 6 seats per row)
            for row in range(5, 16):
                for col in ["A", "B", "C", "D", "E", "F"]:
                    seats.append(Seat(f"{row}{col}", "Business", 1500))
            # Premium Economy (rows 16-25, 8 seats per row)
            for row in range(16, 26):
                for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                    seats.append(Seat(f"{row}{col}", "Premium Economy", 800))
            # Economy Class (rows 26-50, 10 seats per row)
            for row in range(26, 51):
                for col in ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K"]:
                    seats.append(Seat(f"{row}{col}", "Economy", 600))

        return seats
    
    def get_available_seats(self, seat_type=None):
        if seat_type:
            return [seat for seat in self.seats if seat.seat_type == seat_type and seat.is_available()]
        return [seat for seat in self.seats if seat.is_available()]

class FlightRoute:
    def __init__(self, flight_id, origin_airport, destination_airport, departure_time, arrive_time, plane,
                 available_departure_dates=None, available_arrival_dates=None,
                 return_departure_dates=None, return_arrival_dates=None):
        self.flight_id = flight_id
        
        # Handle both string codes and Airport objects
        if isinstance(origin_airport, Airport):
            self.origin = origin_airport.code
            self.origin_airport = origin_airport
        else:
            self.origin = origin_airport
            self.origin_airport = None
            
        if isinstance(destination_airport, Airport):
            self.destination = destination_airport.code
            self.destination_airport = destination_airport
        else:
            self.destination = destination_airport
            self.destination_airport = None
            
        self.departure_time = departure_time
        self.arrive_time = arrive_time
        self.plane = plane
        
        # Additional fields from the second implementation
        self.available_departure_dates = available_departure_dates or [departure_time]
        self.available_arrival_dates = available_arrival_dates or [arrive_time]
        self.return_departure_dates = return_departure_dates or []
        self.return_arrival_dates = return_arrival_dates or []
        
        # Separate outbound and return seats
        self.outbound_seats = []
        self.return_seats = []
        
        # Create deep copies of the plane's seats for this specific flight
        if plane:
            for seat in plane.seats:
                # Create a new seat object with the same properties
                new_seat = Seat(seat.seat_id, seat.seat_type, seat.price)
                self.outbound_seats.append(new_seat)
    
    def display_flight_info(self):
        print(f"Flight {self.flight_id}: {self.origin} -> {self.destination}")
        print(f"Departure: {self.departure_time}")
        print(f"Arrival: {self.arrive_time}")
        if hasattr(self, 'plane') and self.plane:
            print(f"Aircraft: {self.plane.aircraft} (ID: {self.plane.plane_id})")
        
        if self.is_round_trip():
            print("Round trip available with return flights on:")
            for i, date in enumerate(self.return_departure_dates):
                print(f"  - Departure: {date}, Arrival: {self.return_arrival_dates[i]}")
    
    def is_round_trip(self):
        return len(self.return_departure_dates) > 0
    
    def get_routes(self):
        routes = [
            f"{self.origin} → {self.destination} ({self.departure_time} → {self.arrive_time})"
        ]
        if self.is_round_trip():  
            routes.append(f"{self.destination} → {self.origin} ({self.return_departure_dates[0]} → {self.return_arrival_dates[0]})")
        return routes
    
    def add_outbound_seats(self, seats):
        self.outbound_seats.extend(seats)
        
    def add_return_seats(self, seats):
        self.return_seats.extend(seats)

class Passenger:
    _id_counter = 0
    
    def __init__(self, firstname, lastname, phone=None, dob=None):
        Passenger._id_counter += 1
        self.id = f"p{Passenger._id_counter}"
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.dob = dob

class Payment:
    def __init__(self, price):
        self.price = price
        self.method = None
        self.status = "Pending"

    def process_payment(self, method, card_number, cvv, exp):
        if method == "CreditCard":
            self.method = CreditCard(card_number, cvv, exp)
        elif method == "DebitCard":
            self.method = DebitCard(card_number, cvv, exp)
        self.status = "Completed"
        return True
        
    def refund(self, amount=None):
        if not self.method:
            return False
            
        refund_amount = amount or self.price
        print(f"Refunding {refund_amount} to {self.method.method_id} ending with {self.method.card_number[-4:]}")
        self.status = "Refunded"
        return True

    def discount_payment(self, discount_percent):
        if discount_percent is None:
            discount_percent = 0
        
        discount = (100 - discount_percent) / 100
        self.price *= discount

class PaymentMethod:
    def __init__(self, method_id):
        self.method_id = method_id
       
class ATMCard(PaymentMethod):
    def __init__(self, method_id, card_number, card_CVV, card_EXP):
        super().__init__(method_id)
        self.card_number = card_number
        self.card_CVV = card_CVV
        self.card_EXP = card_EXP

class CreditCard(ATMCard):
    def __init__(self, card_number, card_CVV, card_EXP, method_id="CreditCard"):
        super().__init__(method_id, card_number, card_CVV, card_EXP)

class DebitCard(ATMCard):
    def __init__(self, card_number, card_CVV, card_EXP, method_id="DebitCard"):
        super().__init__(method_id, card_number, card_CVV, card_EXP)

class Booking:
    bookings = []  # Class variable to store all bookings
    
    def __init__(self, flight, booking_reference=None):
        # Generate booking reference if not provided
        self.booking_reference = booking_reference or f"BK{randint(1000, 9999)}"
        self.flight = flight
        self.outbound_seat = None
        self.return_seat = None
        self.passengers = []
        self.passenger_seats = {}
        self.luggage_weight = 0
        self.luggage = None
        self.payment = None
        self.status = 'Unpaid'
        
        # Auto-set the flight dates from the flight object
        self.flight_date = flight.departure_time
        self.arrival_time = flight.arrive_time
        
        # For round trips, initialize return flight information
        self.return_flight_date = None
        self.return_arrival_time = None
        
        # Auto-set return flight dates if this is a round trip
        if flight.is_round_trip() and flight.return_departure_dates and flight.return_arrival_dates:
            self.return_flight_date = flight.return_departure_dates[0]
            self.return_arrival_time = flight.return_arrival_dates[0]
        
        # Add to class bookings list
        Booking.bookings.append(self)
    
    def add_luggage(self, kilogram):
        # Check if kilogram is a Luggage object
        if isinstance(kilogram, Luggage):
            self.luggage = kilogram
            self.luggage_weight = kilogram.kilogram  # Extract the weight from the Luggage object
        else:
            # Normal case - kilogram is a number
            self.luggage_weight = kilogram
            self.luggage = Luggage(kilogram)
        
        print(f"Added luggage: {self.luggage_weight} kg")
        return self.luggage_weight
    
    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        print(f"Added passenger: {passenger.firstname} {passenger.lastname}")
        return True
        
    def add_seat(self, seat_id):
        # First check if the seat is already booked on this specific flight
        for booking in Booking.bookings:
            if (booking != self and 
                booking.flight.flight_id == self.flight.flight_id and 
                booking.outbound_seat and 
                booking.outbound_seat.seat_id == seat_id and
                booking.status != "Cancelled"):
                print(f"Seat {seat_id} is already booked on this flight")
                return False
                
        # If not already booked, proceed with booking
        for seat in self.flight.outbound_seats:
            if seat.seat_id == seat_id and seat.is_available():
                self.outbound_seat = seat
                seat.update_seat_status(False)  # Mark as unavailable
                print(f"Added outbound seat: {seat_id}")
                return True
        return False
    
    def add_return_seat(self, seat_id):
        if not self.flight.is_round_trip():
            print("This booking is not for a round trip")
            return False
        
        # First check if the seat is already booked on this specific flight
        for booking in Booking.bookings:
            if (booking != self and 
                booking.flight.flight_id == self.flight.flight_id and 
                booking.return_seat and 
                booking.return_seat.seat_id == seat_id and
                booking.status != "Cancelled"):
                print(f"Return seat {seat_id} is already booked on this flight")
                return False
                
        # If not already booked, proceed with booking
        for seat in self.flight.return_seats:
            if seat.seat_id == seat_id and seat.is_available():
                self.return_seat = seat
                seat.update_seat_status(False)  # Mark as unavailable
                print(f"Added return seat: {seat_id}")
                return True
        return False
    
    def create_payment(self, price):
        self.payment = Payment(price)
        print(f"Created payment: {price}")
        return self.payment

    def update_booking_status(self, status="Paid"):
        self.status = status
        if status == "Cancelled":
            # Release seats when cancelled
            if self.outbound_seat:
                self.outbound_seat.update_seat_status(True)
            if self.return_seat:
                self.return_seat.update_seat_status(True)
        print(f"Updated booking status to: {status}")
        return True
    
    def set_flight_dates(self, flight_date, arrival_time=None):
        self.flight_date = flight_date
        self.arrival_time = arrival_time or self.flight.arrive_time
        return True
        
    def set_return_flight_dates(self, return_flight_date, return_arrival_time=None):
        if not self.flight.is_round_trip():
            print("This booking is not for a round trip")
            return False
            
        self.return_flight_date = return_flight_date
        self.return_arrival_time = return_arrival_time or self.flight.return_arrival_dates[0]
        return True
    
    def edit(self, flight_date=None, arrival_time=None, outbound_seat=None, 
             return_flight_date=None, return_arrival_time=None, return_seat=None):
        # Update outbound details
        if flight_date:
            self.flight_date = flight_date
        if arrival_time:
            self.arrival_time = arrival_time
        if outbound_seat:
            # Free up previous seat
            if self.outbound_seat:
                self.outbound_seat.update_seat_status(True)
            # Set new seat
            if isinstance(outbound_seat, Seat):
                self.outbound_seat = outbound_seat
                outbound_seat.update_seat_status(False)
            else:
                # Handle case where seat_id is passed instead of Seat object
                self.add_seat(outbound_seat)
        
        # Update return details for round trips
        if self.flight.is_round_trip():
            if return_flight_date:
                self.return_flight_date = return_flight_date
            if return_arrival_time:
                self.return_arrival_time = return_arrival_time
            if return_seat:
                # Free up previous seat
                if self.return_seat:
                    self.return_seat.update_seat_status(True)
                # Set new seat
                if isinstance(return_seat, Seat):
                    self.return_seat = return_seat
                    return_seat.update_seat_status(False)
                else:
                    # Handle case where seat_id is passed instead of Seat object
                    self.add_return_seat(return_seat)
        
        return True
    
    def cancel(self):
        if self.status == "Paid":
            # Store the refund amount before changing status
            self.refund_amount = self.calculate_refund()
            result = self.update_booking_status("Cancelled")
            if result:
                self.process_refund()
            return result
        elif self.status == "Unpaid":
            # No need to refund if not paid yet
            return self.update_booking_status("Cancelled")
        else:
            # Already cancelled or another status
            return False
    def calculate_refund(self):
        # Calculate the refund amount based on the booking details
        # This can include seat prices, luggage fees, etc.
        total_price = 0
        # Add seat prices
        if self.outbound_seat:
            total_price += self.outbound_seat.price
        if self.return_seat:
            total_price += self.return_seat.price
            
        # Add luggage fees if applicable
        if hasattr(self, 'luggage_weight') and self.luggage_weight > 0:
            luggage = Luggage(self.luggage_weight)
            total_price += luggage.calculate_price()
            
        return total_price
    
    def process_refund(self):
        if not hasattr(self, 'refund_amount'):
            print("No refund amount calculated")
            return False
            
        if not self.payment:
            print("No payment information available for refund")
            return False
            
        # Process the refund through the payment method
        print(f"Processing refund of {self.refund_amount} THB to {self.payment.method.method_id}")
        print(f"Refund processed successfully to card ending with {self.payment.method.card_number[-4:]}")
        return True
    
    @classmethod
    def get_booking_by_ref(cls, ref):
        for booking in cls.bookings:
            if booking.booking_reference == ref:
                return booking
        return None

# Controller to manage users, flights, and luggage
class Controller:
    def __init__(self):
        self.planes = []
        self.__accounts = []
        self.__logged_in_user = None
        self.__flights = []
        self.bookings = []
        self._next_flight_id = 1
        self.luggage_system = LuggagePricingSystem()
        self.airports = []
   
    @property
    def accounts(self): return self.__accounts
    @property
    def logged_in_user(self): return self.__logged_in_user
    @property
    def flights(self): return self.__flights
    
    @logged_in_user.setter
    def logged_in_user(self, user): self.__logged_in_user = user
   
    def register(self, email, password, firstname, lastname):
        if any(acc.email == email for acc in self.accounts):
            return "Email already registered!"
        
        user_detail = UserDetail(firstname, lastname)
        new_account = Account(email, password, user_detail)
        self.accounts.append(new_account)
        return "Registration successful!"

    def login(self, email, password):
        for acc in self.accounts:
            if acc.email == email and acc.check_password(password):
                self.logged_in_user = acc
                return "Login successful!"
        return "Invalid email or password!"

    def get_logged_in_user(self):
        return self.logged_in_user
   
    def get_flight_by_id(self, flight_id):
        for flight in self.flights:
            if flight.flight_id == flight_id:
                return flight
        print(f"Flight {flight_id} not found")
        return None
   
    def create_booking(self, flight_id, luggage_kg=0):
        flight = self.get_flight_by_id(flight_id)
        if not flight:
            print(f"Error: Flight {flight_id} not found")
            return None
        
        booking_reference = f"BK{randint(1000, 9999)}"
        new_booking = Booking(flight, booking_reference)
        
        if luggage_kg > 0:
            new_booking.add_luggage(luggage_kg)
            
        self.bookings.append(new_booking)
        print(f"Booking Created: {booking_reference} for Flight {flight_id}")
        return new_booking

    def add_booking_history(self, booking):
        print("Adding booking to user history")
        if self.logged_in_user:
            self.logged_in_user.booking_list.append(booking)
            return True
        return False

    def logout(self):
        self.logged_in_user = None
        return "Logged out successfully"
      
    def search_flights(self, origin, destination, date):
        results = [flight for flight in self.flights 
                  if flight.origin == origin and 
                     flight.destination == destination and 
                     any(departure_date.startswith(date) for departure_date in flight.available_departure_dates)]
        return results

    def find_booking_by_reference(self, booking_ref):
        return next((booking for booking in self.bookings if booking.booking_reference == booking_ref), None)

    def process_passenger_data(self, booking, form_data):
        if not hasattr(booking, 'passengers') or not booking.passengers:
            person_count = int(form_data.get("person_count", "1"))
            passenger_data = []
            
            for i in range(person_count):
                passenger = Passenger(
                    firstname=form_data.get(f"first_name_{i}", ""),
                    lastname=form_data.get(f"last_name_{i}", ""),
                    phone=form_data.get(f"phone_{i}", ""),
                    dob=form_data.get(f"dob_{i}", "")
                )           
                passenger_data.append(passenger)
            
            booking.passengers = passenger_data

    def assign_seats_to_passengers(self, booking, form_data):
        seat_ids = form_data.getlist("seat_ids") if hasattr(form_data, "getlist") else form_data.get("seat_ids", [])
        if not isinstance(seat_ids, list):
            seat_ids = [seat_ids]
            
        booking.passenger_seats = {}
        for i, passenger in enumerate(booking.passengers):
            if i < len(seat_ids):
                booking.passenger_seats[passenger.id] = seat_ids[i]
                booking.add_seat(seat_ids[i])

    def calculate_passenger_seat_details(self, booking, flight):
        passenger_items = []
        total_seat_price = 0
        
        for passenger in booking.passengers:
            seat_id = booking.passenger_seats.get(passenger.id, 'Not assigned')
            seat_class = "Economy"
            seat_price = 0

            if seat_id != 'Not assigned':
                seat = self._find_seat_by_id(flight, seat_id)
                
                if seat:
                    seat_class = seat.seat_type
                    seat_price = seat.price
            
            total_seat_price += seat_price
            
            passenger_items.append(
                Div(
                    P(f"Name: {passenger.firstname} {passenger.lastname}"),
                    P(f"Contact: {passenger.phone}"),
                    P(f"Seat: {seat_id} ({seat_class}) - ${seat_price}"),
                    cls="passenger-item"
                )
            )
    
        return passenger_items, total_seat_price

    def _find_seat_by_id(self, flight, seat_id):
        # ค้นหาในที่นั่งขาออก
        seat = next((s for s in flight.outbound_seats if s.seat_id == seat_id), None)
        
        # ถ้าไม่พบ ให้ค้นหาในที่นั่งของเครื่องบิน
        if not seat:
            seat = next((s for s in flight.plane.seats if s.seat_id == seat_id), None)
        
        return seat

    def add_flight(self, flight):
        flight.id = self._next_flight_id
        self._next_flight_id += 1
        self.flights.append(flight)
        return flight

    def get_flight(self, flight_id):
        return next((flight for flight in self.flights if flight.id == flight_id), None)

    def update_flight(self, updated_flight):
        for i, flight in enumerate(self.flights):
            if flight.id == updated_flight.id:
                self.flights[i] = updated_flight
                return updated_flight
        return None

    def delete_flight(self, flight_id):
        self.flights = [flight for flight in self.flights if flight.id != flight_id]
   
    def filter_flights(self, query=None, available_only=False):
        filtered = self.flights
        if query:
            query = query.lower()
            filtered = [flight for flight in filtered 
                    if query in flight.origin.lower() or 
                        query in flight.destination.lower()]
        if available_only:
            filtered = [flight for flight in filtered 
                    if any(flight.outbound_seats) or any(flight.return_seats)]
        
        return filtered
   
    def add_plane(self, plane):
        self.planes.append(plane)
    
    def add_airport(self, airport):
        self.airports.append(airport)
      
    def generate_flight_id(self):
        return f"FL{randint(100, 999)}"

    def generate_random_flight_list(self, airports, num_flights=10):
        for _ in range(num_flights):
            origin = choice(airports)
            destination = choice([ap for ap in airports if ap != origin])
            
            departure_date = datetime(2025, 3, 1) + timedelta(days=randint(1, 30))
            departure_time = departure_date.strftime("%Y-%m-%d %H:%M")
            
            flight_duration = randint(1, 5)
            arrive_time = (departure_date + timedelta(hours=flight_duration)).strftime("%Y-%m-%d %H:%M")
            
            plane = choice(self.planes)
            
            # Create alternative available dates
            alt_dates = []
            alt_arrivals = []
            for i in range(1, 4):  # Add 3 alternative dates
                alt_date = departure_date + timedelta(days=i*7)  # Weekly options
                alt_dates.append(alt_date.strftime("%Y-%m-%d %H:%M"))
                alt_arrival = alt_date + timedelta(hours=flight_duration)
                alt_arrivals.append(alt_arrival.strftime("%Y-%m-%d %H:%M"))
            
            # Add return dates for some flights (50% chance)
            return_dates = []
            return_arrivals = []
            if randint(0, 1) == 1:
                for i in range(1, 3):  # Add 2 return date options
                    return_date = departure_date + timedelta(days=7+i*3)  # Return dates
                    return_dates.append(return_date.strftime("%Y-%m-%d %H:%M"))
                    return_arrival = return_date + timedelta(hours=flight_duration)
                    return_arrivals.append(return_arrival.strftime("%Y-%m-%d %H:%M"))
            
            flight = FlightRoute(
                self.generate_flight_id(), 
                origin, 
                destination, 
                departure_time, 
                arrive_time, 
                plane,
                [departure_time] + alt_dates,
                [arrive_time] + alt_arrivals,
                return_dates,
                return_arrivals
            )
            
            # Add placeholder return seats if it's a round trip
            if flight.is_round_trip():
                # Create independent seat objects for the return flight
                return_seats = []
                for seat in plane.seats:
                    return_seat = Seat(
                        f"R-{seat.seat_id}", 
                        seat.seat_type, 
                        seat.price
                    )
                    return_seats.append(return_seat)
                flight.add_return_seats(return_seats)
            
            self.flights.append(flight)
    
    def display_all_flights(self):
        for flight in self.flights:
            flight.display_flight_info()
            print()
            
    def calculate_luggage_price(self, luggage_kg):
        luggage = Luggage(luggage_kg)
        return self.luggage_system.calculate_luggage_price(luggage)
        
    def get_booking(self, booking_reference):
        return Booking.get_booking_by_ref(booking_reference)

# Create a function to set up the initial system

promotion_codes = [
    
    Promocode("SUMMER2025",100,10,"2025-09-01","Summer Special Discount"),
    Promocode("WELCOME250",250,25,"2025-12-31","New User Welcome Discount")

]

def initialize_system():
    controller = Controller()
    
    # Setup admin account
    controller.logged_in_user = Account("admin", "admin", UserDetail("John", "Doe", points=500))
    
    # Setup airports
    jfk = Airport("John F. Kennedy International Airport", "JFK")
    lax = Airport("Los Angeles International Airport", "LAX")
    sfo = Airport("San Francisco International Airport", "SFO")
    bkk = Airport("Suvarnabhumi Airport", "BKK")
    cnx = Airport("Chiang Mai International Airport", "CNX")
    lhr = Airport("London Heathrow", "LHR")
    cdg = Airport("Paris Charles de Gaulle", "CDG")
    hnd = Airport("Tokyo Haneda", "HND")
    sin = Airport("Singapore Changi", "SIN")
    cgk = Airport("Jakarta Soekarno-Hatta", "CGK")
    
    airports = [jfk, lax, sfo, bkk, cnx, lhr, cdg, hnd, sin, cgk]
    for airport in airports:
        controller.add_airport(airport)
    
    # Create & Add Planes
    boeing_777 = Plane("B777-001", "Boeing 777")
    boeing_737 = Plane("B737-002", "Boeing 737")
    boeing_787 = Plane("B787-003", "Boeing 787")
    airbus_a320 = Plane("A320-001", "Airbus A320")
    airbus_a380 = Plane("A380-001", "Airbus A380")
    

    planes = [boeing_777, boeing_737, boeing_787, airbus_a320, airbus_a380]
    for plane in planes:
        controller.add_plane(plane)
    
    # Generate Flights
    controller.generate_random_flight_list(airports, num_flights=50)
    return controller
controller = initialize_system()

# Define the flight route generation function
def generate_comprehensive_flight_routes(controller):
    """
    Generates FlightRoute objects between all airports in the system
    using the same pattern as the bkk_jfk_flight example.
    """
    # Get all airports and planes from the controller
    airports = controller.airports
    planes = controller.planes
    
    # Counter for creating unique flight IDs
    flight_counter = 1  # Starting from FL200
    
    # List to collect all created flights
    created_flights = []
    
    # Create flight routes between each pair of airports
    for origin in airports:
        for destination in airports:
            # Skip same-airport routes
            if origin == destination:
                continue
                
            # Select a plane (rotating through available planes)
            plane = planes[flight_counter % len(planes)]
            
            # Create flight ID
            flight_id = f"FL{flight_counter}"
            
            # Base departure and arrival dates
            base_departure = "2025-04-10 14:00"
            base_arrival = "2025-04-11 05:00"
            
            # Create multiple departure options (5 days apart)
            departure_dates = [
                base_departure,
                "2025-04-15 14:00",
                "2025-04-20 14:00",
                "2025-04-25 14:00"
            ]
            
            # Create corresponding arrival options
            arrival_dates = [
                base_arrival,
                "2025-04-16 05:00",
                "2025-04-21 05:00",
                "2025-04-26 05:00"
            ]
            
            # Create return departure options (10 days after outbound)
            return_departure_dates = [
                "2025-04-20 14:00",
                "2025-04-25 14:00",
                "2025-04-30 14:00"
            ]
            
            # Create return arrival options
            return_arrival_dates = [
                "2025-04-21 05:00",
                "2025-04-26 05:00",
                "2025-05-01 05:00"
            ]
            
            # Create the FlightRoute
            new_flight = FlightRoute(
                flight_id,
                origin,
                destination,
                base_departure,
                base_arrival,
                plane,
                departure_dates,
                arrival_dates,
                return_departure_dates,
                return_arrival_dates
            )
            
            # Create independent return seats for the round trip
            if new_flight.is_round_trip():
                return_seats = []
                for seat in plane.seats:
                    # Create a completely new seat object for the return flight
                    return_seat = Seat(
                        f"R-{seat.seat_id}",
                        seat.seat_type,
                        seat.price
                    )
                    return_seats.append(return_seat)
                
                # Add the return seats to the flight
                new_flight.add_return_seats(return_seats)
            
            # Add the flight to our collection
            created_flights.append(new_flight)
            
            # Increment counter for next flight
            flight_counter += 1
    
    # Add all created flights to the controller
    for flight in created_flights:
        controller.flights.append(flight)
    
    print(f"Created {len(created_flights)} flight routes connecting all airports")
    return created_flights

# Now call the function with the controller
new_flights = generate_comprehensive_flight_routes(controller)
controller.display_all_flights()




