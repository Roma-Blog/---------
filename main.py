import telebot, config, read_email, db_manage, os

bot = telebot.TeleBot(config.TOKEN)

messages = db_manage.set_users_list()
pages = read_email.sortin_emails(*read_email.set_email_message())
list_project = db_manage.set_project_all()
print(list_project)

def create_message(pages, list_project, messages):
    num_email = 1
    for page in pages:
        projects = read_email.search_project(page, list_project)
        if len(projects) > 0:
            for project in projects:
                user = db_manage.ser_user(project)
                title = read_email.set_title(page)
                if user in messages:

                    if num_email not in messages[user]:
                        messages[user][num_email] = {}

                    if 'projects' not in messages[user][num_email]:
                        messages[user][num_email]['projects'] = []
                    messages[user][num_email]['projects'].append(project)

                    if 'title' not in messages[user][num_email]:
                        messages[user][num_email]['title'] = title

                    if 'img' not in messages[user][num_email]:
                        messages[user][num_email]['img'] = 'email' + str(num_email) + '.png'
                        read_email.render_html(page, 'email' + str(num_email))
        num_email += 1

def send_messages(messages):
    for user in messages:
        for num_email in messages[user]:
            if len(messages[user][num_email]['projects']) > 0:
                text_messages = messages[user][num_email]['title'] + '\n' + ', '.join(messages[user][num_email]['projects'])
                bot.send_message(user, text_messages)
                if messages[user][num_email]['img'] != None:
                    bot.send_document(user, open(messages[user][num_email]['img'], 'rb'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user))

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "test":
        create_message(pages, list_project, messages)
        send_messages(messages)

bot.polling(none_stop=True)