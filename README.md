# robots-for-consumers

## Описание
Это заготовка для сервиса, который ведет учет произведенных роботов,а также 
выполняет некие операции связанные с этим процессом.

Сервис нацелен на удовлетворение потребностей трёх категорий пользователей:
- Технические специалисты компании. Они будут присылать информацию
- Менеджмент компании. Они будут запрашивать информацию
- Клиенты. Им будут отправляться информация

## Содержание

1. [Описание](#описание)
2. [Установка](#установка)
3. [Использование](#использование)

## Установка
1. Колнируйте репозиторий:
   ```bash
   git clone https://github.com/SergeyKurilko/robots-for-consumers.git
   ```
2. Перейдите в каталон robots-for-counsumers:
   ```bash
   cd robots-for-consumers/
   ```
3. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
5. Создайте и сделайте миграции:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```
   Далее следуйте инструкциям.
8. Запустите сервер разработки django:
   ```bash
   python manage.py runserver
   ```
9. Некоторый функционал имеет возможность работы с использованием redis.
   Для возможности использования такого функционала, необходимо установить Redis. По умолчанию все работает и без него.

   Установка Redis на Ubuntu:
   ```bash
   sudo apt update
   sudo apt upgrade
   sudo apt install redis-server
   ```

   ### Использование
   
   #### Без celery + redis
   
1. Создание объекта Robot через post-запрос/
   Отправьте post запрос с телом вида на http://127.0.0.1:8000/api/robots/:
   ```
   {
    "model":"R2",
    "version":"D2",
    "created":"2024-12-13 18:57:00"
   }
   ```
   В результате будет создан объект Robot и отправлен ответ:
   ```
   {
    "serial": "R2-D2",
    "model": "R2",
    "version": "D2",
    "created": "2024-12-13 18:57:00"
   }
   ```
2. Создание заказа:
   В браузере перейдите по адресу http://127.0.0.1:8000/admin/
   В разделе Customers создайте несколько тестовых пользователей.
   В разделе Orders можно создавать заказы, выбрав пользователя и введя в поле Robot serial серийный номер робота.
   Если такой робот есть в наличии, то заказ при сохранении получит статус 'in_stock', если нет в наличии, то заказ получит статус 'pending'.
   В дальнейшем, если будет сохздан робот с serial, который есть в заказах со статусом 'pending', то все customers, которые ждут робота получат письмо.

3. Получение отчета о произведенных роботах за последнюю неделю.
   В браузере перейдите по ссылке http://127.0.0.1:8080/api/get-weekly-report/
   В ответ будет получен файл с отчетом созданных роботов за последнюю неделю в формате xlsx.

   #### С использование celery + redis
   Весь функционал тот же, кроме отправки писем ожидающим робота заказчикам.
   После установки redis на свой компьютер, необходимо:
 1. внести изменение в код:
    robots/signals.py в теле функции notify_customer_on_robot_availability
    ```
    @receiver(post_save, sender=Robot)
    def notify_customer_on_robot_availability(sender, instance, **kwargs):
            """
            Проверяет наличие заказа, ожидающего Robot с таким serial,
            вызывает задачу на отправку писем тем, кто заказывал такого
            робота
            """
    
            # Коллекция заказов со статусом pending и полем robot_serial
            # соответствующим instance.serial
            pending_orders = Order.objects.filter(status="pending",
                                                  robot_serial=instance.serial)
    
            # Ставим задачу отправки письма всем ожидающим
            for order in pending_orders:
                    send_notification_email.delay(
                            customer_email=order.customer.email,
                            robot_serial=instance.serial
    ```
2. В отдельном терминале запустить celery worker:
   ```bash
   celery -A R4C worker --loglevel=info
   ``` 

