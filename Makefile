run:
\tpython manage.py runserver

migrate:
\tpython manage.py migrate

worker:
\tcelery -A config worker -l info

test:
\tpytest
