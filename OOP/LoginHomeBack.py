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
        if self.kilogram >= 20:
            self.price += (self.kilogram - 15) * 1.75
        elif self.kilogram >= 30:
            self.price += (self.kilogram - 20) * 2.25
        return self.price

class LuggagePricingSystem:
    def __init__(self):
        pass
    
    def calculate_luggage_price(self, luggage):
        return luggage.calculate_price()
    
# ================================
#   ACCOUNT MANAGEMENT CLASSES
# ================================
class UserDetail:
    def __init__(self, firstname, lastname, points=0):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__points = points
        self.__birthday = []
        self.__gender = []
        self.__identification = []
        self.__nationality = []
        self.__phone_number = []
        self.__address = []
        self.__promocode_list = []
        
   
    @property
    def firstname(self): return self.__firstname
    @property
    def lastname(self): return self.__lastname
    @property
    def points(self): return self.__points
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
            
class Seat:
    def __init__(self, seat_id, seat_type, price):
        self.seat_id = seat_id
        self.seat_type = seat_type
        self.seat_status = True
        self.price = price
      
    def update_seat_status(self):
        self.seat_status = False
        print(f"seat_status")
      
    def is_available(self):
        return self.seat_status
      
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
        
        return seats
    
    def get_available_seats(self, seat_type=None):
        if seat_type:
            return [seat for seat in self.seats if seat.seat_type == seat_type and seat.is_available()]
        return [seat for seat in self.seats if seat.is_available()]

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
    
class FlightRoute:
    def __init__(self, flight_id, origin_airport, destination_airport, departure_time, arrive_time, plane):
        self.flight_id = flight_id
        self.origin = origin_airport.code
        self.destination = destination_airport.code
        self.departure_time = departure_time
        self.arrive_time = arrive_time
        self.plane = plane
    
    def display_flight_info(self):
        print(f"Flight {self.flight_id}: {self.origin} -> {self.destination}")
        print(f"Departure: {self.departure_time}")
        print(f"Arrival: {self.arrive_time}")
        print(f"Aircraft: {self.plane.aircraft} (ID: {self.plane.plane_id})")

class Booking:
    def __init__(self, flight, booking_reference):
        self.flight = flight
        self.booking_reference = booking_reference
        self.seat_list = []
        self.passengers = []
        self.passenger_seats = {}
        self.luggage = None
        self.payment = None
        self.status = 'Unpaid'
    
    def add_luggage(self, luggage):
        self.luggage = luggage
        print(f"add_luggage: {luggage}")
    
    def add_seat(self, seat_id):
        if seat_id not in self.seat_list:
            for seat in self.flight.plane.seats:
                if seat.seat_id == seat_id:
                    self.seat_list.append(seat)
                    print(f"Seat add: {seat}")
                    return True
        return False
    
    def create_payment(self, price):
        self.payment = Payment(price)
        print(f"create_payment: {price}")

    def update_booking_status(self):
        self.status = 'Paid'
        for seat in self.seat_list:
            seat.update_seat_status()
        print(f"update_booking_status:")

class Passenger:
    _id_counter = 0
    
    def __init__(self, firstname, lastname, phone, dob):
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

    def process_payment(self, method, card_number, cvv, exp):
        if method == "CreditCard":
            self.method = CreditCard(card_number, cvv, exp)
        elif method == "DebitCard":
            self.method = DebitCard(card_number, cvv, exp)

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
        print(f"add_booking_history")
        self.logged_in_user.booking_list.append(booking)

    def logout(self):
      self.logged_in_user = None
      
    def search_flights(self, origin, destination, date):
      results = [flight for flight in self.flights if flight.origin == origin and flight.destination == destination and flight.departure_time.startswith(date)]
      return results

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
         filtered = [flight for flight in filtered if flight.available]
      
      return filtered
   
    def add_plane(self, plane):
        self.planes.append(plane)
      
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
            
            flight = FlightRoute(self.generate_flight_id(), origin, destination, departure_time, arrive_time, plane)
            self.flights.append(flight)
    
    def display_all_flights(self):
        for flight in self.flights:
            flight.display_flight_info()
            print()
            
    def calculate_luggage_price(self, luggage):
        return self.luggage_system.calculate_luggage_price(luggage)

# Initialize the system
controller = Controller()

controller.logged_in_user = Account("admin", "admin", UserDetail("admin","admin"))

# Setup airports
jfk = Airport("John F. Kennedy International Airport", "JFK")
lax = Airport("Los Angeles International Airport", "LAX")
sfo = Airport("San Francisco International Airport", "SFO")
bkk = Airport("Suvarnabhumi Airport", "BKK")
cnx = Airport("Chiang Mai International Airport", "CNX")

airport_list = [jfk, lax, sfo, bkk, cnx]

# Create & Add Planes
boeing_777 = Plane("B777-001", "Boeing 777")
boeing_737 = Plane("B737-002", "Boeing 737")

controller.add_plane(boeing_777)
controller.add_plane(boeing_737)

# Generate Flights
controller.generate_random_flight_list(airport_list, num_flights=50)

# Display Flights
controller.display_all_flights()

luggage_system = LuggagePricingSystem()