import os, smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from handlers.DataBaseCoordinator import db_query, read_json

def get_username_by_id(id):
    
    # Construct the SQL query to retrieve the username
    # Secure Query
    query = "SELECT username FROM users WHERE user_id = ?;"
    result = db_query(query, (id))

    # Check if the username was found
    if result:

        # If it was, return the username
        return result[0][0]

    else:

        # If it wasn't return None
        return None


def sql_to_pdf(user_id, output_path):
    
    # Product ID - 0
    # Product Quantity - 1
    # Product Name - 2
    # Quantity - 3
    # Price - 4
    # Total - 5

    # Query to join carts and products tables
    query = """
        SELECT carts.product_id, carts.quantity, products.product_name, products.price, carts.quantity * products.price AS total
        FROM carts
        JOIN products ON carts.product_id = products.product_id
        WHERE carts.user_id = ?
    """

    result = db_query(query, (user_id))

    username = get_username_by_id(user_id)
    lst = []
    for element in result:
        product_id = element[0]
        quantity = element[1]
        product_name = element[2]
        price = element[4]
        price = str(round(element[4], 2)) + " €"
        lst.append((product_id, product_name, quantity, price))

    lst = sorted(lst, key=lambda x: x[0])
    result = lst
    result.insert(0, ("Product ID", "Product Name", "Quantity", "Price"))

    
    # Read the CSV file and convert it to a list of rows
    rows = result

    # Define the table style
    style = TableStyle([
        # Header row style
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(77/255, 155/255, 75/255)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 14),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        # Data rows style
        ("BACKGROUND", (0, 1), (-1, -1), colors.Color(102/255, 102/255, 102/255)),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.whitesmoke),
        ("ALIGN", (0, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ])

    # Create the table object
    table = Table(rows)

    # Apply the table style
    table.setStyle(style)

    # Create the PDF document and add the table to it
    doc = SimpleDocTemplate(output_path, pagesize=letter, encoding="utf-8")


    # Create the username and ID paragraph
    username_style = ParagraphStyle(
        name='UsernameStyle',
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.black,
        alignment=TA_CENTER
    )
    username_text = f"{username.capitalize()} ({id})"
    username_para = Paragraph(username_text, username_style)

    # Create the date and time paragraph
    datetime_style = ParagraphStyle(
        name='DateTimeStyle',
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.black,
        alignment=TA_CENTER
    )
    now = datetime.now()
    datetime_text = f"Date: {now.strftime('%d-%m-%Y %H:%M:%S')}"
    datetime_para = Paragraph(datetime_text, datetime_style)

    # Add the spacer, username/ID paragraph, table, and datetime paragraph to the PDF document
    elements = [
        username_para,
        Spacer(width=0, height=0.2*inch),
        table,
        Spacer(width=0, height=0.2*inch),
        datetime_para
    ]

    doc.build(elements)
    return True



def send_email_with_attachment(to, subject, body, attachment_path):
    return True
    # Read Email credentials file
    credentials = read_json("/credentials/EmailCredentials.json")

    # Create a MIMEText object to represent the email body
    msg = MIMEMultipart()
    msg['From'] = credentials["email"]
    msg['To'] = to
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'html'))

    # Attach the PDF file as an attachment
    with open(attachment_path, "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")

    pdf_attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
    msg.attach(pdf_attachment)

    # Connect to the SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your email provider's SMTP server

    try:
        # Login to your email account
        server.login(credentials["email"], credentials["password"])

        # Send the email with attachment
        server.sendmail(credentials["email"], to, msg.as_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()

    # Return True to indicate the email was sent successfully
    return True




def send_email(to, subject, body):

    # Read Email credentials file
    credentials = read_json("/credentials/EmailCredentials.json")

    # Create a MIMEText object to represent the email body
    msg = MIMEMultipart()
    msg['From'] = credentials["email"]
    msg['To'] = to
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your email provider's SMTP server

    try:
        # Login to your email account
        server.login(credentials["email"], credentials["password"])

        # Send the email
        server.sendmail(credentials["email"], to, msg.as_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()

    # Return True to indicate the email was sent successfully
    return True