import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(destinatario, codigo):
    remitente = 'gopark3139@gmail.com'
    contraseña = 'pcyqcrzhqimssxlu'
    asunto = 'Recuperación de contraseña - GoPark'
    mensaje = (
        f"Hola!\n\n"
        f"Tu código de recuperación es:\n\n"
        f"{codigo}\n\n"
        f"Este código expirará en 10 minutos.\n\n"
        f"Equipo GoPark 🚗"
    )

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.sendmail(remitente, destinatario, msg.as_string())
        servidor.quit()
        print("📤 Correo enviado correctamente.")
    except Exception as e:
        print("❌ Error al enviar el correo:", e)
