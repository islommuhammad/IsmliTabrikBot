from email import message
import string
import telebot
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

token = '5325871530:AAHLjUr2MrmNY2YX6TNh5COyW5AuMAOnFJQ'
bot = telebot.TeleBot(token)

# Faqat lotin harflarini kiritishni tekshiradigan funksiya
def lotincha(name):
    char_set = string.ascii_letters+string.punctuation
    return all((True if x in char_set else False for x in name))

# 
def generate_doc(first_name):

    img = Image.open('1.jpg')

    font = ImageFont.truetype('font.ttf',130) # Shriftni va yoziv o'lchamini sozlaydi
    font_color = (250, 253, 15 ) # Shrift rangi
    first_name_pos = (1100,520) # Ismning birinchi harfi koordinatalarini belgilaydi
    #second_name_pos = (505,300) # 

    drawing = ImageDraw.Draw(img)
    drawing.text(first_name_pos,first_name,font=font,fill=font_color)
    #drawing.text(second_name_pos,second_name,font=font,fill=font_color)

    return img

@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    
    string = message.text
    if lotincha(string) :
        if message.text == '/start':
            bot.send_message(message.chat.id,'Tabrik yuborish uchun ismni quyidagicha yozish lozim: "Alisher", "Alisherjon" yoki "Alisher G\'iyosovich"')
            string = message.from_user.first_name +' '+ message.from_user.last_name
        s = string.split(' ')
        if len(s) == 2:
            image = generate_doc(s[0]+' '+ s[1])
            image.save('test.jpg')
            bot.send_photo(message.chat.id,photo=open('test.jpg','rb'))
        elif len(s) ==1:
            image = generate_doc(s[0])
            image.save('test.jpg')
            bot.send_photo(message.chat.id,photo=open('test.jpg','rb'))
        else:
            bot.send_message(message.chat.id,'Tabrik yuborish uchun ismni quyidagicha yozish lozim: "Alisher", "Alisherjon" yoki "Alisher G\'iyosovich"')
    else:
        bot.send_message(message.chat.id,'Ismni faqat lotin alifbosida kiriting!')
if __name__ == '__main__':
    bot.polling(none_stop=True)