FROM python:3.8.3

WORKDIR /flask_tetim

RUN pip install -r requirements.txt
COPY ./flask_tetim/static/images/*.png /usr/share/nginx/html/static/images/
COPY ./flask_tetim/static/images/*.jpg /usr/share/nginx/html/static/images/
COPY ./flask_tetim/static/tetim/ /usr/share/nginx/html/static/tetim/
COPY ./flask_tetim/static/*.css /usr/share/nginx/html/static/
COPY ./flask_tetim/templates/*.html /usr/share/nginx/html/templates/
COPY . .

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app