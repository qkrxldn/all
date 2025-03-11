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
        
        # Simplify weight calculation
        for i in range(1, person_count + 1):
            try:
                weight = float(form_data.get(f"weight_{i}", 0))
                total_weight += weight
            except ValueError:
                pass

        booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
        if booking:
            booking.add_luggage(Luggage(total_weight))
            luggage_weight_price = booking.luggage.calculate_price()
        else:
            luggage_weight_price = 0

        seat_info = [{"id": seat_id} for seat_id in seat_ids]
        
    # Simplified validation script
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

    # Create passenger forms
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
    
    booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    flight = controller.get_flight_by_id(booking.flight.flight_id)
    if not flight:
        return Title("Error"), H1("Flight not found")
    
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
        
        seat_ids = form_data.getlist("seat_ids") if hasattr(form_data, "getlist") else form_data.get("seat_ids", [])
        if not isinstance(seat_ids, list):
            seat_ids = [seat_ids]
            
        booking.passenger_seats = {}
        for i, passenger in enumerate(booking.passengers):
            if i < len(seat_ids):
                booking.passenger_seats[passenger.id] = seat_ids[i]
                booking.add_seat(seat_ids[i])
    
    total_seat_price = 0
    passenger_items = []
    
    for passenger in booking.passengers:
        seat_id = booking.passenger_seats.get(passenger.id, 'Not assigned')
        seat_class = "Economy"
        seat_price = 0

        if seat_id != 'Not assigned':
            # Look for the seat in the flight's outbound_seats first
            seat = next((s for s in flight.outbound_seats if s.seat_id == seat_id), None)
            
            # If not found in outbound_seats, try the plane's seats
            if not seat:
                seat = next((s for s in flight.plane.seats if s.seat_id == seat_id), None)
            
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
    
    luggage_weight_price = float(form_data.get("luggage_weight_price", "0"))
    total_price = total_seat_price + luggage_weight_price
    
    booking.create_payment(total_price)

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
    
    booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    # Simplified validation script
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

    booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    # Process payment
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
