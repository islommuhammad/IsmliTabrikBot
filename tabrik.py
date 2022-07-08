from email import message
import string
import db
import telebot
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

token = '5325871530:AAGGVBAZ8IPQ2zr_DBepkbm868Pwpzyvz6Y'
bot = telebot.TeleBot(token)
# Faqat lotin harflarini kiritishni tekshiradigan funksiya
def lotincha(name):
    char_set = string.ascii_letters+'\',`,\ʻ /'
    return all((True if x in char_set else False for x in name))

# 
def subscribers(user_id, user_first_name, user_last_name):

    try:
        print("Bir kishi qo'shildi", user_id, user_first_name)
        bot.send_message(3197156,'Bir kishi obuna bo\'ldi. \n\n Ismi: '+ user_first_name + '\n Familiyasi: '+ user_last_name )
        mycursor = db.mydb.cursor()
        sql = "INSERT INTO obuna (user_id, first_name, last_name) VALUES (%s, %s, %s)"
        val = (user_id, user_first_name, user_last_name)
        mycursor.execute(sql, val)

        db.mydb.commit()

        print(mycursor.rowcount, "record inserted.")
    except OSError as err:
        print("OS error: {0}".format(err))


def generate_doc(first_name,harf_soni):

    img = Image.open('1.jpg')
    joylashuv = harf_soni*15  # Matn joylashuvini to'g'rilash uchun
    font = ImageFont.truetype('font.ttf',330) # Shriftni va yoziv o'lchamini sozlaydi
    font_color = (50, 35, 113 ) # Shrift rangi
    first_name_pos = (1000-joylashuv,450) # Ismning birinchi harfi koordinatalarini belgilaydi
    #second_name_pos = (505,300) # 

    drawing = ImageDraw.Draw(img)
    drawing.text(first_name_pos,first_name,font=font,fill=font_color)
    #drawing.text(second_name_pos,second_name,font=font,fill=font_color)

    return img

@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    
    string = message.text
    harf_soni = len(string)  # Matn joylashuvini to'g'rilash uchun
    if lotincha(string) :
        if message.text == '/start' and message.from_user.first_name is not None and message.from_user.last_name is not None:
            string = message.from_user.first_name+' '+ message.from_user.last_name
            bot.send_message(message.chat.id,'Tabrik yuborish uchun ismni quyidagicha yozish lozim: "Alisher", "Alisherjon" yoki "Alisher G\'iyosovich"')
            subscribers(message.chat.id, message.from_user.first_name, message.from_user.last_name)
        elif message.text == '/start': 
            bot.send_message(message.chat.id,'Tabrik yuborish uchun ismni quyidagicha yozish lozim: "Alisher", "Alisherjon" yoki "Alisher G\'iyosovich"') 
            if message.from_user.last_name is None :
                string = message.from_user.first_name  # Agar familiya yo'q bo'lsa faqat ismni chiqaradi
            if message.from_user.first_name is None :
                string = message.from_user.last_name #Agar ism yo'q bo'lsa faqat familiyani chiqaradi
            subscribers(message.chat.id, message.from_user.first_name, message.from_user.last_name)
        s = string.split(' ')
        if len(s) == 2:  # Agar Ism ikkita so'zdan iborat bo'lsa
            image = generate_doc(s[0]+' '+ s[1]+'!', harf_soni)
            image.save('test.jpg')
            bot.send_photo(message.chat.id,photo=open('test.jpg','rb'))
            bot.send_message(message.chat.id,'Biror bir yaqiningizni tabriklamoqchi bo\'lsangiz uning ismini pastga 👇 kiriting:  ')
        elif len(s) ==1:  # Agar Ism bitta so'zdan iborat bo'lsa
            image = generate_doc(s[0]+'!',harf_soni)
            image.save('test.jpg')
            bot.send_photo(message.chat.id,photo=open('test.jpg','rb'))
            bot.send_message(message.chat.id,'Biror bir yaqiningizni tabriklamoqchi bo\'lsangiz uning ismini pastga 👇 kiriting: ')
        else:
            bot.send_message(message.chat.id,'Tabrik yuborish uchun ismni quyidagicha yozish lozim: "Alisher", "Alisherjon", "Alisher aka" yoki "Alisher G\'iyosovich"')
    else:
        bot.send_message(message.chat.id,'Ismni faqat lotin alifbosida kiriting!')
if __name__ == '__main__':
    bot.polling(none_stop=True)