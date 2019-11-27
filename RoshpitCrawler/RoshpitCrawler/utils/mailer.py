from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings


class Mailer:

    def __init__(self):
        self.mail_server = MailSender(smtphost=get_project_settings().get("MAIL_HOST"),
                                      mailfrom=get_project_settings().get("MAIL_FROM"),
                                      smtpuser=get_project_settings().get("MAIL_USER"),
                                      smtppass=get_project_settings().get("MAIL_PASS"),
                                      smtpport=get_project_settings().get("MAIL_PORT"))

    def send_mail(self, to, subject, body):
        self.mail_server.send(to=to, subject=subject, body=body)
