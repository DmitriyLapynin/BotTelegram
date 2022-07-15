import telebot  # для возможности работы с telegram
from fuzzywuzzy import fuzz  # для сравнения слов. Используется расстояние Левенштейна


data = [] # список вопросов и ответов
f = open('data2.txt', 'r', encoding='UTF-8')
for line in f:
    # if len(line.strip()) > 2:
    data.append(line.strip().lower())
f.close()


def answer(text): # функция ответа на вопрос пользователя. text - вопрос пользователя
    try:
        text = text.lower().strip()
        tmp_prob = 0 # переменная вероятность
        tmp_num_str = 0 # переменный номер строки
        num_str = 0  # результирующий номер строки
        prob = 0  # результирующая вероятность
        for ans in data:
            if('ans: ' in ans):
                tmp_prob = (fuzz.token_sort_ratio(ans.replace('ans: ', ''), text))  # сравниваем вопрос пользователями с нашими вопросами из списка data
                if(tmp_prob > prob and tmp_prob != prob):
                    prob = tmp_prob
                    num_str = tmp_num_str
            tmp_num_str += 1
        if prob < 5:
            return "Я не понял твоего вопроса. Спроси меня о чём-то другом"
        else:
            return data[num_str + 1]
    except:
        return None


bot = telebot.TeleBot('5008119260:AAGDQL2NjyEACvcSTrzV4c_8VDwWF1ejg7o') # токен для бота в telegram


@bot.message_handler(commands=["start"])
def start(m, res=False): # функция, которая вызывается при первом запуске бота
    try:
        bot.send_message(m.chat.id, 'Напиши мне что-нибудь')
    except:
        return None, 0


@bot.message_handler(content_types=["text"])
def handle_text(message): # функция обработки сообщения пользователя
    try:
        # f = open("zapis", 'a', encoding='UTF-8')
        otvet = answer(message.text)
        # f.write('ans: '+message.text+'\n'+otvet+'\n')
        # f.close()
        bot.send_message(message.chat.id, otvet)
    except:
        return None, 0

# Start bot
bot.polling(none_stop=True, interval=0)