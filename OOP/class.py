class Flight:
    def __init__(self, plane):
        self.__plane = plane
        self.__flight_route_list = []
        self.__airport_list = []

    def search_flight(self, origin, destination):
        for route in self.__flight_route_list:
            if route.origin == origin and route.destination == destination:
                return route
        return None

    def filter_flights(self):
        pass


class SeatClass:
    def __init__(self, seat_id, seat_type):
        self.__seat_id = seat_id
        self.__seat_type = seat_type

    @property
    def seat_id(self):
        return self.__seat_id

    @property
    def seat_type(self):
        return self.__seat_type


class Airport:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name


class Plane:
    def __init__(self, plane_id, aircraft, seat_classes):
        self.__plane_id = plane_id
        self.__aircraft = aircraft
        self.__seat_classes = seat_classes

    @property
    def plane_id(self):
        return self.__plane_id

    @property
    def aircraft(self):
        return self.__aircraft

    @property
    def seat_classes(self):
        return self.__seat_classes


class Booking:
    def __init__(self, booking_reference, payment, status, flight, promocode_discount, price):
        self.__booking_reference = booking_reference
        self.__payment = payment
        self.__status = status
        self.__flight = flight
        self.__passenger_detail_list = []
        self.__promocode_discount = promocode_discount
        self.__price = price

    def edit_booking(self):
        pass

    def calculate_price(self):
        pass


class Payment:
    def __init__(self, ticket_price, amount):
        self.__ticket_price = ticket_price
        self.__amount = amount

    def process_payment(self):
        pass


class Card(Payment):
    pass


class DebitCard(Card):
    pass


class CreditCard(Card):
    pass


class OnlineBanking(Payment):
    pass


class User:
    def __init__(self, email, points):
        self.__email = email
        self.__points = points
        self.__purchase_history = []

    def login(self, email, password):
        pass

    def register(self, email, password):
        pass

    def use_points(self, points_to_use):
        pass


class PromoCode:
    def __init__(self, code, discount_percent, expiration_date):
        self.__code = code
        self.__discount_percent = discount_percent
        self.__expiration_date = expiration_date

    def is_valid(self, current_date):
        pass


class FlightRoute:
    def __init__(self, origin, destination, departure_time, arrival_time):
        self.__origin = origin
        self.__destination = destination
        self.__departure_time = departure_time
        self.__arrival_time = arrival_time

    @property
    def origin(self):
        return self.__origin

    @property
    def destination(self):
        return self.__destination


class PassengerDetail:
    def __init__(self, passenger_type, passenger_name, contact, birthday):
        self.__passenger_type = passenger_type
        self.__passenger_name = passenger_name
        self.__contact = contact
        self.__birthday = birthday


class PassengerType:
    def __init__(self, type_name, discount_percent):
        self.__type_name = type_name
        self.__discount_percent = discount_percent


class PurchaseHistory:
    def __init__(self, booking):
        self.__booking = booking


class Membership:
    def __init__(self, user, discount_percent):
        self.__user = user
        self.__discount_percent = discount_percent
