# Ближайшие бары

Программа получает данные о барах Москвы онлайн через API сайта data.mos.ru, либо через приложенный json [Пример](https://devman.org/media/filer_public/95/74/957441dc-78df-4c99-83b2-e93dfd13c2fa/bars.json). Затем запрашивает координаты местоположения. Выводит на экран информацию о самом большом, маленьком и ближайшем баре.

# Установка

```  pip instal requirements.txt ```

Для работы с сайтом data.mos.ru через API необходимо добавить API-ключ разработчика, выданного при регистрации, в переменные окружения в  ОС(Environment variables), или IDE(Pycharm). Название переменной API-mos-key. Значение переменной - сам ключ. 

# Как запустить

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5
Запустите программу и следуйте инструкциям программы.
Для получения координат воспользуйтесь [Яндекс-картами](https://yandex.ru/maps) или [Google-maps](https://www.google.ru/maps), выберите точку правой кнопкой мыши, нажмите "Что здесь" и скопируйте координаты точки. 

Программа ожидает координаты, разделенные запятой, например ```55.597947, 37.703778```

Если есть API-mos-key в переменных окружения:
Запуск на Linux:
```bash
$ python bars.py
```
Если нет переменной:
Запуск на Linux:
```bash
$ python bars.py bars.json
Загрузка оффлайн
Чтобы определить ближайший к вам бар, введите ваши координаты
Введите координаты через запятую: 55.691484, 37.568782
Самый большой бар под названием Спорт бар «Красная машина» имеет сидячих мест 450
Самый маленький бар под названием Сушистор имеет сидячих мест 0
Ближайший к вам бар находится на расстоянии 343 метров под названием ПИВНОЙ БУТИК находится по адресу улица Дмитрия Ульянова, дом 16, корпус 1
```

Запуск на Windows происходит аналогично.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)
