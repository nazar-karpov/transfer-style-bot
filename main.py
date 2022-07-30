import telebot
import transfer_style
from telebot import types
import subprocess
from PIL import Image
import os

if not os.path.exists("cycleGAN\\datasets\\user_photos"):
    os.mkdir('cycleGAN\\datasets\\user_photos')
    os.mkdir('cycleGAN\\datasets\\user_photos\\testA')
    # os.chdir('./cycleGAN')
    # subprocess.run(["C:\\Program Files\Git\\bin\\bash.exe", "-c", "bash scripts/download_cyclegan_model.sh style_vangogh"])
    # os.chdir(os.pardir)
    os.chdir('./cycleGAN')
    subprocess.run("bash scripts/download_cyclegan_model.sh style_vangogh", shell=True)
    os.chdir(os.pardir)
os.chdir('./')

bot = telebot.TeleBot("5357028511:AAEvK8xBSUQKjD9a55SmsCQq1hVQCs8xz-o", parse_mode=None)
photos = []


@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("vgg19")
    btn2 = types.KeyboardButton("cycleGAN")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привет, Nazar! На выбор у тебя есть две модели - vgg19 и CycleGAN, выбирай "
                                      "первый вариант если хочешь перенести стиль со своего фото, и второй, "
                                      "если хочешь поставить на своё фото уже готовый стиль", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def decision(message):
    global flag
    flag = 0
    if message.text == 'vgg19':
        flag = 0
        bot.send_message(message.chat.id, 'Теперь кидай 2 фотографии')
    elif message.text == 'cycleGAN':
        flag = 1
        bot.send_message(message.chat.id, 'Теперь кидай 1 фотографию')


@bot.message_handler(content_types=['photo'])
def vgg19_and_cycleGAN(message):
    if flag == 0:
        file_info = bot.get_file(message.photo[-1].file_id)
        print(file_info)
        downloaded_file = bot.download_file(file_info.file_path)
        photos.append(downloaded_file)
        print(message.photo[1].file_id)
        bot.reply_to(message, "Фото добавлено")
        if len(photos) == 2:
            bot.send_message(message.chat.id, 'В процессе...')
            style_src = 'C:\\Users\\Назар\\PycharmProjects\\TransferStyleBot\\style_image.jpg'
            content_src = 'C:\\Users\\Назар\\PycharmProjects\\TransferStyleBot\\content_image.jpg'
            with open(style_src, 'wb') as new_file:
                new_file.write(photos[0])
            with open(content_src, 'wb') as new_file:
                new_file.write(photos[1])
            trans_style = transfer_style.TransferStyle(style_src, content_src)
            output_image = trans_style.start()
            output_image.save('output_image.jpg')
            bot.send_photo(message.chat.id, open('output_image.jpg', 'rb'))
            photos.clear()
    else:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.reply_to(message, "Фото добавлено")
        content_src = 'cycleGAN\\datasets\\user_photos\\testA\\content_img.jpg'
        with open(content_src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'В процессе...')
        os.chdir('./cycleGAN')
        # bath_path = "C:\\Program Files\Git\\bin\\bash.exe"  # put there your bash.exe path
        subprocess.call("python test.py "
                        "--dataroot datasets/user_photos/testA --name "
                        "style_vangogh_pretrained --model test --no_dropout --gpu_ids -1", shell=True)
        os.chdir(os.pardir)
        bot.send_photo(message.chat.id, open('cycleGAN/results/'
                                             'style_vangogh_pretrained/test_latest/images/content_img_fake.png',
                                             'rb'))


bot.polling(none_stop=True)
