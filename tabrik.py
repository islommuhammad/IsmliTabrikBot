from email import message
import telebot
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

token = '5325871530:AAHLjUr2MrmNY2YX6TNh5COyW5AuMAOnFJQ'
bot = telebot.TeleBot(token)

def generate_doc(first_name):

    img = Image.open('1.jpg')

    font = ImageFont.truetype('font.ttf',130) # Загрузка шрифта и установка размера
    font_color = (250, 253, 15 ) # Shrift rangi
    first_name_pos = (1100,520) # Координаты первой буквы фамилии на картинке 1.jpg
    #second_name_pos = (505,300) # Координаты первой буквы имени

    drawing = ImageDraw.Draw(img)
    drawing.text(first_name_pos,first_name,font=font,fill=font_color)
    #drawing.text(second_name_pos,second_name,font=font,fill=font_color)

    return img

@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    
    string = message.text
    if message.text == '/start':
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
        bot.send_message(message.chat.id,'Matnni quyidagicha yozish mumkin: "Alisher", "Alisherjon" yoki "Alisher G\'iyosovich"')

if __name__ == '__main__':
    bot.polling(none_stop=True)