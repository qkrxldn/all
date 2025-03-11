from fasthtml.common import *
from LoginHomeBack import *
import re

app, rt = fast_app()


# ================================
#           ROUTES
# ================================

# Welcome Page
@rt('/')
def home():
    # Fullscreen Background with Pastel Gradient and Centering
    background = Style("""
        body { 
            height: 100vh; 
            margin: 0;
            font-family: 'Arial', sans-serif;
            color: #555; /* Light text color */
            text-align: center;
            background-image: url('/Picture/fu7.jpg'); /* Add your background image */
            background-size: cover;
            background-position: center;
            background-attachment: cover;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center; /* Horizontally center */
            align-items: center; /* Vertically center */
        }
    """)

    go_to_login = Form(Button("Go to Login Page", 
            style="""background-color: #FFEB99;
            color: #333; width: 100%; 
            padding: 12px; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            font-weight: bold; 
            cursor: pointer; 
            transition: 0.3s ease; 
            border: 2px solid #F9D01C;""",
            
            onmouseover="this.style.backgroundColor='#F9D01C'",
            onmouseout="this.style.backgroundColor='#FFEB99'"),
        
        action="/login", 
        method="get",
    )

    return Title("Welcome to my Page"), background, go_to_login

# Registration Page
@rt("/register")
def get():
    form = Form(
        Input(id="email", name="email", placeholder="Email", type="email"),
        Input(id="password", name="password", placeholder="Password", type="password", 
              hx_post="/check-password", hx_trigger="input", hx_target="#password-message"),
        Div(id="password-message", style="color: red; font-size: 0.9em;"),
        Input(id="firstname", name="firstname", placeholder="First Name"),
        Input(id="lastname", name="lastname", placeholder="Last Name"),
        Button("Register"),
        action="/register", method="post"
    )
    return Titled("Register", form)

@rt("/check-password")
def post(password: str):
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\"_:{}|<>]", password):  # This checks for a special symbol
        return "Password must contain at least one special character (!@#$%^&* etc.)."

    return ""  # No message if password is valid

@rt("/register")
def post(email: str, password: str, firstname: str, lastname: str):
    # Backend password validation (same rules as in /check-password)
    if len(password) < 6:
        return Container(
            P("Password must be at least 6 characters long.", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if not re.search(r"[A-Z]", password):
        return Container(
            P("Password must contain at least one uppercase letter.", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if not re.search(r"[a-z]", password):
        return Container(
            P("Password must contain at least one lowercase letter.", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if not re.search(r"\d", password):
        return Container(
            P("Password must contain at least one number.", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if not re.search(r"[!@#$%^&*(),.?\"_:{}|<>]", password):
        return Container(
            P("Password must contain at least one special character (!@#$%^&* etc.).", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )

    # If password passes validation, proceed with registration
    message = controller.register(email, password, firstname, lastname)

    return RedirectResponse('/login', status_code=303) if "successful" in message else Container(
        P(message, style="color: red;"),
        Form(Button("Return to Register Page", type="submit", formaction="/register"))
    )
# Login Page
@rt("/login")
def get():
    return Container(
        H1("Login", style="text-align: center;"),
        Form(
            Label("Email:", Input(name="email", type="email", required=True), style="display: block;"),
            Label("Password:", Input(name="password", type="password", required=True), style="display: block;"),
            A("Don't have an account? Register here!",
            style="""
            display: block;
            text-align: center;
            font-family: 'Arial', sans-serif;
            color: #555; /* Light text color */
            margin-bottom: 10px;
            """ ,
            href="/register"),
            
            Button("Login", type="submit", style="display: block; margin: 0 auto;"),
            method="post",
            action="/login"
        )
    )

@rt("/login")
def post(email: str, password: str):
    message = controller.login(email, password)
    return RedirectResponse('/home', status_code=303) if "success" in message else Container(
        P(message), 
        Form(Button("Return to Login Page", 
            style="""background-color: #FFEB99;
            color: #333; width: 100%; 
            padding: 12px; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            font-weight: bold; 
            cursor: pointer; 
            transition: 0.3s ease; 
            border: 2px solid #F9D01C;""",
            
            onmouseover="this.style.backgroundColor='#F9D01C'",
            onmouseout="this.style.backgroundColor='#FFEB99'"),
        
        formaction="/login")
    )

# Home Page (Only Accessible if Logged In)
@rt("/home")
def get():
    user = controller.get_logged_in_user()
    if not user:
       return RedirectResponse('/login', status_code=303)

    return Container(
        H1(f"Hello {user.userdetail.firstname} {user.userdetail.lastname}", 
           style="text-align: center; color: #FFFFFF; margin: 20px 0;"),
        H6(f"Total points: {user.userdetail.points}", 
           style="text-align: center; color: #FFFFFF; margin: 20px 0;"),

        # Grid for cards
        Div(
            Card(
                H3("Find & Book", style="color: #ffee63;"),
                P("Find a flight"),
                Form(Button("View", type="submit", formaction="/flight_search")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            
            Card(
                H3("View profile", style="color: #ffee63;"),
                P("View my personal details"),
                Form(Button("Edit", type="submit", formaction="/profile")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            Card(
                H3("My bookings", style="color: #ffee63;"),
                P("View all booked flights"),
                Form(Button("View", type="submit", formaction="/my_booking")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            Card(
                H3("Promocode", style="color: #ffee63;"),
                P("View all of my promocodes"),
                Form(Button("View", type="submit", formaction="/promocode")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            Card(
                H3("Change password", style="color: #ffee63;"),
                P("New pass, new security"),
                Form(Button("Change", type="submit", formaction="/password")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 20px;"
        ),

        # Logout button at bottom
        Form(Button("Logout", type="submit", 
                    style="position: fixed; bottom: 20px; right: 20px;", formaction="/logout"))
    )

@rt("/profile")
def get():
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)

    return Container(
        H1("My Profile", style="text-align: center; color: #FFFFFF; margin: 20px 0;"),
        
        Card(
            H3("Profile Information", style="color: #ffee63;"),
            P(f"Name: {user.userdetail.firstname} {user.userdetail.lastname}"),
            P(f"Birthday: {user.userdetail.birthday}"),
            P(f"Gender: {user.userdetail.gender}"),
            P(f"Nationality: {user.userdetail.nationality}"),
            P(f"Phone: {user.userdetail.phone_number}"),
            P(f"Address: {user.userdetail.address}"),
            Form(
                Button("Edit", style="background-color: #ffee63; padding: 10px; font-size: 16px;", 
                    formaction="/edit-profile")
            ),
            
            Form(
                Button("Back", style="background-color: #ccc; padding: 10px; font-size: 16px;", 
                    formaction="/home")
            ),
            
            id="profile-card",
            style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
        ),
    )

@rt("/edit-profile", methods=["GET", "POST"])
def edit_profile(firstname: str="",lastname: str = "", birthday:str="",phone_number: str = "", address: str = "", gender: str="",nationality: str=""):
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)
    
    if firstname or lastname or phone_number or address or birthday or gender or nationality:  
        user.userdetail.edit_profile(firstname = firstname,lastname=lastname, phone_number=phone_number, address=address, birthday=birthday, gender=gender,nationality= nationality)

        # After saving, show the updated profile card
        return Card(
            H3("Profile Information", style="color: #ffee63;"),
            P(f"Name: {user.userdetail.firstname} {user.userdetail.lastname}"),
            P(f"Birthday: {user.userdetail.birthday}"),
            P(f"Gender: {user.userdetail.gender}"),
            P(f"Nationality: {user.userdetail.nationality}"),
            P(f"Phone: {user.userdetail.phone_number}"),
            P(f"Address: {user.userdetail.address}"),
            Form(
                Button("Edit", style="background-color: #ffee63; padding: 10px; font-size: 16px;", 
                    formaction="/edit-profile")
            ),
            
            Form(
                Button("Back", style="background-color: #ccc; padding: 10px; font-size: 16px;", 
                    formaction="/home")
            ),
            id="profile-card",
            style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
        )

    # Show the edit form
    return Card(
        H3("Edit Profile", style="color: #ffee63;"),
        Form(
            Label("Fitst Name"),
            Input(name="firstname", type="text", value=user.userdetail.firstname),
            
            Label("Last Name"),
            Input(name="lastname", type="text", value=user.userdetail.lastname),
            
            Label("Birthday"),
            Input(name="birthday", type="date", value=user.userdetail.birthday),
            
            Label("Phone Number"),
            Input(name="phone_number", type="text", value=user.userdetail.phone_number),
            
            Label("Address"),
            Input(name="address", type="text", value=user.userdetail.address),
            
            Label("National"),
            Select(
                Option("Thai", selected=user.userdetail.nationality == "Thai"),
                Option("American", selected=user.userdetail.nationality == "American"),
                Option("Other", selected=user.userdetail.nationality == "Other"),
                name = "nationality"
            ),
            
            Label("Gender"),
            Select(
                Option("Male", selected=user.userdetail.nationality == "Male"),
                Option("Female", selected=user.userdetail.nationality == "Female"),
                Option("Prefer not to tell", selected=user.userdetail.nationality == "Prefer not to tell"),
                name = "gender"
            ),
            
                
            
            Button("Save Changes", type="submit", 
                hx_post="/edit-profile", 
                hx_target="#profile-card", 
                hx_swap="outerHTML",
                style="background-color: #ffee63; padding: 10px; font-size: 16px;"
            ),
            method="post",
            style="display: flex; flex-direction: column; gap: 10px;"
        ),
        id="profile-card",
        style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
    )
    
@rt("/password", methods=["GET", "POST"])
def get():
    return Container(
        H2("Change Your Password", style="text-align: center; color: #fff; margin: 20px 0;"),

        # Password change form
        Form(
            Input(name="old_password", type="password", placeholder="Enter old password", required=True),
            Input(name="new_password", type="password", placeholder="Enter new password", required=True),
            Input(name="confirm_new_password", type="password", placeholder="Confirm new password", required=True),

            # Submit button
            Button("Submit", type="submit", style="font-size: 16px; background-color: #ffee63; padding: 10px;",
                   formaction="/passwordCheck"),
            style="text-align: center; padding: 20px; display: flex; flex-direction: column; gap: 10px;"
        ),

        # Separate Go Back button (not inside the form to prevent validation issues)
        Form(
            Button("Go Back", type="submit", style="font-size: 16px; background-color: #ccc; padding: 10px;",
                   formaction="/home"),
            style="text-align: center; margin-top: -40px; padding: 20px;"  # Moves the button closer to the form
        )
    )
     
@rt("/passwordCheck", methods=["GET","POST"])
def password_change(old_password: str = "", new_password: str = "", confirm_new_password: str = ""):
    user = controller.get_logged_in_user()  # Get the logged-in user
    if not user:
        return RedirectResponse('/login', status_code=303)

    result = user.change_password(old_password, new_password, confirm_new_password)

    color = "green" if "successfully" in result else "red"
    if "successfully" in result:
        controller.logout()
        return Container(H3(result, style=f"color: {color}; text-align: center;"),
                    Form(Button("Go Back to login page", type="submit", style="font-size: 16px; background-color: #ccc; padding: 10px;",
                    formaction="/logout")
                     )
        )
    else :
        return Container(H3(result, style=f"color: {color}; text-align: center;"),
                    Form(Button("Try again", type="submit", style="font-size: 16px; background-color: #ccc; padding: 10px;",
                    formaction="/password")
                    )
        )
# Logout
@rt("/logout")
def get():
    controller.logout()
    return RedirectResponse('/login', status_code=303)

@rt("/flight_search")
def search():
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #000000;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .form-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 320px;
            text-align: center;
        }
        .form-container select, .form-container input {
            width: 100%;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
            background-color: #fff;
            cursor: pointer;
        }
        .search-btn {
            background-color: #FFEB99;
            padding: 10px;
            font-size: 16px;
            width: 100%;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
        }
        .search-btn:hover {
            background-color: #F9D01C;
        }
    """)

    # Get airport list from controller
    airport_options = [
        Option(f"{airport.name} ({airport.code})", value=airport.code)
        for airport in [jfk, lax, sfo, bkk, cnx]  # Replace with `controller.airports` if you have a list
    ]

    origin = Select(*airport_options, name="origin", required=True)
    destination = Select(*airport_options, name="destination", required=True)
    date = Input(type="date", name="date", required=True)
    submit = Button("Search", type="submit", cls="search-btn")

    return Title("Search Flights"), styles, Div(
        H1("Find a Flight"),
        Form(
            Div(Label("From:"), origin),
            Div(Label("To:"), destination),
            Div(Label("Date:"), date),
            submit,
            action="/search_results",
            method="post",
            cls="form-container"
        ),
        Form(
            Div(
                Button("Go Back", type="submit", style="font-size: 16px; background-color: grey; padding: 10px; border-radius: 8px;", formaction="/home"),
                style="text-align: center; margin-top: -40px; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);"
            )
        )
    )

@rt("/search_results", methods=["POST"])
async def search_results(request):
    form_data = await request.form()

    origin_code = form_data.get("origin", "").strip()
    destination_code = form_data.get("destination", "").strip()
    date = form_data.get("date", "").strip()

    try:
        search_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return Div("Invalid date format!", cls="error")

    matching_flights = [
        flight for flight in controller.flights
        if flight.origin == origin_code
        and flight.destination == destination_code
        and datetime.strptime(flight.departure_time, "%Y-%m-%d %H:%M") >= search_date
    ]

    if not matching_flights:
        return Title("Search Results"), Div(
            Div("No flights found!", cls="results-container"),
            Form(Button("Back", type="submit", cls="back-btn"), action="/flight_search")
        )

    flight_cards = [
        Div(
            H3(f"{flight.origin} ✈ {flight.destination}", style="color: #F9D01C;"),
            P(f"Departure: {flight.departure_time}"),
            P(f"Arrival: {flight.arrive_time}"),
            P(f"Aircraft: {flight.plane.aircraft}"),
            Form(
                Hidden(name="flight_id", value=flight.flight_id),  # ✅ Store flight ID
                Button("Book This Flight", type="submit", cls="book-btn", formaction="/seat_map")  # ✅ Now goes to /seat_map
            ),
            cls="flight-card"
        )
        for flight in matching_flights
    ]

    styles = Style("""
        body { font-family: Arial, sans-serif; background-color: #000000; color: #333;
               display: flex; flex-direction: column; align-items: center;
               justify-content: center; min-height: 100vh; margin: 0; padding: 20px; }
        .results-container { background: white; padding: 20px; border-radius: 10px;
                             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); width: 90%; max-width: 600px;
                             text-align: center; }
        .flight-card { border: 2px solid #F9D01C; border-radius: 10px;
                       padding: 15px; margin: 10px 0; text-align: left; }
        .book-btn { background-color: #F9D01C; padding: 10px; font-size: 16px;
                    border: none; border-radius: 8px; font-weight: bold;
                    cursor: pointer; transition: 0.3s ease; width: 100%; }
        .book-btn:hover { background-color: #FFD700; }
        .back-btn { background-color: #ccc; padding: 10px; font-size: 16px;
                    border: none; border-radius: 8px; font-weight: bold;
                    cursor: pointer; transition: 0.3s ease; }
        .back-btn:hover { background-color: #bbb; }
    """)

    return Title("Search Results"), styles, Div(
        H1("Available Flights"),
        Div(*flight_cards, cls="results-container"),
        Form(Button("Back", type="submit", cls="back-btn"), action="/flight_search")
    )

@rt("/seat_map", methods=["GET", "POST"])
async def seat_map(request):

    max_seat_count = 5

    form_data = await request.form() if request.method == "POST" else request.query_params

    flight_id = form_data.get("flight_id", "").strip()
    flight = controller.get_flight_by_id(flight_id)

    if not flight:
        return Title("Error"), H1("Flight not found")

    styles = Style("""
        body { font-family: Arial, sans-serif; background-color: #000000; color: #333; }
        .container { background: white; padding: 20px; border-radius: 10px; 
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); max-width: 800px; margin: 0 auto; }
        .seat-map { display: flex; flex-direction: column; gap: 5px; margin: 20px 0; }
        .row { display: flex; justify-content: center; gap: 5px; margin-bottom: 5px; }
        .seat { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;
                border-radius: 5px; font-size: 12px; position: relative; }
        .seat-checkbox { position: absolute; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
        .seat-checkbox:checked + .seat-label { border: 2px solid #FF0000; }
        .seat-label { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
        
        /* Seat classes */
        .economy { background-color: #A0D6B4; } /* Light green for economy */
        .business { background-color: #8BB5FE; } /* Light blue for business */
        .first-class { background-color: #F3B5C1; } /* Light pink for first class */
        
        /* Seat availability */
        .available { border: 1px solid #888; cursor: pointer; }
        .booked { background-color: #ddd; color: #999; cursor: not-allowed; }
        
        /* Legend */
        .legend { display: flex; justify-content: center; gap: 15px; margin-bottom: 20px; }
        .legend-item { display: flex; align-items: center; gap: 5px; font-size: 12px; }
        .legend-color { width: 15px; height: 15px; border-radius: 3px; }
        
        /* Submit button */
        .submit-btn { background-color: #FFEB99; padding: 10px; font-size: 16px;
                     border: 2px solid #F9D01C; border-radius: 8px; font-weight: bold;
                     cursor: pointer; transition: 0.3s ease; margin-top: 20px; width: 100%; }
        .submit-btn:hover { background-color: #F9D01C; }
        
        /* Counter for selected seats */
        .seat-counter { font-weight: bold; margin: 10px 0; }
    """)

    # ✅ Ensure a booking is created
    if request.method == "GET":
        booking = controller.create_booking(flight_id)
        if not booking:
            return Title("Error"), H1("Could not create booking")
    else:
        booking_ref = form_data.get("booking_ref", "").strip()
        booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
        if not booking:
            return Title("Error"), H1("Booking not found")

    # ✅ Seat Map Logic
    seat_rows = {}
    for seat in flight.plane.seats:
        row_num = ''.join(filter(str.isdigit, seat.seat_id))
        if row_num not in seat_rows:
            seat_rows[row_num] = []
        seat_rows[row_num].append(seat)

    seat_map_html = []
    for row_num in sorted(seat_rows.keys(), key=int):
        seats_in_row = sorted(seat_rows[row_num], key=lambda s: ''.join(filter(str.isalpha, s.seat_id)))
        seat_buttons = []

        for seat in seats_in_row:
            seat_class = "available" if seat.is_available() else "booked"
            seat_type_class = "economy" if seat.seat_type == "Economy" else "business" if seat.seat_type == "Business" else "first-class"

            if seat.is_available():
                seat_buttons.append(
                    Div(
                        Input(type="checkbox", name="seat_ids", value=seat.seat_id, 
                              cls="seat-checkbox", 
                              onclick="checkSeatLimit(this)"),
                        Div(seat.seat_id, cls="seat-label"),
                        cls=f"seat {seat_class} {seat_type_class}"
                    )
                )
            else:
                seat_buttons.append(Div(seat.seat_id, cls=f"seat {seat_class} {seat_type_class}"))

        seat_map_html.append(Div(*seat_buttons, cls="row"))

    legend = Div(
        Div(Div(cls="legend-color economy"), "Economy", cls="legend-item"),
        Div(Div(cls="legend-color business"), "Business", cls="legend-item"),
        Div(Div(cls="legend-color first-class"), "First Class", cls="legend-item"),
        Div(Div(cls="legend-color available"), "Available", cls="legend-item"),
        Div(Div(cls="legend-color booked"), "Booked", cls="legend-item"),
        cls="legend"
    )

    # Javascript to limit seat selection to 5
    seat_limit_script = Script("""
        function checkSeatLimit(checkbox) {
            var checkboxes = document.querySelectorAll('input[name="seat_ids"]:checked');
            var maxSeats = 5; // Change this to dynamically fetch the max seat count
            document.getElementById('selected_seat_count').value = checkboxes.length;
            document.getElementById('selected-count').textContent = checkboxes.length;
            if (checkboxes.length > maxSeats) {
                checkbox.checked = false;
                alert(`You can only select up to ${maxSeats} seats`);
            }
        }
    """)

    return Title("Seat Selection"), styles, seat_limit_script, Div(
        H1(f"Select Seats for Flight {flight_id}"),
        P(f"From {flight.origin} to {flight.destination}"),
        P(f"Departure: {flight.departure_time}"),
        Div("Selected seats: ", Span("0", id="selected-count"), Span(f"/{max_seat_count}", id="max-seat-count"), cls="seat-counter"),
        legend,
        Form(
            Div(*seat_map_html, cls="seat-map"),
            Input(type="hidden", name="booking_ref", value=booking.booking_reference),
            Input(type="hidden", name="selected_seat_count", id="selected_seat_count", value="0"),
            Button("Continue with Selected Seats", type="submit", cls="submit-btn"),
            action="/luggage_calculator",
            method="post",
            cls="container"
        )
    )

@rt("/luggage_calculator", methods=["POST"])
async def luggage_calculator(request):
    # Get form data with await
    form_data = await request.form()

    # Get the selected seat count from the form data
    selected_seat_count = int(form_data.get("selected_seat_count", "1").strip())
    
    # Extract booking reference for passing along
    booking_ref = form_data.get("booking_ref", "").strip()
    
    # Get selected seats for passing along
    seat_ids = form_data.getlist("seat_ids") if hasattr(form_data, "getlist") else form_data.get("seat_ids", [])
    if not isinstance(seat_ids, list):
        seat_ids = [seat_ids]
    
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #000000;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .form-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 400px;
            text-align: center;
        }
        .form-container input {
            width: 100%;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
            background-color: #fff;
        }
        .calculate-btn {
            background-color: #FFEB99;
            padding: 10px;
            font-size: 16px;
            width: 100%;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
            margin-top: 20px;
        }
        .calculate-btn:hover {
            background-color: #F9D01C;
        }
        .person-container {
            border: 1px solid #eee;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .person-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .action-btn {
            background-color: #FFEB99;
            padding: 5px 10px;
            font-size: 14px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
        }
        .action-btn:hover {
            background-color: #F9D01C;
        }
        .add-person-btn {
            margin-top: 10px;
            background-color: #e6f7ff;
            border: 2px solid #1890ff;
        }
        .add-person-btn:hover {
            background-color: #bae7ff;
        }
        .seat-info {
            margin-bottom: 15px;
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 5px;
            border: 1px solid #d0e8ff;
        }
    """)

    # Add JavaScript for dynamic person management with seat count limitation
    script = Script("""
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize with one person container
        const seatCount = parseInt(document.getElementById('selected_seat_count').value, 10);
        
        // If we have more than one seat, add appropriate number of person containers
        for (let i = 1; i < seatCount; i++) {
            addPerson();
        }
        
        // Update the add person button visibility
        updateAddPersonButtonVisibility();
    });
    
    function addPerson() {
        const personCount = document.querySelectorAll('.person-container').length;
        const maxPersons = parseInt(document.getElementById('selected_seat_count').value, 10);
        
        if (personCount >= maxPersons) {
            alert(`Maximum ${maxPersons} people allowed based on selected seats.`);
            return;
        }

        const personContainer = document.createElement('div');
        personContainer.className = 'person-container';
        personContainer.id = `person-${personCount + 1}`;

        personContainer.innerHTML = `
            <div class="person-header">
                <h3>Person ${personCount + 1}</h3>
                <button type="button" class="action-btn" onclick="removePerson(${personCount + 1})">Remove</button>
            </div>
            <div>
                <label>Luggage Weight (kg):</label>
                <input type="number" name="weight_${personCount + 1}" min="1" max="50" value="20" required>
            </div>
        `;

        const addButton = document.getElementById('add-person-button');
        document.getElementById('people-container').insertBefore(personContainer, addButton);

        document.getElementById('person_count').value = personCount + 1;
        
        // Update add person button visibility
        updateAddPersonButtonVisibility();
    }
    
    function removePerson(personId) {
        const element = document.getElementById(`person-${personId}`);
        element.remove();
        
        // Renumber remaining people
        const personContainers = document.querySelectorAll('.person-container');
        personContainers.forEach((container, index) => {
            container.id = `person-${index + 1}`;
            container.querySelector('h3').textContent = `Person ${index + 1}`;
            container.querySelector('button').setAttribute('onclick', `removePerson(${index + 1})`);
            container.querySelector('input[type="number"]').name = `weight_${index + 1}`;
        });
        
        // Update the person count
        document.getElementById('person_count').value = personContainers.length;
        
        // Update add person button visibility
        updateAddPersonButtonVisibility();
    }
    
    function updateAddPersonButtonVisibility() {
        const personCount = document.querySelectorAll('.person-container').length;
        const maxPersons = parseInt(document.getElementById('selected_seat_count').value, 10);
        const addButton = document.getElementById('add-person-button');
        
        if (personCount >= maxPersons) {
            addButton.style.display = 'none';
        } else {
            addButton.style.display = 'block';
        }
    }
    """)

    # Hidden field to track the number of people (start with 1)
    person_count = Input(type="hidden", name="person_count", value="1", id="person_count")

    submit = Button("Calculate Total Price", type="submit", cls="calculate-btn")

    # Build the full UI
    return Title("Multi-Person Luggage Calculator"), styles, script, Div(
        H1("Calculate Luggage Price"),
        Form(
            # Display information about selected seats
            Div(cls="seat-info", children=[
                H3(f"Selected Seats: {selected_seat_count}"),
                P(f"You can add up to {selected_seat_count} people for luggage calculation.")
            ]),
            
            # Container for all person entries
            Div(
                H3("Luggage Information"),
                # Start with one person
                Div(
                    Div(
                        H3("Person 1"),
                        style="margin-bottom: 10px;"
                    ),
                    Div(Label("Luggage Weight (kg):"), 
                        Input(
                            type="number", 
                            name="weight_1", 
                            min="1", 
                            max="50", 
                            value="20",
                            required=True
                        )
                    ),
                    cls="person-container",
                    id="person-1"
                ),
                # Button to add more people
                Button(
                    "Add Person", 
                    type="button", 
                    onclick="addPerson()",
                    cls="action-btn add-person-btn",
                    id="add-person-button"
                ),
                id="people-container"
            ),
            
            # Hidden input for person count
            person_count,
            
            # Hidden input for the selected seat count
            Input(type="hidden", id="selected_seat_count", name="selected_seat_count", value=str(selected_seat_count)),
            
            # Pass along the booking reference and selected seats
            Input(type="hidden", name="booking_ref", value=booking_ref),
            *[Input(type="hidden", name="seat_ids", value=seat_id) for seat_id in seat_ids],
            
            # Submit button
            submit,
            action="/passenger_details",
            method="post",
            cls="form-container"
        )
    )

@rt("/passenger_details", methods=["GET", "POST"])
async def passenger_details(request):
    if request.method == "POST":
        form_data = await request.form()
        
        booking_ref = form_data.get("booking_ref", "").strip()
        seat_ids = form_data.getlist("seat_ids") if hasattr(form_data, "getlist") else form_data.get("seat_ids", [])
        if not isinstance(seat_ids, list):
            seat_ids = [seat_ids]
        
        person_count = int(form_data.get("person_count", "1"))
        total_weight = 0
        person_weights = []
    
        for i in range(1, person_count + 1):
            weight_key = f"weight_{i}"
            if weight_key in form_data:
                try:
                    weight = float(form_data.get(weight_key, 0))
                    person_weights.append(weight)
                    total_weight += weight
                except ValueError:
                    person_weights.append(0)

        booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
        
        if booking:
            booking.add_luggage(Luggage(total_weight))

        luggage_weight_price = booking.luggage.calculate_price()

        seat_info = []
        for seat_id in seat_ids:
            seat_info.append({"id": seat_id,})
        
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 600px;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .booking-info {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .booking-ref {
            font-weight: bold;
        }
        .passenger-form {
            margin-top: 20px;
        }
        .passenger-section {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #FFEB99;
        }
        .passenger-title {
            font-weight: bold;
            margin-bottom: 15px;
            color: #555;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        .action-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
        }
        .confirm-btn {
            background-color: #FFEB99;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
        }
        .confirm-btn:hover {
            background-color: #F9D01C;
        }
        .back-btn {
            background-color: #f0f0f0;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #ddd;
        }
        .back-btn:hover {
            background-color: #e0e0e0;
        }
        .required {
            color: red;
        }
    """)
    
    passenger_forms = []
    for i, seat in enumerate(seat_info):
        passenger_forms.append(
            Div(
                H3(f"Seat {seat['id']}", cls="passenger-title"),
                Div(
                    Label("First Name", For=f"first_name_{i}"),
                    Span("*", cls="required"),
                    Input(type="text", id=f"first_name_{i}", name=f"first_name_{i}", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Last Name", For=f"last_name_{i}"),
                    Span("*", cls="required"),
                    Input(type="text", id=f"last_name_{i}", name=f"last_name_{i}", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Date of Birth", For=f"dob_{i}"),
                    Span("*", cls="required"),
                    Input(type="date", id=f"dob_{i}", name=f"dob_{i}", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Phone", For=f"phone_{i}"),
                    Span("*", cls="required"),
                    Input(type="tel", id=f"phone_{i}", name=f"phone_{i}", required=True),
                    cls="form-group"
                ),
                cls="passenger-section"
            )
        )
    
    return Title("Passenger Details"), styles, Div(
        H1("Passenger Details", cls="header"),
        
        Div(
            H3("Booking Information:"),
            P(Span("Booking Reference: ", cls="booking-ref"), booking_ref),
            P(f"Number of passengers: {person_count}"),
            P("Please enter details for all passengers"),
            cls="booking-info"
        ),
        Form(
            *passenger_forms,
            *[Input(type="hidden", name="seat_ids", value=seat_id) for seat_id in seat_ids],
            Input(type="hidden", name="booking_ref", value=booking_ref),
            Input(type="hidden", name="person_count", value=str(person_count)),
            Input(type="hidden", name="luggage_weight_price", value=luggage_weight_price),
            Div(
                Button("Back to Luggage", type="button", cls="back-btn", onclick="history.back()"),
                Button("Continue to Review", type="submit", cls="confirm-btn"),
                cls="action-buttons"
            ),
            action="/booking_summary",
            method="post",
            cls="passenger-form"
        ),
        cls="container"
    )

@rt("/booking_summary", methods=["POST"])
async def booking_summary(request):
    form_data = await request.form()
    booking_ref = form_data.get("booking_ref", "").strip()
    
    booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    flight = controller.get_flight_by_id(booking.flight.flight_id)
    if not flight:
        return Title("Error"), H1("Flight not found")
    
    if not hasattr(booking, 'passengers') or not booking.passengers:
        passenger_data = []
        person_count = int(form_data.get("person_count", "1"))
        
        for i in range(person_count):
            first_name = form_data.get(f"first_name_{i}", "")
            last_name = form_data.get(f"last_name_{i}", "")
            phone = form_data.get(f"phone_{i}", "")
            dob = form_data.get(f"dob_{i}", "")
            
            passenger = Passenger(
                firstname=first_name,
                lastname=last_name,
                phone=phone,
                dob=dob,
            )           
            passenger_data.append(passenger)
        
        booking.passengers = passenger_data
        
        seat_ids = form_data.getlist("seat_ids") if hasattr(form_data, "getlist") else form_data.get("seat_ids", [])
        if not isinstance(seat_ids, list):
            seat_ids = [seat_ids]
            
        booking.passenger_seats = {}
        for i, passenger in enumerate(booking.passengers):
            if i < len(seat_ids):
                booking.passenger_seats[passenger.id] = seat_ids[i]
                booking.add_seat(seat_ids[i])
    
    passenger_items = []
    seat_prices = {"Economy": 500, "Business": 1200, "First Class": 2500}
    total_seat_price = 0
    
    seat_details = []
    for passenger in booking.passengers:
        seat_id = booking.passenger_seats.get(passenger.id, 'Not assigned')
        seat_class = "Economy"

        if seat_id != 'Not assigned':
            seat = next((s for s in flight.plane.seats if s.seat_id == seat_id), None)
            if seat and hasattr(seat, 'seat_type'):
                seat_class = seat.seat_type
        
        seat_price = seat_prices.get(seat_class, 500)
        total_seat_price += seat_price
        
        seat_details.append({
            "id": seat_id,
            "class": seat_class,
            "price": seat_price
        })
        
        passenger_items.append(
            Div(
                P(f"Name: {passenger.firstname} {passenger.lastname}"),
                P(f"Contact: {passenger.phone}"),
                P(f"Seat: {seat_id} ({seat_class}) - ${seat_price}"),
                cls="passenger-item"
            )
        )
    
    luggage_weight_price = form_data.get("luggage_weight_price", "").strip()

    total_price = total_seat_price + int(luggage_weight_price)
    
    booking.create_payment(total_price)

    styles = Style("""
    body {
        font-family: Arial, sans-serif;
        background-color: #000000;
        color: #333;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        margin: 0;
        padding: 20px;
    }
    .container {
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        width: 90%;
        max-width: 500px;
        text-align: center;
    }
    .success-icon {
        font-size: 60px;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .booking-ref {
        background: #f5f5f5;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        margin: 20px 0;
    }
    .home-btn {
        background-color: #FFEB99;
        padding: 12px;
        font-size: 16px;
        width: 200px;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s ease;
        border: 2px solid #F9D01C;
        margin-top: 20px;
    }
    .home-btn:hover {
        background-color: #F9D01C;
    }
    .details {
        margin-top: 20px;
        text-align: left;
    }
""")

    return Title("Booking Summary"), styles, Div(
        Div(
            H1("Booking Summary"),
            P("Please review your booking details before confirming"),
            cls="header"
        ),
        
        Div(f"Booking Reference: {booking_ref}", cls="booking-ref"),
        
        Div(
            H2("Flight Details"),
            Div(
                P(f"Flight: {flight.origin} to {flight.destination}"),
                P(f"Departure: {flight.departure_time}"),
                P(f"Arrival: {flight.arrive_time}"),
                P(f"Aircraft: {flight.plane.aircraft}"),
                cls="flight-details"
            ),
            cls="section"
        ),
        
        Div(
            H2("Passengers"),
            Div(*passenger_items, cls="passenger-list"),
            cls="section"
        ),
        
        Div(
            H2("Luggage Information"),
            Div(
                P(f"Total Luggage Weight: {booking.luggage.kilogram} kg"),
                P(f"Luggage Fee: ${luggage_weight_price}"),
                cls="luggage-details"
            ),
            cls="section"
        ),
        
        Div(
            H2("Price Summary"),
            Div(
                Div(
                    Div("Seat Prices:", cls="price-label"),
                    Div(f"${total_seat_price}", cls="price-value"),
                    cls="price-row"
                ),
                Div(
                    Div("Luggage Fee:", cls="price-label"),
                    Div(f"${luggage_weight_price}", cls="price-value"),
                    cls="price-row"
                ),
                Div(
                    Div("Total Price:", cls="price-label"),
                    Div(f"${total_price}", cls="price-value"),
                    cls="total-price price-row"
                ),
                cls="price-summary"
            ),
            cls="section"
        ),
        
        Div(
            Form(
                Button("Back", type="submit", cls="back-btn"),
                action="/passenger_details",
                method="get"
            ),
            Form(
                Input(type="hidden", name="booking_ref", value=booking_ref),
                Input(type="hidden", name="total_price", value=str(total_price)),
                Button("Confirm and Pay", type="submit", cls="confirm-btn"),
                action="/payment",
                method="post"
            ),
            cls="action-buttons"
        ),
        
        cls="container"
    )

@rt("/payment", methods=["POST"])
async def payment(request):
    form_data = await request.form()
    booking_ref = form_data.get("booking_ref", "").strip()
    total_price = float(form_data.get("total_price", "0").strip())
    
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #000000;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 400px;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
            text-align: left;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .submit-btn {
            background-color: #FFEB99;
            padding: 10px;
            font-size: 16px;
            width: 100%;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
            margin-top: 20px;
        }
        .submit-btn:hover {
            background-color: #F9D01C;
        }
    """)
    
    booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    return Title("Payment"), styles, Div(
        H1("Payment Details"),
        P(f"Total Amount: ${total_price}"),
        Form(
            Div(
                Label("Card Type:"),
                Select(
                    Option("DebitCard"),
                    Option("CreditCard"),
                    name="card_type",
                    required=True
                ),
                cls="form-group"
            ),
            Div(
                Label("Card Number:"),
                Input(type="text", name="card_number", placeholder="XXXX XXXX XXXX XXXX", required=True),
                cls="form-group"
            ),
            Div(
                Div(
                    Label("Expiry Date:"),
                    Input(type="text", name="expiry", placeholder="MM/YY", required=True),
                ),
                Div(
                    Label("CVV:"),
                    Input(type="text", name="cvv", placeholder="XXX", required=True),
                ),
                cls="card-details form-group"
            ),
            Div(
                Input(type="text", name="promocode", placeholder="Enter promocode (if any)"),
                Button("Apply", type="button"),
                cls="promocode"
            ),
            Input(type="hidden", name="booking_ref", value=booking_ref),
            Button("Pay Now", type="submit", cls="payment-btn"),
            action="/payment_confirmation",
            method="post",
        ),
        cls="container"
    )

@rt("/payment_confirmation", methods=["POST"])
async def payment_confirmation(request):
    form_data = await request.form()
    booking_ref = form_data.get("booking_ref", "").strip()
    card_type = form_data.get("card_type", "").strip()
    card_number = form_data.get("card_number", "").strip()
    exp = form_data.get("expiry", "").strip()
    cvv = form_data.get("cvv", "").strip()

    booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    booking.update_booking_status()
    controller.add_booking_history(booking)
    booking.payment.process_payment(card_type, card_number, cvv, exp)
    
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #000000;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 500px;
            text-align: center;
        }
        .success-icon {
            font-size: 60px;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .booking-ref {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px 0;
        }
        .home-btn {
            background-color: #FFEB99;
            padding: 12px;
            font-size: 16px;
            width: 200px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
            margin-top: 20px;
        }
        .home-btn:hover {
            background-color: #F9D01C;
        }
        .details {
            margin-top: 20px;
            text-align: left;
        }
    """)
    
    return Title("Payment Confirmed"), styles, Div(
        Div("✓", cls="success-icon"),
        H1("Payment Successful!"),
        P("Your flight booking has been confirmed."),
        Div(f"Booking Reference: {booking_ref}", cls="booking-ref"),
        Form(
            Button("Return to Home", type="submit", cls="home-btn"),
            action="/home",
            method="get"
        ),
        cls="container"
    )

@rt("/my_booking")
def get():
    pass

serve()

