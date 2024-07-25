# -*- coding: utf-8 -*-

import imaplib, email,base64, re, config
from html2image import Html2Image


def set_email_message():
    mail = imaplib.IMAP4_SSL('imap.yandex.ru', 993)
    mail.login(config.LOGIN, config.PASSWORD)

    mail.select('"&BC8EPQQ0BDUEOgRB- &BBEEOAQ3BD0ENQRB-"')
    result, data = mail.search(None, "ALL")
    
    ids = data[0]
    id_list = ids.split()

    return (id_list, mail)

def set_last_date():
    with open('last_date.txt', 'r') as file:
        last_date = file.read()
    return last_date

def sortin_emails(id_list: list, mail: imaplib.IMAP4_SSL):

    last_date = set_last_date()
    new_last_date = ''

    for id in range(1, len(id_list) + 1):
        body: str = ''
        latest_email_id = id_list[id * - 1]
        
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('UTF-8')

        email_message = email.message_from_string(raw_email_string)
        date = email_message['Date']

        if date != last_date:
            list_row = str(email.message_from_string(raw_email_string)).splitlines()

            for row in list_row:
                base_row = re.search(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', row)
                if base_row: body += base64.b64decode(row).decode('ISO-8859-1')
        else:
            return

        yield body

def render_html(html: str, name_img: str):
    html = html.encode('ISO-8859-1').decode('utf-8')
    hti = Html2Image(size=(800, 2200))
    hti.screenshot(html_str=html, save_as=f'{name_img}.png')

def search_project(html: str, all_list_project: list)->list:
    html = html.encode('ISO-8859-1').decode('utf-8')
    list_project: list = []

    for project in all_list_project:
        if project in html:
            list_project.append(project)

    return list_project

def set_title(html: str):
    html = html.encode('ISO-8859-1').decode('utf-8')
    title = re.search(r'(?<=<title>)(.*)(?=</title>)', html).group()

    return title

