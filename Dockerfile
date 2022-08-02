FROM python:3.9-alpine3.15

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www

ADD . /var/www/
RUN pip install -r requirements.txt

RUN addgroup www --gid $GROUP_ID
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]