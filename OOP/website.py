from fasthtml.common import *


app, rt = fast_app()

def themed_card(*children):
    return Container(
        Card(
            *children,
        ),
        style="max-width: 1050px; margin: 0 auto; padding: 10px;"
    )

passenger_num = 1

@rt('/')
def get():
    if passenger_num == 1:
        return Redirect('/passenger_one')
    elif passenger_num == 2:
        return Redirect('/passenger_two')
    elif passenger_num == 3:
        return Redirect('/passenger_three')
    elif passenger_num == 4:
        return Redirect('/passenger_four')
    elif passenger_num == 5:
        return Redirect('/passenger_five')

@rt('/passenger_one')
def passenger1():
    return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            
            Form(
                H4("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle1"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday1"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday1"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1"
                        )
                    ),
                ),
                H6("ข้อมูลติดต่อ"),
                Grid(
                    Label("Email", Input(type="email", id="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                ),
                Button("ถัดไป", type="submit"),
                method="post",
                action="/passenger_details_submit1"
            )
        ),
    )

@rt('/passenger_details_submit1')
def post(nametitle1 : str, name1: str, surname1: str, email1: str, phone_number1: str):
    return Redirect('/pay')

@rt('/passenger_two')
def passenger2():
    return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            
            Form(
                H4("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle1"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday1"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday1"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1"
                        )
                    ),
                ),
                H6("ข้อมูลติดต่อ"),
                Grid(
                    Label("Email", Input(type="email", id="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                )
            )
            ,
            Form(
                H4("ข้อมูลผู้โดยสารที่ 2"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle2"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name2", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname2", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday2"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday2"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2"
                        )
                    ),
                ),
                Button("ถัดไป", type="submit"),
                method="post",
                action="/passenger_details_submit2"
            )
        ),
    )

@rt('/passenger_details_submit2')
def post(nametitle1 : str, name1: str, surname1: str, day_bday1:str, month_day1: str, year_bday1: str, email1: str, phone_number1: str, 
    nametitle2 : str, name2: str, surname2: str, day_bday2:str, month_day2: str, year_bday2: str):
    return Redirect('/pay')

@rt('/passenger_three')
def passenger3():
    return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            
            Form(
                H4("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle1"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday1"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday1"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1"
                        )
                    ),
                ),
                H6("ข้อมูลติดต่อ"),
                Grid(
                    Label("Email", Input(type="email", id="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                )
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 2"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle2"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name2", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname2", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)],
                        id="day_bday2"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday2"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2"
                        )
                    ),
                ),
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 3"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle3"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name3", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname3", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday3"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday3"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday3"
                        )
                    ),
                ),
                Button("ถัดไป", type="submit"),
                method="post",
                action="/passenger_details_submit3"
            )
        ),
    )

@rt('/passenger_details_submit3')
def post(nametitle1 : str, name1: str, surname1: str, day_bday1:str, month_day1: str, year_bday1: str, email1: str, phone_number1: str, 
    nametitle2 : str, name2: str, surname2: str, day_bday2:str, month_day2: str, year_bday2: str,
    nametitle3 : str, name3: str, surname3: str, day_bday3:str, month_day3: str, year_bday3: str):
    return Redirect('/pay')

@rt('/passenger_four')
def passenger4():
    return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            
            Form(
                H4("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle1"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday1"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday1"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1"
                        )
                    ),
                ),
                H6("ข้อมูลติดต่อ"),
                Grid(
                    Label("Email", Input(type="email", id="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                )
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 2"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle2"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name2", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname2", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday2"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday2"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2"
                        )
                    ),
                ),
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 3"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle3"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name3", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname3", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday3"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday3"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday3"
                        )
                    ),
                ),
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 4"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle4"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name4", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname4", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday4"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday4"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday4"
                        )
                    ),
                ),
                Button("ถัดไป", type="submit"),
                method="post",
                action="/passenger_details_submit4"
            )
        ),
    )

@rt('/passenger_details_submit4')
def post(nametitle1 : str, name1: str, surname1: str, day_bday1:str, month_day1: str, year_bday1: str, email1: str, phone_number1: str, 
    nametitle2 : str, name2: str, surname2: str, day_bday2:str, month_day2: str, year_bday2: str,
    nametitle3 : str, name3: str, surname3: str, day_bday3:str, month_day3: str, year_bday3: str,
    nametitle4 : str, name4: str, surname4: str, day_bday4:str, month_day4: str, year_bday4: str):
    return Redirect('/pay')

@rt('/passenger_Five')
def passenger5():
    return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            
            Form(
                H4("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle1"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday1"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday1"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1"
                        )
                    ),
                ),
                H6("ข้อมูลติดต่อ"),
                Grid(
                    Label("Email", Input(type="email", id="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                )
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 2"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle2"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name2", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname2", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday2"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday2"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2"
                        )
                    ),
                ),
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 3"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle3"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name3", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname3", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday3"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday3"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday3"
                        )
                    ),
                ),
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 4"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle4"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name4", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname4", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday4"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday4"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday4"
                        )
                    ),
                ),
            ),
            Form(
                H4("ข้อมูลผู้โดยสารที่ 5"),
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle4"
                        )
                    ),
                    Label("ชื่อ", Input(type="text", id="name5", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname5", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                        Select(
                        *[Option(i, value=i) for i in range(1, 32)], id="day_bday5"
                        )
                    ),
                    Label("เดือน",
                        Select(
                        *[Option(i, value=i) for i in range(1, 13)], id="month_bday5"
                        )
                    ),
                    Label("ปี",
                        Select(
                        *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday5"
                        )
                    ),
                ),
                Button("ถัดไป", type="submit"),
                method="post",
                action="/passenger_details_submit5"
            )
        ),
    )

@rt('/passenger_details_submit5')
def post(nametitle1 : str, name1: str, surname1: str, day_bday1:str, month_day1: str, year_bday1: str, email1: str, phone_number1: str, 
    nametitle2 : str, name2: str, surname2: str, day_bday2:str, month_day2: str, year_bday2: str,
    nametitle3 : str, name3: str, surname3: str, day_bday3:str, month_day3: str, year_bday3: str,
    nametitle4 : str, name4: str, surname4: str, day_bday4:str, month_day4: str, year_bday4: str,
    nametitle5 : str, name5: str, surname5: str, day_bday5:str, month_day5: str, year_bday5: str):
    return Redirect('/pay')

@rt('/pay')
def pay():
    return Div(
        themed_card(
            H1("เลือกช่องทางชำระเงิน"),
            Div(
                Button("📱 Online Banking", 
                       hx_get="/pay/onlineBanking", hx_target="#content", hx_swap="innerHTML"),
                Button("🏦 Debit Card", 
                       hx_get="/pay/DebitCard", hx_target="#content", hx_swap="innerHTML"),
                Button("💳 Credit Card", 
                       hx_get="/pay/CreditCard", hx_target="#content", hx_swap="innerHTML")
            )
        ),
        Div(id="content"),
    )

@rt('/pay/onlineBanking')
def online_banking():
    paymentmethod = "Online Banking"
    return Div(
        themed_card(
            H1("ชำระเงินผ่าน Online Banking"),
            P(f"วิธีการชำระเงิน: {paymentmethod}"),
            Img(src="https://example.com/online_banking_image.png"),
            Form(
                Button("ชำระเงิน"),
                method="post",
                action="/booking_confirm"
            )
        ),
    )

@rt('/pay/DebitCard')
def debit_card():
    paymentmethod = "Debit Card"
    return Div(
        themed_card(
            H1("ชำระด้วยบัตรเดบิต"),
            P(f"วิธีการชำระเงิน: {paymentmethod}"),
            Form(
                Label("Card Number", Input(type="text", id="debit_card_number", required=True, placeholder="Enter card number")),
                Label("CVV", Input(type="password", id="debit_cvv", required=True, placeholder="Enter CVV")),
                Label("EXP (MM/YY)", Input(type="text", id="debit_exp_date", required=True, placeholder="MM/YY")),
                Button("ชำระเงิน"),
                method="post",
                action="/booking_confirm"
            )
        ),
    )

@rt('/pay/CreditCard')
def credit_card():
    paymentmethod = "Credit Card" 
    return Div(
        themed_card(
            H1("ชำระด้วยบัตรเครดิต"),
            P(f"วิธีการชำระเงิน: {paymentmethod}"),
            Form(
                Label("Card Number", Input(type="text", id="credit_card_number", required=True, placeholder="Enter card number")),
                Label("CVV", Input(type="password", id="credit_cvv", required=True, placeholder="Enter CVV")),
                Label("EXP (MM/YY)", Input(type="text", id="credit_exp_date", required=True, placeholder="MM/YY")),
                Button("ชำระเงิน"),
                method="post",
                action="/booking_confirm"
            )
        ),
    )

@rt('/booking_confirm')
def booking_confirm():

    return Redirect('/success')

@rt('/success')
def success():
    return Div(
        themed_card(
            H1("🎉 จองตั๋วสำเร็จ!"),
            P("ขอบคุณที่ใช้บริการสายการบินของเรา")
        ),
    )

serve()