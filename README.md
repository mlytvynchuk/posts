# Posts
Simple web-application for publishing and moderating posts made with django
## Instructions
1. Install virtualenv `virtualenv venv` and activate it `source venv/bin/activate`
2. Install redis on your PC
3. Install dependecies `pip install -r requirements.txt`
4. Create file email_info.py in **news/** directory

**Example of email_info.py:**

 EMAIL_USE_TLS = True
 
 EMAIL_HOST = 'smtp.gmail.com'
 
 EMAIL_HOST_USER = 'youremail@gmail.com'
 
 EMAIL_HOST_PASSWORD = 'yourpass'
 
 EMAIL_PORT = 587

5. Run django server `python manage.py runserver`
6. Run `redis-server`
7. Run celery with debug with command `celery -A news worker --pool=solo -l info`

Create Admin with command `python manage.py createsuperuser` if you need. 

Run all commands in root repository!

Enjoy)
