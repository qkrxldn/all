from fasthtml.common import *
from main_back import *
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
                Form(Button("View", type="submit", formaction="/manage-booking")),
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
        .error-message {
            color: red;
            font-size: 14px;
            margin-top: 5px;
            display: none;
        }
    """)

    # Get airport list from controller
    airport_options = [
        Option(f"{airport.name} ({airport.code})", value=airport.code)
        for airport in controller.airports  # Replace with `controller.airports` if you have a list
    ]

    # Get today's date for min attribute on date input
    today = datetime.now().strftime("%Y-%m-%d")

    # Add JavaScript for validation
    validation_script = Script("""
        function validateForm() {
            const origin = document.getElementById('origin').value;
            const destination = document.getElementById('destination').value;
            const date = document.getElementById('flight-date').value;
            const today = new Date().toISOString().split('T')[0];
            
            // Reset error messages
            document.getElementById('same-airports-error').style.display = 'none';
            document.getElementById('past-date-error').style.display = 'none';
            
            // Check if origin and destination are the same
            if (origin === destination) {
                document.getElementById('same-airports-error').style.display = 'block';
                return false;
            }
            
            // Check if date is in the past
            if (date < today) {
                document.getElementById('past-date-error').style.display = 'block';
                return false;
            }
            
            return true;
    }
    """)

    origin = Select(*airport_options, name="origin", id="origin", required=True)
    destination = Select(*airport_options, name="destination", id="destination", required=True)
    date = Input(type="date", name="date", id="flight-date", min=today, required=True)
    submit = Button("Search", type="submit", cls="search-btn")

    return Title("Search Flights"), styles, validation_script, Div(
        H1("Find a Flight"),
        Form(
            Div(Label("From:"), origin),
            Div(id="same-airports-error", cls="error-message", 
                children=["Origin and destination cannot be the same."]),
            Div(Label("To:"), destination),
            Div(Label("Date:"), date),
            Div(id="past-date-error", cls="error-message", 
                children=["Please select a date in the future."]),
            submit,
            action="/search_results",
            method="post",
            cls="form-container",
            onsubmit="return validateForm()"
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
        
        /* Disabled button style */
        .submit-btn.disabled {
            background-color: #f0f0f0;
            border-color: #ccc;
            color: #999;
            cursor: not-allowed;
        }
        
        /* Counter for selected seats */
        .seat-counter { font-weight: bold; margin: 10px 0; }
        
        /* Error message */
        .error-message { color: #e74c3c; font-weight: bold; margin: 10px 0; }
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

    # Check for error message
    error = form_data.get("error", "")
    error_message = Div("Please select at least one seat to continue.", cls="error-message") if error == "no_seats" else ""

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

    # Javascript to limit seat selection to 5 and enforce at least 1 seat selection
    seat_limit_script = Script("""
        function checkSeatLimit(checkbox) {
            var checkboxes = document.querySelectorAll('input[name="seat_ids"]:checked');
            var maxSeats = 5; // Max seat count
            var submitButton = document.getElementById('submit_button');
            
            document.getElementById('selected_seat_count').value = checkboxes.length;
            document.getElementById('selected-count').textContent = checkboxes.length;
            
            // Disable or enable submit button based on selection count
            if (checkboxes.length === 0) {
                submitButton.disabled = true;
                submitButton.classList.add('disabled');
            } else {
                submitButton.disabled = false;
                submitButton.classList.remove('disabled');
            }
            
            if (checkboxes.length > maxSeats) {
                checkbox.checked = false;
                alert(`You can only select up to ${maxSeats} seats`);
                
                // Update count after rejecting the check
                checkboxes = document.querySelectorAll('input[name="seat_ids"]:checked');
                document.getElementById('selected_seat_count').value = checkboxes.length;
                document.getElementById('selected-count').textContent = checkboxes.length;
            }
        }
        
        // Initialize button state when page loads
        window.onload = function() {
            checkSeatLimit(null);
        }
        
        // Add form validation
        function validateForm(form) {
            var checkboxes = document.querySelectorAll('input[name="seat_ids"]:checked');
            if (checkboxes.length === 0) {
                alert('Please select at least one seat to continue.');
                return false;
            }
            return true;
        }
    """)

    return Title("Seat Selection"), styles, seat_limit_script, Div(
        H1(f"Select Seats for Flight {flight_id}"),
        P(f"From {flight.origin} to {flight.destination}"),
        P(f"Departure: {flight.departure_time}"),
        Div("Selected seats: ", Span("0", id="selected-count"), Span(f"/{max_seat_count}", id="max-seat-count"), cls="seat-counter"),
        error_message,
        legend,
        Form(
            Div(*seat_map_html, cls="seat-map"),
            Input(type="hidden", name="booking_ref", value=booking.booking_reference),
            Input(type="hidden", name="flight_id", value=flight_id),
            Input(type="hidden", name="selected_seat_count", id="selected_seat_count", value="0"),
            Button("Continue with Selected Seats", type="submit", id="submit_button", cls="submit-btn"),
            action="/luggage_calculator",
            method="post",
            onsubmit="return validateForm(this);",
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
        
        for i in range(1, person_count + 1):
            try:
                weight = float(form_data.get(f"weight_{i}", 0))
                total_weight += weight
            except ValueError:
                pass

        booking = controller.find_booking_by_reference(booking_ref)
        booking.add_luggage(Luggage(total_weight))
        luggage_weight_price = booking.luggage.calculate_price()

        seat_info = [{"id": seat_id} for seat_id in seat_ids]
        
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #fff;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 800px;
            margin: 20px auto;
            background: #1e1e1e;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(255, 255, 255, 0.1);
        }

        h1, h2, h3 {
            color: #fff;
            text-align: center;
        }

        p { color: #bbb; }

        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            margin-bottom: 15px;
        }

        label {
            font-weight: bold;
            margin-bottom: 5px;
        }

        input, select, button {
            padding: 10px;
            border: 1px solid #444;
            border-radius: 5px;
            background: #222;
            color: #fff;
        }

        button {
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover { background-color: #0056b3; }

        .passenger-section {
            padding: 15px;
            background: #2a2a2a;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .passenger-title { color: #007BFF; }

        .booking-info {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }

        .action-buttons {
            display: flex;
            justify-content: space-between;
        }

        .back-btn { background-color: #6c757d; }
        .back-btn:hover { background-color: #5a6268; }
        .confirm-btn { background-color: #28a745; }
        .confirm-btn:hover { background-color: #218838; }

        .booking-ref {
            font-size: 18px;
            font-weight: bold;
            color: #007BFF;
            text-align: center;
            margin-bottom: 15px;
        }

        .passenger-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .passenger-item {
            padding: 10px;
            border-radius: 5px;
            background: #2a2a2a;
        }

        .price-summary {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 5px;
        }

        .price-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        .total-price {
            font-weight: bold;
            font-size: 18px;
            color: #28a745;
        }

        .error-message {
            color: #dc3545;
            font-size: 12px;
            margin-top: 5px;
        }

        input:invalid { border-color: #dc3545; }

        .validation-info {
            font-size: 12px;
            color: #6c757d;
            margin-top: 3px;
        }
    """)

    validation_script = Script("""
        // Function to calculate age from DOB
        function calculateAge(birthDate) {
            const today = new Date();
            const birth = new Date(birthDate);
            let age = today.getFullYear() - birth.getFullYear();
            const monthDiff = today.getMonth() - birth.getMonth();
            
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
                age--;
            }
            
            return age;
        }

        // Validation functions
        function validateDOB(input) {
            const age = calculateAge(input.value);
            const errorElement = document.getElementById(input.id + '-error');
            
            if (age < 5) {
                errorElement.textContent = 'Passenger must be at least 5 years old';
                input.setCustomValidity('Passenger must be at least 5 years old');
                return false;
            } else {
                errorElement.textContent = '';
                input.setCustomValidity('');
                return true;
            }
        }

        function validatePhone(input) {
            const phone = input.value;
            const phonePattern = /^[0-9]{10}$/;
            const errorElement = document.getElementById(input.id + '-error');
            
            if (!phonePattern.test(phone)) {
                errorElement.textContent = 'Phone number must be exactly 10 digits';
                input.setCustomValidity('Phone number must be exactly 10 digits');
                return false;
            } else {
                errorElement.textContent = '';
                input.setCustomValidity('');
                return true;
            }
        }

        function formatPhoneNumber(input) {
            let phone = input.value.replace(/\\D/g, '');
            if (phone.length > 10) phone = phone.substring(0, 10);
            input.value = phone;
            validatePhone(input);
            
            const countElement = document.getElementById(input.id + '-count');
            if (countElement) countElement.textContent = phone.length + '/10';
        }

        // Set max date for DOB fields (must be at least 5 years old)
        function setMaxDate() {
            const dobInputs = document.querySelectorAll('input[type="date"]');
            const maxDate = new Date(new Date().getFullYear() - 5, new Date().getMonth(), new Date().getDate());
            const maxDateStr = maxDate.toISOString().split('T')[0];
            
            dobInputs.forEach(input => input.setAttribute('max', maxDateStr));
        }

        // Validate form before submission
        function validateForm(form) {
            let isValid = true;
            
            form.querySelectorAll('input[type="date"]').forEach(input => {
                if (!validateDOB(input)) isValid = false;
            });
            
            form.querySelectorAll('input[type="tel"]').forEach(input => {
                if (!validatePhone(input)) isValid = false;
            });
            
            return isValid;
        }

        // Initialize validation when page loads
        window.onload = function() {
            setMaxDate();
            
            document.querySelectorAll('input[type="date"]').forEach(input => {
                input.addEventListener('change', function() { validateDOB(this); });
            });
            
            document.querySelectorAll('input[type="tel"]').forEach(input => {
                input.addEventListener('input', function() { formatPhoneNumber(this); });
                const countElement = document.getElementById(input.id + '-count');
                if (countElement) countElement.textContent = input.value.length + '/10';
            });
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
                    Div(id=f"dob_{i}-error", cls="error-message"),
                    Div("Passenger must be at least 5 years old", cls="validation-info"),
                    cls="form-group"
                ),
                Div(
                    Label("Phone", For=f"phone_{i}"),
                    Span("*", cls="required"),
                    Input(type="tel", id=f"phone_{i}", name=f"phone_{i}", required=True, 
                          pattern="[0-9]{10}", maxlength="10"),
                    Div(id=f"phone_{i}-error", cls="error-message"),
                    Div(
                        Span("Must be exactly 10 digits", cls="validation-info"),
                        Span(id=f"phone_{i}-count", cls="validation-info", style="float: right;"),
                    ),
                    cls="form-group"
                ),
                cls="passenger-section"
            )
        )
    
    return Title("Passenger Details"), styles, validation_script, Div(
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
            onsubmit="return validateForm(this)",
            cls="passenger-form"
        ),
        cls="container"
    )

@rt("/booking_summary", methods=["POST"])
async def booking_summary(request):
    form_data = await request.form()
    booking_ref = form_data.get("booking_ref", "").strip()
    
    booking = controller.find_booking_by_reference(booking_ref)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    flight = controller.get_flight_by_id(booking.flight.flight_id)
    if not flight:
        return Title("Error"), H1("Flight not found")
    
    controller.process_passenger_data(booking, form_data)
    controller.assign_seats_to_passengers(booking, form_data)
    
    total_seat_price = 0
    passenger_items = []
    
    passenger_items, total_seat_price = controller.calculate_passenger_seat_details(booking, flight)
    
    luggage_weight_price = float(form_data.get("luggage_weight_price", "0"))
    total_price = total_seat_price + luggage_weight_price
    
    booking.create_payment(total_price)

    code = form_data.get("code", "").strip()

    user = controller.get_logged_in_user()

    discount_percent = user.userdetail.search_promo(code)

    original_price = booking.payment.price

    booking.payment.discount_payment(discount_percent)
    
    discounted_price = booking.payment.price

    user.userdetail.use_promo(code)

    return Title("Booking Summary"), Div(
        Div(
            H1("Booking Summary"),
            P("Please review your booking details before confirming"),
            cls="header",
        ),
        
        Div(f"Booking Reference: {booking_ref}", cls="booking-ref"),
        
        Div(
            H2("Flight Details"),
            Div(
                P(f"Flight: {flight.origin} to {flight.destination}"),
                P(f"Departure: {flight.departure_time}"),
                P(f"Arrival: {flight.arrive_time}"),
                P(f"Aircraft: {flight.plane.aircraft}"),
                cls="flight-details",
            ),
            cls="section"
        ),
        
        Div(
            H2("Passengers"),
            Div(*passenger_items, cls="passenger-list"),
            cls="section",
        ),
        
        Div(
            H2("Luggage Information"),
            Div(
                P(f"Total Luggage Weight: {booking.luggage.kilogram} kg"),
                P(f"Luggage Fee: ${luggage_weight_price}"),
                cls="luggage-details",
            ),
            cls="section"
        ),
        
        Div(
            H2("Price Summary"),
            P(f"Seat Prices: ${total_seat_price}"),
            P(f"Luggage Fee: ${luggage_weight_price}"),
            P(f"Total Price: ${original_price}"),
            P(f"Price After Use Promocode: ${discounted_price}"),  # Use the actual discounted price here!
            cls="price-summary"
        ),
        Div(
            H2("Promocode"),
            Form(
                Div(
                    Label("Have a promocode?", for_="promocode-input"),
                    Input(id="code", type="text", name="code", placeholder="Enter promocode"),
                    Button("Apply", type="submit", cls="apply-btn"),
                    cls="promocode-form"
                ),
                Input(type="hidden", name="booking_ref", value=booking_ref),
                Input(type="hidden", name="luggage_weight_price", value=str(luggage_weight_price)),
                *[Input(type="hidden", name=k, value=v) for k, v in form_data.items() if k != "code" and k != "booking_ref" and k != "luggage_weight_price"],
                action="/booking_summary",
                method="post"
            ),
            cls="section promocode-section"
        ),
        
        Div(
            Form(
                Button("Back", type="button", cls="back-btn", onclick="history.back()"),
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
    total_price = float(form_data.get("total_price", "0"))
    
    booking = controller.find_booking_by_reference(booking_ref)
    
    styles = Style("""
        body { 
            height: 100vh; 
            margin: 0;
            font-family: 'Arial', sans-serif;
            color: #555;
            text-align: center;
            background-image: url('/Picture/fu7.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            width: 90%;
            max-width: 450px;
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
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .card-details {
            display: flex;
            gap: 10px;
        }
        .card-details > div {
            flex: 1;
        }
        .payment-btn {
            background-color: #FFEB99;
            color: #333;
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
            margin-top: 20px;
        }
        .payment-btn:hover {
            background-color: #F9D01C;
        }
        .error-message {
            color: #e74c3c;
            font-size: 12px;
            margin-top: 5px;
            display: none;
        }
        .success-icon {
            font-size: 60px;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .booking-ref {
            background: rgba(245, 245, 245, 0.8);
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px 0;
        }
        .home-btn {
            background-color: #FFEB99;
            color: #333;
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
    """)

    validation_script = Script("""
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.querySelector('form');
            const cardNumberInput = document.querySelector('input[name="card_number"]');
            const cardNumberError = document.getElementById('card-number-error');
            const expiryInput = document.querySelector('input[name="expiry"]');
            const expiryError = document.getElementById('expiry-error');
            const cvvInput = document.querySelector('input[name="cvv"]');
            const cvvError = document.getElementById('cvv-error');
            
            // Process card number input
            cardNumberInput.addEventListener('input', function() {
                this.value = this.value.replace(/\\D/g, '').slice(0, 16);
                cardNumberError.style.display = (this.value.length > 0 && this.value.length !== 16) ? 'block' : 'none';
            });
            
            // Format expiry date (MM/YY)
            expiryInput.addEventListener('input', function() {
                this.value = this.value.replace(/\\D/g, '');
                
                if (this.value.length > 2) {
                    this.value = this.value.slice(0, 2) + '/' + this.value.slice(2, 4);
                }
                
                if (this.value.length > 5) {
                    this.value = this.value.slice(0, 5);
                }
                
                const month = parseInt(this.value.slice(0, 2), 10);
                expiryError.style.display = (this.value.length > 0 && (month < 1 || month > 12)) ? 'block' : 'none';
            });
            
            // Process CVV input
            cvvInput.addEventListener('input', function() {
                this.value = this.value.replace(/\\D/g, '').slice(0, 4);
                cvvError.style.display = (this.value.length > 0 && (this.value.length < 3 || this.value.length > 4)) ? 'block' : 'none';
            });
            
            // Form validation
            form.addEventListener('submit', function(e) {
                let isValid = true;
                
                if (cardNumberInput.value.length !== 16) {
                    cardNumberError.style.display = 'block';
                    isValid = false;
                }
                
                const expiryPattern = /^(0[1-9]|1[0-2])\\/([0-9]{2})$/;
                if (!expiryPattern.test(expiryInput.value)) {
                    expiryError.style.display = 'block';
                    isValid = false;
                }
                
                if (cvvInput.value.length < 3 || cvvInput.value.length > 4) {
                    cvvError.style.display = 'block';
                    isValid = false;
                }
                
                if (!isValid) {
                    e.preventDefault();
                }
            });
        });
    """)
    
    return Title("Payment"), styles, validation_script, Div(
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
                Input(type="text", name="card_number", placeholder="Enter 16 digits", required=True, 
                      pattern="[0-9]{16}", inputmode="numeric", maxlength="16"),
                P("Card number must be exactly 16 digits", id="card-number-error", cls="error-message"),
                cls="form-group"
            ),
            Div(
                Div(
                    Label("Expiry Date:"),
                    Input(type="text", name="expiry", placeholder="MM/YY", required=True, maxlength="5"),
                    P("Enter a valid month/year format (MM/YY)", id="expiry-error", cls="error-message"),
                ),
                Div(
                    Label("CVV:"),
                    Input(type="text", name="cvv", placeholder="XXX", required=True, 
                          pattern="[0-9]{3,4}", inputmode="numeric", maxlength="4"),
                    P("CVV must be 3-4 digits", id="cvv-error", cls="error-message"),
                ),
                cls="card-details form-group"
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

    booking = controller.find_booking_by_reference(booking_ref)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    booking.update_booking_status()
    controller.add_booking_history(booking)
    booking.payment.process_payment(card_type, card_number, cvv, exp)
    
    return Title("Payment Confirmed"), Div(
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

# Define yellow theme colors
YELLOW_PRIMARY = "#FFD700"  # Golden yellow
YELLOW_SECONDARY = "#FFEE63"  # Light yellow
YELLOW_ACCENT = "#FFC107"  # Amber yellow
YELLOW_DARK = "#F9A825"  # Dark yellow
YELLOW_TEXT = "#333333"  # Dark text for contrast
YELLOW_BACKGROUND = "#FFFEF0"  # Very light yellow background
YELLOW_BORDER = "#FFB300"  # Border color

# CSS styles for yellow theme
YELLOW_THEME_STYLES = """
<style>
    body {
        background-color: """ + YELLOW_BACKGROUND + """;
        font-family: 'Arial', sans-serif;
        color: """ + YELLOW_TEXT + """;
    }
    h1, h2, h3, h4, h5, h6 {
        color: """ + YELLOW_DARK + """;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: white;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        border-radius: 8px;
        border-top: 5px solid """ + YELLOW_PRIMARY + """;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        border: 1px solid """ + YELLOW_BORDER + """;
    }
    th {
        background-color: """ + YELLOW_PRIMARY + """;
        color: """ + YELLOW_TEXT + """;
        padding: 12px;
        font-weight: bold;
        text-align: left;
    }
    td {
        padding: 10px;
        border-bottom: 1px solid """ + YELLOW_BORDER + """;
    }
    tr:nth-child(even) {
        background-color: """ + YELLOW_BACKGROUND + """;
    }
    tr:hover {
        background-color: """ + YELLOW_SECONDARY + """;
    }
    button {
        background-color: """ + YELLOW_PRIMARY + """;
        color: """ + YELLOW_TEXT + """;
        border: none;
        padding: 8px 16px;
        margin: 5px;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    button:hover {
        background-color: """ + YELLOW_DARK + """;
    }
    button.danger {
        background-color: #ff6347;
        color: white;
    }
    button.danger:hover {
        background-color: #dc3545;
    }
    button.secondary {
        background-color: #e0e0e0;
        color: """ + YELLOW_TEXT + """;
    }
    button.secondary:hover {
        background-color: #c0c0c0;
    }
    .card {
        border: 1px solid """ + YELLOW_BORDER + """;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
        color: """ + YELLOW_DARK + """;
    }
    select, input {
        width: 100%;
        padding: 8px;
        margin-bottom: 15px;
        border: 1px solid """ + YELLOW_BORDER + """;
        border-radius: 4px;
        background-color: white;
    }
    select:focus, input:focus {
        outline: none;
        border-color: """ + YELLOW_PRIMARY + """;
        box-shadow: 0 0 5px """ + YELLOW_SECONDARY + """;
    }
    dialog {
        border: 1px solid """ + YELLOW_BORDER + """;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    dialog::backdrop {
        background-color: rgba(0,0,0,0.6);
    }
</style>
"""

@rt("/manage-booking")
def manage_booking():
    return (
        Title("Manage Bookings"), 
        Container(
            H1("Manage Bookings", style=f"color: {YELLOW_DARK}; text-align: center; margin-bottom: 30px;"),
            Button("Back to Home", 
                   hx_get="/home", 
                   hx_target="body", 
                   hx_swap="outerHTML",
                   style=f"background-color: {YELLOW_ACCENT}; color: {YELLOW_TEXT}; padding: 10px 20px; border-radius: 5px; margin-bottom: 20px;"
            ),
            get_booking_table(),
            Div(id="edit-section"),
            Dialog(id="confirm-dialog")
        )
    )

@rt("/edit-booking/{ref}", methods=["GET", "POST"])
def edit_booking_page(ref: str, flight_date: str = "", outbound_seat: str = "", return_flight_date: str = "", 
                      return_seat: str = "", confirm: bool = False):
    booking = Booking.get_booking_by_ref(ref)

    if not booking:
        return Div(H3(f"Booking with ref {ref} not found.", style=f"color: red;"))

    route = booking.flight
    is_round_trip = route.is_round_trip()
    
    # Get available seats for outbound flight
    outbound_seat_type = booking.outbound_seat.seat_type if isinstance(booking.outbound_seat, Seat) else None
    available_outbound_seats = route.outbound_seats
    
    # Filter by seat type if needed
    if outbound_seat_type:
        available_outbound_seats = [seat for seat in available_outbound_seats if outbound_seat_type in seat.seat_type]
    
    # Get available seats for return flight (if this is a round trip)
    available_return_seats = []
    if is_round_trip:
        return_seat_type = booking.return_seat.seat_type if hasattr(booking, 'return_seat') and isinstance(booking.return_seat, Seat) else None
        available_return_seats = route.return_seats
        
        # Filter by seat type if needed
        if return_seat_type:
            available_return_seats = [seat for seat in available_return_seats if return_seat_type in seat.seat_type]
    
    # Show available departure and arrival dates as pairs
    date_options = [
        Option(f"{departure} → {arrival}", value=f"{departure}|{arrival}") 
        for departure, arrival in zip(route.available_departure_dates, route.available_arrival_dates)
    ]

    # Add round-trip options if available
    round_trip_options = []
    if is_round_trip:
        round_trip_options = [
            Option(f"{departure} → {arrival}", value=f"{departure}|{arrival}") 
            for departure, arrival in zip(route.return_departure_dates, route.return_arrival_dates)
        ]

    if confirm:
        selected_outbound_seat = next((s for s in available_outbound_seats if s.seat_id == outbound_seat), None)
        
        # Only process return seat if this is a round-trip
        selected_return_seat = None
        if is_round_trip and return_seat:
            selected_return_seat = next((s for s in available_return_seats if s.seat_id == return_seat), None)

        if flight_date:
            # Split flight_date into departure and arrival
            departure, arrival = flight_date.split("|")
            booking.flight_date = departure
            booking.arrival_time = arrival

            # Handle return flight date for round-trip bookings
            if is_round_trip and return_flight_date:
                # Split return_flight_date into departure and arrival
                return_departure, return_arrival = return_flight_date.split("|")
                booking.return_flight_date = return_departure
                booking.return_arrival_time = return_arrival

            # Save the changes with separate outbound and return seats
            if booking.edit(
                flight_date=departure, 
                arrival_time=arrival, 
                outbound_seat=selected_outbound_seat,  # ✅ Corrected
                return_flight_date=booking.return_flight_date if is_round_trip else None, 
                return_arrival_time=booking.return_arrival_time if is_round_trip else None,
                return_seat=selected_return_seat  # ✅ This is correct
            ):

                # Ensure the updated table is displayed
                return get_booking_table(), Div(id="edit-section"), Script("window.location.reload();")

    # Create options for outbound seat selection
    outbound_seat_options = [
        Option(f"{seat.seat_id} ({seat.seat_type})", value=seat.seat_id) for seat in available_outbound_seats
    ]
    
    # Create options for return seat selection (if round trip)
    return_seat_options = []
    if is_round_trip:
        return_seat_options = [
            Option(f"{seat.seat_id} ({seat.seat_type})", value=seat.seat_id) for seat in available_return_seats
        ]

    # Create the form with clearly separated outbound and return fields
    form_content = [
        # Outbound Flight Section
        H4(f"Outbound Flight: {route.origin} → {route.destination}", style=f"color: {YELLOW_DARK}; margin-top: 20px; border-bottom: 1px solid {YELLOW_BORDER};"),
        Label("Departure and Arrival Date"),
        Select(
            name="flight_date",
            *date_options,
            value=f"{booking.flight_date}|{booking.arrival_time}" if booking.flight_date and booking.arrival_time else ""
        ),
        Label("Select Outbound Seat"),
        Select(
            name="outbound_seat",
            *outbound_seat_options,
            value=booking.outbound_seat.seat_id if isinstance(booking.outbound_seat, Seat) else booking.outbound_seat
        )
    ]
    
    # Add return flight options only if this is a round-trip
    if is_round_trip:
        form_content.extend([
            # Return Flight Section
            H4(f"Return Flight: {route.destination} → {route.origin}", style=f"color: {YELLOW_DARK}; margin-top: 20px; border-bottom: 1px solid {YELLOW_BORDER};"),
            Label("Return Flight Date"),
            Select(
                name="return_flight_date",
                *round_trip_options,
                value=f"{booking.return_flight_date}|{booking.return_arrival_time}" if booking.return_flight_date and booking.return_arrival_time else ""
            ),
            Label("Select Return Seat"),
            Select(
                name="return_seat",
                *return_seat_options,
                value=booking.return_seat.seat_id if hasattr(booking, 'return_seat') and isinstance(booking.return_seat, Seat) else ""
            )
        ])
    
    # Add the save button
    form_content.append(
        Button("Save Changes", type="submit",
            hx_post=f"/edit-booking/{ref}?confirm=true",
            hx_target="#manage-booking-table",
            hx_swap="outerHTML",
            style=f"background-color: {YELLOW_PRIMARY}; padding: 15px 32px; font-size: 18px; color: {YELLOW_TEXT}; border-radius: 8px; border: none; transition: background-color 0.3s ease; cursor: pointer; width: 100%; margin-top: 20px;",
            onmouseover=f"this.style.backgroundColor='{YELLOW_DARK}';",  
            onmouseout=f"this.style.backgroundColor='{YELLOW_PRIMARY}';"
        )
    )

    # Make sure to display return seat information initially
    if booking.return_seat:
        return_seat_info = f"{booking.return_seat.seat_id} ({booking.return_seat.seat_type})"
    else:
        return_seat_info = "No return seat selected"
    
    # Update the booking details section to include return seat information
    booking_details = Div(
        H3("Current Booking Details"),
        P(f"Flight: {booking.flight.flight_id} ({booking.flight.origin} → {booking.flight.destination})"),
        P(f"Outbound Date: {booking.flight_date}"),
        P(f"Outbound Seat: {booking.outbound_seat.seat_id} ({booking.outbound_seat.seat_type})"),
        # Add return flight information if it's a round trip
        P(f"Return Date: {booking.return_flight_date if booking.return_flight_date else 'N/A'}") if booking.flight.is_round_trip() else "",
        P(f"Return Seat: {return_seat_info}") if booking.flight.is_round_trip() else "",
        class_="booking-details"
    )

    return Card(
        H3(f"Edit Booking {ref}", style=f"color: {YELLOW_PRIMARY}; margin-bottom: 20px;"),
        Form(
            *form_content,
            method="post",
            style="display: flex; flex-direction: column; gap: 10px; margin-top: 20px;"
        ),
        style=f"border: 1px solid {YELLOW_BORDER}; border-radius: 8px; padding: 20px; "
    )
@rt("/cancel-booking/{ref}")
def cancel_booking(ref: str):
    booking = Booking.get_booking_by_ref(ref)  
    if booking:
        booking.cancel()  
        return get_booking_table(), Div(id="edit-section"), Script("window.location.reload();")
    return RedirectResponse("/manage-booking?error=Booking+not+found")

@rt("/confirm-cancel/{ref}")
def confirm_cancel(ref: str):
    return Dialog(
        P(f"Confirm Cancellation", style=f"font-size: 24px; color: {YELLOW_DARK}; font-weight: bold; margin-bottom: 15px;"),
        P(f"Are you sure you want to cancel booking {ref}?", style="font-size: 16px; margin-bottom: 20px;"),
        Div(
            Button("Yes, Cancel",
                   hx_post=f"/cancel-booking/{ref}",
                   hx_target="#manage-booking-table",
                   hx_swap="outerHTML",
                   cls="danger",
                   onclick="this.closest('dialog').close();",
                   style="padding: 10px 20px;"),  
            Button("Close", 
                   onclick="this.closest('dialog').close()", 
                   cls="secondary",
                   style="padding: 10px 20px;"),
            style="display: flex; justify-content: space-between; gap: 10px;"
        ),
        open=True,
        id="confirm-dialog",
        style=f"border: 2px solid {YELLOW_BORDER}; border-radius: 8px; padding: 20px;"
    )

def get_booking_table():
    if not Booking.bookings:
        return Div(
            H3("No bookings available", style=f"color: {YELLOW_DARK}; text-align: center; margin: 30px 0;")
        )
    
    # Check if any bookings have a flight/route attribute and if any are round-trips
    has_round_trips = False
    for b in Booking.bookings:
        # Check both possible attributes (flight or route)
        if (hasattr(b, 'flight') and hasattr(b.flight, 'is_round_trip') and b.flight.is_round_trip()) or \
           (hasattr(b, 'route') and hasattr(b.route, 'is_round_trip') and b.route.is_round_trip()):
            has_round_trips = True
            break
    
    # Create table headers based on whether we have any round-trips
    table_headers = [
        Th("Ref"), 
        Th("Passenger "), 
        Th("Departure → Arrival"), 
        Th("Return Flight Date") if has_round_trips else Th(""),
        Th("Route"), 
        Th("Seat"),
    ]
    
    # Add Return Seat column only if we have round-trips
    if has_round_trips:
        table_headers.append(Th("Return Seat"))
    
    # Add remaining headers
    table_headers.extend([
        Th("Price​"), 
        Th("Luggage​"), 
        Th("Payment Method​"), 
        Th("Status"),  
        Th("Actions")
    ])
    
    booking_rows = []
    for b in Booking.bookings:
        # Get the booking reference
        ref = b.booking_reference
        
        # Get passenger information directly from object
        passenger_info = ""
        if hasattr(b, 'passengers') and b.passengers:
            # Format passenger names (first passenger or all passengers)
            if len(b.passengers) == 1:
                passenger = b.passengers[0]
                passenger_info = f"{passenger.firstname} {passenger.lastname}"
            else:
                passenger_names = [f"{p.firstname} {p.lastname}" for p in b.passengers]
                passenger_info = ", ".join(passenger_names)
        
        # Create row data for each booking
        row_data = [
            Td(ref),
            Td(passenger_info),
            Td(f"{b.flight_date} → {b.arrival_time}" if hasattr(b, 'flight_date') and hasattr(b, 'arrival_time') else ""),
        ]
        
        # Add return flight data only if this booking is a round-trip
        if has_round_trips:
            if hasattr(b, 'return_flight_date') and hasattr(b, 'return_arrival_time'):
                row_data.append(Td(f"{b.return_flight_date} → {b.return_arrival_time}" if b.return_flight_date and b.return_arrival_time else ""))
            else:
                row_data.append(Td(""))
        else:
            row_data.append(Td(""))
            
        # Add route information with proper attribute access (check both flight and route)
        route_info = "Route info unavailable"
        if hasattr(b, 'flight') and hasattr(b.flight, 'origin') and hasattr(b.flight, 'destination'):
            route_info = f"{b.flight.origin} → {b.flight.destination}"
        elif hasattr(b, 'route') and hasattr(b.route, 'origin') and hasattr(b.route, 'destination'):
            route_info = f"{b.route.origin} → {b.route.destination}"
        row_data.append(Td(route_info))
        
        # Add outbound seat information (check both outbound_seat and seat)
        seat_info = "Seat info unavailable"
        if hasattr(b, 'outbound_seat'):
            seat_info = b.outbound_seat.seat_id if hasattr(b.outbound_seat, 'seat_id') else str(b.outbound_seat)
        elif hasattr(b, 'seat'):
            seat_info = b.seat.seat_id if hasattr(b.seat, 'seat_id') else str(b.seat)
        row_data.append(Td(seat_info))
        
        # Add return seat only if this is a round-trip
        if has_round_trips:
            is_round_trip = False
            if hasattr(b, 'flight') and hasattr(b.flight, 'is_round_trip') and b.flight.is_round_trip():
                is_round_trip = True
            elif hasattr(b, 'route') and hasattr(b.route, 'is_round_trip') and b.route.is_round_trip():
                is_round_trip = True
                
            if is_round_trip:
                if hasattr(b, 'return_seat'):
                    return_seat_info = b.return_seat.seat_id if hasattr(b.return_seat, 'seat_id') else str(b.return_seat)
                    row_data.append(Td(return_seat_info))
                else:
                    row_data.append(Td("Same as outbound"))
            else:
                row_data.append(Td(""))  # Empty cell for one-way bookings
        
        # Get price information directly from object
        price_info = ""
        if hasattr(b, 'payment') and hasattr(b.payment, 'price'):
            price_info = f"{b.payment.price} THB"
        elif hasattr(b, 'price'):
            price_info = f"{b.price} THB"
        
        # Get luggage information directly from object
        luggage_info = ""
        if hasattr(b, 'luggage_weight'):
            luggage_info = f"{b.luggage_weight} kg"
        elif hasattr(b, 'luggage'):
            luggage_info = f"{b.luggage} kg"
        
        # Get payment method information directly from object
        payment_method_info = ""
        if hasattr(b, 'payment') and hasattr(b.payment, 'method'):
            if hasattr(b.payment.method, 'method_id'):
                payment_method_info = b.payment.method.method_id
        elif hasattr(b, 'payment_method'):
            payment_method_info = b.payment_method
            
        # Add remaining fields
        row_data.extend([
            Td(price_info),
            Td(luggage_info),
            Td(payment_method_info),
            Td(b.status if hasattr(b, 'status') else "", 
               style="font-weight: bold; color: " + 
               ("#4CAF50" if hasattr(b, 'status') and b.status == "Confirmed" else 
                "#F44336" if hasattr(b, 'status') and b.status == "Cancelled" else 
                YELLOW_DARK)),
            Td(
                Button("Edit", 
                       hx_get=f"/edit-booking/{ref}", 
                       hx_target="#edit-section", 
                       hx_swap="outerHTML",
                       style=f"background-color: {YELLOW_PRIMARY}; color: {YELLOW_TEXT};"
                      ) if hasattr(b, 'status') and b.status != "Cancelled" else "",
                Button("Cancel", 
                       cls="danger", 
                       hx_get=f"/confirm-cancel/{ref}", 
                       hx_target="#confirm-dialog", 
                       hx_swap="outerHTML"
                      ) if hasattr(b, 'status') and b.status != "Cancelled" else ""
            ) 
        ])
        
        booking_rows.append(Tr(*row_data))

    return Div(
        Table(
            Thead(Tr(*table_headers)),
            Tbody(*booking_rows),
            id="manage-booking-table",
            style=f"border: 1px solid {YELLOW_BORDER}; border-radius: 4px; overflow: hidden;"
        ),
        style="overflow-x: auto;"
    )

@rt("/promocode")
def get():
    """หน้าแสดงโปรโมชั่น & แต้มของผู้ใช้"""
    return Title("Promotion Codes"), Container(
        Button("Back to Home", 
               hx_get="/home", 
               hx_target="body", 
               hx_swap="outerHTML",
               style="background-color: #FFFF33; color: black; padding: 10px 20px; border-radius: 5px; margin-bottom: 20px; border: none; cursor: pointer; font-weight: bold;"),
        H1("Promotion Codes", cls="text-center mb-4"),
        Div(get_user_info(), id="user-info", cls="mb-4 p-3 border rounded"),
        H2("Available Promotions", cls="mb-3"),
        get_promotion_table(),
        Dialog(id="confirm-dialog", cls="p-4 rounded shadow-lg"),
        get_page_styles(),
        Script(""" 
            function closeDialog() { 
                document.getElementById('confirm-dialog').close(); 
            }
            
            function showToast(message, isSuccess = true) {
                const toast = document.createElement('div');
                toast.className = isSuccess ? 'toast success' : 'toast error';
                toast.textContent = message;
                document.body.appendChild(toast);
                
                setTimeout(() => {
                    toast.classList.add('show');
                }, 100);
                
                setTimeout(() => {
                    toast.classList.remove('show');
                    setTimeout(() => document.body.removeChild(toast), 300);
                }, 3000);
            }
        """)
    )


def get_page_styles():
    return Style("""
        .success { background-color: #4CAF50; color: white; }
        .error { background-color: #f44336; color: white; }
        .secondary { background-color: #363636; }
        
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 4px;
            transform: translateY(100px);
            opacity: 0;
            transition: transform 0.3s, opacity 0.3s;
            z-index: 1000;
        }
        
        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #FFFF33;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        button {
            padding: 8px 16px;
            margin: 5px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        button:hover {
            opacity: 0.8;
        }
        
        .code-badge {
            display: inline-block;
            padding: 4px 8px;
            margin: 3px;
            background-color: #FFFF33;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        .expired {
            text-decoration: line-through;
            opacity: 0.7;
        }
    """)

def get_user_info():
    """แสดงแต้มและโค้ดที่แลกแล้วของผู้ใช้"""
    return Div(
        Div(
            Span("Your Points: ", style="font-size: 16px;"),
            Span(f"{user_account.points}", style="font-size: 24px; font-weight: bold; color: #4CAF50;", id="user-points")
        ),
        H3("Your Redeemed Codes", cls="mt-3"),
        get_owned_codes_list(),
        id="update-section"
    )

user = controller.get_logged_in_user()
user_account = user.userdetail

def get_owned_codes_list():
    """แสดงโค้ดที่แลกแล้วของผู้ใช้"""
    if not user_account.promocode_list:  # ✅ ใช้ instance ของ user_account
        return P("You haven't redeemed any codes yet.", style="color: #777;")
    
    owned_code_list = []
    for code in user_account.promocode_list:  # ✅ ใช้ instance แทน property
        promo = next((p for p in promotion_codes if p.code == code), None)
        if promo:
            is_expired = promo.is_expired()
            cls = "code-badge" + (" expired" if is_expired else "")
            expired_text = " (EXPIRED)" if is_expired else ""
            owned_code_list.append(
                Div(
                    f"{code} : -{promo.discount_percent}% {expired_text}",
                    cls=cls
                )
            )
    
    return Div(*owned_code_list, id="owned-codes", cls="mt-2")


def get_promotion_table():
    """สร้างตารางแสดงโค้ดโปรโมชั่น"""
    promo_rows = []
    
    for promo in promotion_codes:
        # Check if code is already redeemed
        is_redeemed = promo.code in user_account.promocode_list
        is_expired = promo.is_expired()
        has_enough_points = user_account.points >= promo.points
        
        button_attrs = {}
        
        if is_redeemed:
            button_text = "Redeemed"
            button_cls = "secondary"
            button_disabled = True
        elif is_expired:
            button_text = "Expired"
            button_cls = "secondary"
            button_disabled = True
        elif not has_enough_points:
            button_text = "Not Enough Points"
            button_cls = "secondary"
            button_disabled = True
        else:
            button_text = "Redeem"
            button_cls = "success"
            button_disabled = False
            button_attrs = {
                "hx_get": f"/confirm-redeem/{promo.code}",
                "hx_target": "#confirm-dialog",
                "hx_swap": "outerHTML"
            }
        
        row_cls = "expired" if is_expired else ""
        
        promo_rows.append(
            Tr(
                Td(promo.description),
                Td(f"{promo.points} pts"),
                Td(f"{promo.discount_percent}%"),
                Td(promo.expiration_date),
                Td(
                    Button(
                        button_text,
                        cls=button_cls,
                        disabled=button_disabled,
                        **button_attrs
                    )
                ),
                cls=row_cls
            )
        )

    return Table(
        Thead(Tr(Th("Description"), Th("Points Required"), Th("Discount %"), Th("Expiration Date"), Th("Action"))),
        Tbody(*promo_rows),
        id="promo-table",
        cls="mt-4"
    )

@rt("/confirm-redeem/{code}")
def confirm_redeem(code: str):
    """แสดงป๊อปอัปยืนยันก่อนแลก"""
    promo = next((p for p in promotion_codes if p.code == code), None)

    if not promo:
        return Dialog(
            P("Error: Promotion code not found"),
            Button("Close", onclick="this.closest('dialog').close()"),
            open=True,
            id="confirm-dialog"
        )

    # เช็คว่าแต้มผู้ใช้เพียงพอหรือไม่
    if not promo.can_redeem(user_account.points):
        # ถ้าแต้มไม่เพียงพอหรือโค้ดหมดอายุ
        if promo.is_expired():
            message = f"This promotion code has expired on {promo.expiration_date}."
        else:
            message = f"You do not have enough points. You need {promo.points} points, but you have {user_account.points}."
            
        return Dialog(
            H3("Cannot Redeem", style="color: #f44336; margin-top: 0;"),
            P(message),
            Button("Close", onclick="this.closest('dialog').close()", cls="secondary"),
            open=True,
            id="confirm-dialog"
        )

    return Dialog(
        Div(
            P(f"Description: {promo.description}"),
            P(f"Discount: ", Span(f"{promo.discount_percent}%", style="color: #4CAF50; font-weight: bold;")),
            P(f"Points Required: ", Span(f"{promo.points}", style="font-weight: bold;")),
            P(f"Your Current Points: ", Span(f"{user_account.points}", style="font-weight: bold;")),
            P(f"Remaining Points After Redemption: ", 
              Span(f"{user_account.points - promo.points}", style="color: #1976D2; font-weight: bold;")),
            cls="mt-3 mb-3"
        ),
        P("Are you sure you want to redeem this promocode?"),
        Div(
            Button("Yes, Redeem", 
                  hx_post=f"/redeem/{promo.code}",  
                  hx_target="#update-section",  
                  hx_swap="outerHTML",
                  hx_on="htmx:afterRequest: closeDialog();",
                   cls="success"),
            Button("Cancel", onclick="this.closest('dialog').close()", cls="secondary"),
            style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;"
        ),
        open=True,
        id="confirm-dialog",
        style="max-width: 500px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
    )

@rt("/redeem/{code}")
def redeem(code: str):
    """ดำเนินการแลกโค้ด"""
    promo = next((p for p in promotion_codes if p.code == code), None)

    if not promo:
        return get_user_info(), Script("showToast('Promotion code not found', false);")

    # Create a new Promocode instance to avoid modifying the original
    promo_instance = Promocode(
        promo.code, 
        promo.points, 
        promo.discount_percent, 
        promo.expiration_date,
        promo.description
    )

    if user_account.redeem_promocode(promo_instance):
        # Return updated user info section และเพิ่ม Script แสดง toast ว่าสำเร็จ
        return get_user_info(), Script("""
            showToast('Promocode redeemed successfully!', true);
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        """)
    else:
        return get_user_info(), Script("showToast('Failed to redeem promocode', false);")


serve()

