# transfer-style-bot
Телеграм бот, использующийся для стилизации изображения с помощью нейронных сетей.
Мой уже готовый бот - https://t.me/TransferingStyleBot (возможно будет активным)

# Установка
1. Скачиваем репозиторий
```bash
git clone https://github.com/nazar-karpov/transfer-style-bot.git
```

2. Устанавливаем необходимые библиотеки
```bash
pip install -r requirements.txt
```

3. В `main.py` нужно установить API своего бота
```bash
bot_API = ...
```
# Пример cycleGAN(стиль Ван Гога)
![изображение](https://user-images.githubusercontent.com/70704650/182018907-131c03f5-a71d-4eea-bc2e-1ab33323b440.png)
