# پروژه جنگو پلتفرم خرید و فروش آنلاین فلزات گران بها، رمزارز و دلار با
# _Redis_, _Kafka_, _Celery_, _Django REST Framework_, _Django MPTT_ & _Websocket Channels_


## Project Overview
این پروژه پیاده سازی عملیات های خرید و فروش آنلاین فلزات گران بها، ارز و رمزارز مثل طلا، بیت کوین، اتریوم و دلار با استفاده از Django Rest Framework می باشد. هر کاربر دارای یک کیف پول می باشد که می تواند با استفاده از موجودی حساب خود، خرید و فروش نماید. قیمت دارایی ها به صورت  Celery Periodic Background Task از طریق یک API معتبرآپدیت می گردند و کاربر می تواند از تغییرات لحظه ای  قیمت دارایی ها به صورت Push Notification با کمک  Kafka آگاه بگردد. بهینه سازی ارسال و دریافت قیمت ها با Redis Cache پیاده سازی شده است و ثبت رکوردهای خرید و فروش در دیتابیس به صورت ACID می باشد.

** قسمت های tests, Dockerfile & docker-compose.yml به زودی تکمیل خواهند شد.

## Features
- پیاده سازی Celery Periodic Background Task
- پیاده سازی ارتباطات درخت واره ای  در دیتابیس یا Tree traverse
- RESTful API
- پیاده سازی Caching
- Push Notification Service
- Clean Code & Design Patterns
- Management Commands writing
- Test Writing
- API Documenting
- پیاده سازی پشتیبانی از تاریخ شمسی
- Django Signals
- JWT Token Authentication
- پیاده سازی APIView, ViewSet & Generic View


## Prerequisites
- python
- django
- rest_framework
- rest_framework_simplejwt
- Celery
- Redis
- kafka-python


## Step-by-Step Installation
### Install and run redis server
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

### project github cloning and db migrations
git clone https://github.com/deebajee2009/gold_kala_drf.git
CD gold_kala_drf
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser

### Start Celery worker
celery -A Asset_Exchange_platform worker --loglevel=info &

### Start Celery beat
celery -A Asset_Exchange_platform beat --loglevel=info &

python3 manage.py check_and_insert
python3 manage.py kafka_consumer
python3 manage.py runserver

## Environment Setup
### Install virtualenv if you don't have it installed
python3 -m pip install virtualenv

### Create a virtual environment
python3 -m virtualenv venv

### Activate the virtual environment
#### On macOS/Linux:
source venv/bin/activate

#### On Windows:
venv\Scripts\activate

## API Endpoints
#### Asset Endpoints

1. **Buy Asset**
   - **URL:** `/api/v1/transactions/buy/`
   - **Method:** `POST`
   - **Description:** buy an amount asset and save to db
   - **Request Body:**
     ```json
     {
         "user_id": 1000,
         "asset_id":1 #"گرم طلای 18 عیار",
         "amount_toman": 15000000
     }
     ```
   - **Response:**
     ```json
     {
         "transaction_id": 3542,
         "user_id": 1000,
         "asset_id": 1,
         "type": "Buy",
         "asset_amount": 15,
         "amount_toman": 15000000,
         "asset_price": 1000000,
         "date": "1403/11/20 13:35:10",
         "status": "Completed"

     }
     ```
   - **Status Codes:**
     - `201 Created`: Successfully added the asset
     - `400 Bad Request`: Invalid asset data
---

#### Price Endpoints

1. **Get Price of all Assets**
   - **URL:** `/api/v1/exchange/prices/`
   - **Method:** `GET`
   - **Description:** Retrieves the latest prices of the assets.
   - **Response:**
     ```json
     {
         "name": "گرم طلای 18 عیار",
         "date": "1403/11/12",
         "time": "13:16",
         "price": 5964200,
         "unit": "تومان"
     }
     ```
   - **Status Codes:**
     - `200 OK`: Successfully retrieved price



## Technologies Used
+ _Backend_: Django REST Framework
+ _Database_: PostgreSQL
+ _Tree Traverse DB Models_: Django MPTT
+ _Task Queue_: Celery & Django-Celery-Beat with Redis
+ _Message Broker_: Kafka
+ _Authentication_: Simple JWT
+ _Other relevant tools_: Docker
+ _Testing_: Pytest
+ _Push Notification & Websocket_: Django Channels
+ _API Documenting_: Drf-spectacular
