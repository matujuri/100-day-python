import smtplib

my_email = "b38860114@gmail.com"
password = "APP_PASSWORD"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email, 
        to_addrs="xiaobaka59@gmail.com", 
        msg="subject:Hello\n\nThis is the body of the email."
    )
    
