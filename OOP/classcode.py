class Controller:
    def __init__(self):
        self.plane_list = []
        self.account_list = []
        self.flightRoute_list = []
        self.booking_list = []

    def flight_search(self):
        pass

    def booking_search(self):
        pass

class Seat:
    def __init__(self, seat_id, seat_type):
        self.seat_id = seat_id
        self.seat_type = seat_type
        self.seat_status = True

    def update_seat_status(self):
        pass

class Airport:
    def __init__(self, name):
        self.name = name

class Plane:
    def __init__(self, plane_id, aircraft, seats):
        self.plane_id = plane_id
        self.aircraft = aircraft
        self.seats = []

class FlightRoute:
    def __init__(self, origin, destination, departure_time, arrive_time):
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrive_time = arrive_time

class Booking:
    def __init__(self, booking_reference, status, flight, passenger_details, promocode_discount, price, luggage):
        self.booking_reference = booking_reference
        self.status = False
        self.flight = flight
        self.passenger_details = passenger_details
        self.promocode_discount = promocode_discount
        self.price = price
        self.luggage = luggage
        
    def edit_booking(self):
        pass

    def price_cal(self):
        pass

    def update_passenger_datails(self):
        pass
    
    def get_passenger_details(self):
        pass

    def update_booking_status(self):
        pass

class Luggage:
    def __init__(self, kilogram, price_rate):
        self.kilogram = kilogram
        self.price_rate = price_rate

class Payment:
    def __init__(self, ticket_price, amount):
        self.ticket_price = ticket_price
        self.amount = amount

    def process_payment(self, payment_method):
        return payment_method.pay()

class PaymentMethod:
    def __init__(self, method_id):
        self.method_id = method_id

class OnlineBanking(PaymentMethod):
    def __init__(self, method_id="OnlineBanking"):
        super().__init__(method_id)

    def pay(self):
        pass

class Card(PaymentMethod):
    def __init__(self, method_id, card_number):
        super().__init__(method_id)
        self.card_number = card_number

class CreditCard(Card):
    def __init__(self, card_number):
        super().__init__("CreditCard", card_number)

    def pay(self):
        pass

class DebitCard(Card):
    def __init__(self, card_number):
        super().__init__("DebitCard", card_number)

    def pay(self):
        pass

class Account:
    def __init__(self, password, email, purchased_history, user_detail):
        self.password = password
        self.email = email
        self.purchased_history = []
        self.user_detail = user_detail

    def login(self):
        pass

    def register(self):
        pass

    def forgot_pass(self):
        pass

    def get_booking_list(self):
        return []

    def get_promocode(self):
        return self.user_detail.get_promocode()

    def use_points(self, points):
        if self.user_detail.point >= points:
            self.user_detail.point -= points
            return True
        return False

    def change_password(self, old_password, new_password):
        if self.password == old_password:
            self.password = new_password
            return True
        return False

    def update_purchased_history(self):
        pass

    def logout(self):
        pass

class UserDetail:
    def __init__(self, firstname, lastname, birthday, gender, identification, nationality, phone_number, address, point, promocode_list):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.gender = gender
        self.identification = identification
        self.nationality = nationality
        self.phone_number = phone_number
        self.address = address
        self.point = point
        self.promocode_list = promocode_list

    def edit_profile(self, firstname=None, lastname=None, phone_number=None, address=None):
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if phone_number:
            self.phone_number = phone_number
        if address:
            self.address = address

    def get_promocode(self):
        return self.promocode_list

class Promocode:
    def __init__(self, code, discount_percent, expiration_date):
        self.code = code
        self.discount_percent = discount_percent
        self.expiration_date = expiration_date

    def is_valid(self):
        return True

class PassengerDetail:
    def __init__(self, passengerType, passengerName, contact, birthday, seat):
        self.passengerType = passengerType
        self.passengerName = passengerName
        self.contact = contact
        self.birthday = birthday
        self.seat = seat

    def get_seat(self):
        pass

    def update_passenger_details(self):
        pass

class PassengerType:
    def __init__(self, type, discount_percent):
        self.type = type
        self.discount_percent = discount_percent

# Mockup Data
seat1 = Seat("1A", "Economy")
plane1 = Plane("P001", "Boeing 737", [seat1])
flight1 = FlightRoute("JFK", "LAX", "10:00", "13:00")
promocode1 = Promocode("DISCOUNT10", 10, "2025-12-31")
promocode2 = Promocode("SALE20", 20, "2025-06-30")
user_detail1 = UserDetail("John", "Doe", "1990-05-15", "Male", "123456789", "USA", "555-1234", "123 Main St", 100, [promocode1, promocode2])
account1 = Account("password123", "john.doe@example.com", [], user_detail1)
controller = Controller()
controller.account_list.append(account1)