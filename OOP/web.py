from fasthtml.common import *

app, rt = fast_app()

YELLOW_LIGHT = '#FFECB3'
YELLOW = '#FFC107'
YELLOW_DARK = '#FFA000'
WHITE = '#FFFFFF'
DARK_GRAY = '#333333'

def themed_card(*children):
    return Container(
        Card(
            *children,
            style=f"""
                background-color: {WHITE};
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                margin-top: 15px;
                margin-bottom: 10px;
            """
        ),
        style="max-width: 1050px; margin: 0 auto; padding: 10px;"
    )

GRADIENT_STYLE = f"""
    background: {YELLOW};
    min-height: 100vh;
    padding-top: 50px;
    padding-bottom: 20px;
"""

@rt('/')
def get():
    return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX", style=f"color: {DARK_GRAY}; text-align: center;"),
            H2("ที่นั่ง : XXXX", style=f"color: {YELLOW}; text-align: center; margin-bottom: 20px;"),
            
            Form(
                Grid(
                    Label("คำนำหน้า",
                        Select(
                            Option("นาย", value="นาย"),
                            Option("นาง", value="นาง"),
                            Option("นางสาว", value="นางสาว"),
                            id="nametitle"
                        ), style=f"color: {DARK_GRAY}"
                    ),
                    Label("ชื่อ", Input(type="text", id="name", required=True, placeholder="กรอกชื่อ"), style=f"color: {DARK_GRAY}"),
                    Label("นามสกุล", Input(type="text", id="surname", required=True, placeholder="กรอกนามสกุล"), style=f"color: {DARK_GRAY}"),
                ),
                Grid(
                    Label("Email", Input(type="email", id="email", required=True, placeholder="กรอก E-mail"), style=f"color: {DARK_GRAY}"),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phoone_number", required=True, placeholder="กรอกเบอร์โทรศัพท์"), style=f"color: {DARK_GRAY}"),
                ),
                Button("ถัดไป", style=f"background-color: {YELLOW_DARK}; color: {WHITE}; padding: 12px 20px; border: none; border-radius: 8px; width: 100%; margin-top: 20px;"),
                method="post",
                action="/pay"
            )
        ),
        style=GRADIENT_STYLE
    )
def get 

@rt('/pay')
def pay():
    return Div(
        themed_card(
            H1("เลือกช่องทางชำระเงิน", style=f"color: {DARK_GRAY}; text-align: center;"),

            Div(
            Button("📱 Online Banking", 
                   style=f"background-color: {YELLOW_DARK}; color: {WHITE}; padding: 12px 20px; border: none; border-radius: 8px; width: 100%; margin-top: 10px;", 
                   hx_get="/onlineBanking", hx_target="#content", hx_swap="innerHTML"),

            Button("🏦 Debit Card", 
                   style=f"background-color: {YELLOW_DARK}; color: {WHITE}; padding: 12px 20px; border: none; border-radius: 8px; width: 100%; margin-top: 10px;", 
                   hx_get="/DebitCard", hx_target="#content", hx_swap="innerHTML"),

            Button("💳 Credit Card", 
                   style=f"background-color: {YELLOW_DARK}; color: {WHITE}; padding: 12px 20px; border: none; border-radius: 8px; width: 100%; margin-top: 10px;", 
                   hx_get="/CreditCard", hx_target="#content", hx_swap="innerHTML")
        )
        ),
        Div(id="content", style="margin-top: 1px;"),
        style=GRADIENT_STYLE
    )

@rt('/onlineBanking')
def online_banking():
    return Div(
        themed_card(
            H1("ชำระเงินผ่าน Online Banking", style=f"color: {DARK_GRAY}; text-align: center;"),
            Img(src="https://media.discordapp.net/attachments/1124269839448559657/1344655574909845515/123.png?ex=67c25c57&is=67c10ad7&hm=0c2a375585afff666b9b3acbaa451520cd7c4a8d8fb8a3138a0854837a522ea3&=&format=webp&quality=lossless&width=921&height=856", style="width: 450px; margin: 20px auto; display: block;"),
            Form(
                Button("ชำระเงิน", style=f"background-color: {YELLOW_DARK}; color: {WHITE}; padding: 12px 20px; border: none; border-radius: 8px; width: 100%;"),
                method="post",
                action="/success"
            )
        ),
        style=GRADIENT_STYLE
    )

@rt('/DebitCard')
def debit_card():
    return Div(
        themed_card(
            H1("ชำระด้วยบัตรเดบิต", style=f"color: {DARK_GRAY}; text-align: center;"),

            Form(
                Label("Card Number", Input(type="text", id="debit_card_number", required=True, placeholder="Enter card number"), style=f"color: {DARK_GRAY}"),
                Label("CVV", Input(type="password", id="debit_cvv", required=True, placeholder="Enter CVV"), style=f"color: {DARK_GRAY}"),
                Label("EXP (MM/YY)", Input(type="text", id="debit_exp_date", required=True, placeholder="MM/YY"), style=f"color: {DARK_GRAY}"),
                
                Button("ชำระเงิน", style=f"background-color: {YELLOW_DARK}; color: {WHITE}; padding: 12px 20px; border: none; border-radius: 8px; width: 100%;"),
                method="post",
                action="/success"
            )
        ),
        style=GRADIENT_STYLE
    )

@rt('/CreditCard')
def credit_card():
    return Div(
        themed_card(
            H1("ชำระด้วยบัตรเครดิต", style=f"color: {DARK_GRAY}; text-align: center;"),

            Form(
                Label("Card Number", Input(type="text", id="debit_card_number", required=True, placeholder="Enter card number"), style=f"color: {DARK_GRAY}"),
                Label("CVV", Input(type="password", id="debit_cvv", required=True, placeholder="Enter CVV"), style=f"color: {DARK_GRAY}"),
                Label("EXP (MM/YY)", Input(type="text", id="debit_exp_date", required=True, placeholder="MM/YY"), style=f"color: {DARK_GRAY}"),
                
                Button("ชำระเงิน", style=f"background-color: {YELLOW_DARK}; color: {WHITE}; padding: 12px 20px; border: none; border-radius: 8px; width: 100%;"),
                method="post",
                action="/success"
            )
        ),
        style=GRADIENT_STYLE
    )

@rt('/success')
def success():
    return Div(
        themed_card(
            H1("🎉 จองตั๋วสำเร็จ!", style=f"color: {YELLOW_DARK}; text-align: center;"),
            P("ขอบคุณที่ใช้บริการสายการบินของเรา", style=f"color: {DARK_GRAY}; text-align: center;")
        ),
        style=GRADIENT_STYLE
    )

serve()
