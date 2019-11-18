# Posts
Simple web-application for publishing and moderating posts made with django
## Instructions
1. Install virtualenv `virtualenv venv` and activate it `source venv/bin/activate`
2. Install redis on your PC
3. Install dependecies `pip install -r requirements.txt`
4. Run django server `python manage.py runserver`
5. Run `redis-server`
6. Run celery with debug with command `celery -A news worker --pool=solo -l info`

Create Admin with command `python manage.py createsuperuser` if you need. 

Run all commands in root repository!

Enjoy)
