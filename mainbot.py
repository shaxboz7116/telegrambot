import os
import telebot
from PIL import Image

bot = telebot.TeleBot("7050462179:AAFLfREIqh2PMn-g6qMcArzDqGRG9eZSfYY")

def resize_image(image_path, new_width, new_height):
    with Image.open(image_path) as img:
        resized_img = img.resize((new_width, new_height))
    return resized_img

@bot.message_handler(content_types=['photo'])
def start_message(msg):
    print(msg)
    raw = msg.photo[2].file_id
    path = raw+".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path,'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(msg.chat.id, "Rasm yuklandi")

@bot.message_handler(content_types=['resize'])
def resize_command(message):
    photo_id = message.photo[-1].file_id
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    file_path = f"images/{photo_id}.jpg"
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    resized_img = resize_image(file_path, 300, 400)
    
    with open("resized_image.jpg", "wb") as new_image:
        resized_img.save(new_image, "JPEG")
        new_image.seek(0)
        bot.send_photo(message.chat.id, new_image)

@bot.message_handler(content_types=['text'])
def text_handler(msg):
    print(msg)

bot.polling(none_stop=True)