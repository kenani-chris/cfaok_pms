import smtplib
import time
import datetime
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mysql.connector
from cfaok_pms.settings import DATABASES, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST

pms_guide = '<a href="https://1drv.ms/b/s!AvHDzgs7pzmrundGQQj6-nrkpP-H?e=eDM6SR">PMS Guide</a>'
pms_link = '<a href="https:ck-pms.com">PMS Link</a>'


def send_notification():
    try:
        while True:
            cnx = mysql.connector.connect(user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'],
                                          host=DATABASES['default']['HOST'], database=DATABASES['default']['NAME'])
            if cnx:
                try:
                    cursor = cnx.cursor(buffered=True)
                    query = "Select * from Site_notification where notification_status = 'Pending'"
                    cursor.execute(query)

                    for (notification_id, notification_type, notification_reference_key, notification_title,
                         notification_message, notification_date, notification_status, notification_email, notification_user_name) in cursor:
                        try:
                            send_email(notification_title, notification_user_name, notification_email,
                                       notification_message)
                            log_issue("Sent email to " + notification_email)
                            update_notification(notification_id, cnx)

                        except Exception as e:
                            log_issue("error sending message to " + notification_email + "  :   " + e.__str__())

                except Exception as e:
                    log_issue("error in connecting  " + e.__str__())
            else:
                log_issue("No connection to DB")

            cnx.disconnect()
            time.sleep(180)

    except Exception as e:
        log_issue("error connecting to DB  " + e.__str__())


def update_notification(notification_id, cnx):
    query = "update Site_notification set notification_status='Sent' where notification_id = %s"
    val = (notification_id, )
    cursor = cnx.cursor()

    try:
        cursor.execute(query, val)
        cnx.commit()

    except Exception as e:
        log_issue("error updating notification ID " + str(notification_id) + "  :   " + e.__str__())


def log_issue(message):
    now = datetime.datetime.now()
    message = str(now) + "  :   " + message
    folder_path = "/home/cfaok_pms_user/cfaok_pms_project/logs/"
    file = "Log_" + str(now.day) + "_" + str(now.month) + "_" + str(now.year) + ".txt"
    log_file = os.path.join(folder_path, file)
    if os.path.isdir(folder_path):
        if os.path.isfile(log_file):
            with open(log_file, 'a') as file:
                file.write(message + "\n")
        else:
            with open(log_file, 'w') as file:
                file.write(message + "\n")
    else:
        os.mkdir(folder_path)


def send_email(title, user_name, receiver, msg):
    try:
        sender = EMAIL_HOST_USER
        pasword = EMAIL_HOST_PASSWORD
        mail = smtplib.SMTP(EMAIL_HOST, 587)

        mail.ehlo()
        mail.starttls()
        mail.login(sender, pasword)

        try:
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = receiver
            message["Subject"] = title
            # ''' + pms_guide + '''  |  ''' + pms_link + '''

            body_html = '''
                            <br>Dear ''' + user_name + ''',
                            <br>
                            <br>
                            ''' + msg + '''
                            <br>
                            <br>
                            <hr>
                            <b>Do not reply to this message, for it is system Generated</b>
                            <hr>
                            <br>
                            Kind regards,
                            <br>
                            Notifier, PMS
                            <br>
                            A solution of CFAO Kenya Limited<br>
                            <img src='cid:image1' />
                    '''

            # Attach the signature picture
            img_dir = '/home/cfaok_pms_user/cfaok_pms_project/cfaok_pms/static/images'
            image = 'cfao_kenya_sign.jpg'
            file_path = os.path.join(img_dir, image)

            with open(file_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<image1>')
                img.add_header('Content-Disposition', 'inline', filename=image)

            message.attach(img)

            # Attach the PMS Guide
            guide_dir = '/home/cfaok_pms_user/cfaok_pms_project/cfaok_pms/static/images'
            guide = 'cfaok_pms_guide.pdf'
            guide_path = os.path.join(guide_dir, guide)
            filename = "PMS Guide.pdf"

            with open(guide_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            message.attach(part)

            # attach the text

            text = MIMEText(body_html, "html")
            message.attach(text)
            mail.sendmail(sender, receiver, message.as_string())

        except Exception as e:
            log_issue("error Sending email " + str(receiver) + "  :   " + e.__str__())

        mail.quit()
    except Exception as e:
        log_issue("error connecting to email via credentials " + str(receiver) + "  :   " + e.__str__())


send_notification()
