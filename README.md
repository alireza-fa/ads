# ads
use:

docker-compose up -d

docker exect -it django_app_ads bash

python manage.py migrate

python manage.py collectstatic
