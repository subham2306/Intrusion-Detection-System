import smtplib
from email.mime.text import MIMEText

ADMIN_EMAIL = "subhamsahoo2306@gmail.com"
APP_PASSWORD = "zavknrclesowqofg"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

msg = MIMEText("🚨 Test IDS Alert 🚨\n\nThis is a test email.")
msg["Subject"] = "IDS Test Alert"
msg["From"] = ADMIN_EMAIL
msg["To"] = ADMIN_EMAIL

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(ADMIN_EMAIL, APP_PASSWORD)
        server.sendmail(ADMIN_EMAIL, ADMIN_EMAIL, msg.as_string())
    print("✅ Test email sent successfully!")
except Exception as e:
    print(f"[ERROR] Failed to send email: {e}")

