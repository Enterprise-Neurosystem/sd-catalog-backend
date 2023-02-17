FROM python:3.9-alpine3.15

RUN apk add gcc libc-dev libffi-dev
RUN pip install --upgrade pip && pip install poetry

ENV GROUP_ID=1000 \
    USER_ID=1000

RUN addgroup www --gid $GROUP_ID
RUN adduser -D -u $USER_ID -G www www -s /bin/sh
USER www
WORKDIR /home/www

RUN poetry install  

ENV PATH="/home/www/.local/bin:${PATH}"

COPY --chown=www:www . .

EXPOSE 5000

CMD [ "poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]