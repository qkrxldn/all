from fasthtml.common import *

app, rt = fast_app()

YELLOW = '#FFC107'
WHITE = '#FFFFFF'
DARK_GRAY = '#333333'
LIGHT_GRAY = '#F5F5F5'

@rt('/')
def get():
    return Div(
        H1("เที่ยวบิน : AIR22", style="color: "+DARK_GRAY),
        H2("ที่นั่ง : A01", style="color: "+DARK_GRAY),
        H3("ข้อมูลผู้โดยสาร", style="color: "+DARK_GRAY),

        Form(
            Grid(
                Label("คำนำหน้า",
                    Select(
                        Option("นาย", value="นาย"),
                        Option("นาง", value="นาง"),
                        Option("นางสาว", value="นางสาว"),
                        id="nametitle"
                    )
                ),
                Label("ชื่อ", Input(type="text", id="name", required=True, placeholder="กรอกชื่อ")),
                Label("นามสกุล", Input(type="text", id="surname", required=True, placeholder="กรอกนามสกุล")),
            ),
            Button("ถัดไป", style=f"background-color: {YELLOW}; color: {DARK_GRAY}; border: none; padding: 10px 20px; border-radius: 5px;"),
            method="post",
            action="/pay",
            style="margin-top: 20px;"
        ),
        style=f"""
            background-color: {WHITE};
            padding: 20px;
            max-width: 600px;
            margin: 50px auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        """
    )

@rt('/pay')
def pay():
    return Div(
        H1("เที่ยวบิน : AIR22", style="color: "+DARK_GRAY),
        H2("ที่นั่ง : A01", style="color: "+DARK_GRAY),
        H3("วิธีชำระเงิน", style="color: "+DARK_GRAY),

        Div(
            Grid(
                Form(
                    Button("Online Banking", style=f"background-color: {YELLOW}; color: {DARK_GRAY}; border: none; padding: 10px 20px; border-radius: 5px;"),
                    method="post",
                    action="/onlineBanking"
                ),
                Form(
                    Button("Debit Card", style=f"background-color: {YELLOW}; color: {DARK_GRAY}; border: none; padding: 10px 20px; border-radius: 5px;"),
                    method="post",
                    action="/DebitCard"
                ),
                Form(
                    Button("Credit Card", style=f"background-color: {YELLOW}; color: {DARK_GRAY}; border: none; padding: 10px 20px; border-radius: 5px;"),
                    method="post",
                    action="/CreditCard"
                ),
                style="gap: 20px;"
            ),
            style="margin-top: 20px;"
        ),
        style=f"""
            background-color: {WHITE};
            padding: 20px;
            max-width: 600px;
            margin: 50px auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        """
    )

@rt('/success')
def success():
    return Div(
        H1("จองตั๋วสำเร็จ", style="color: "+DARK_GRAY),
        P("ขอบคุณที่ใช้บริการ", style="color: "+DARK_GRAY),
        style=f"""
            background-color: {YELLOW};
            padding: 20px;
            max-width: 600px;
            margin: 50px auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        """
    )

serve()
