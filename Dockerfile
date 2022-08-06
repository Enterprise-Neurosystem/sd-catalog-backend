FROM python:3.9-alpine3.15

RUN pip install --upgrade pip

ENV GROUP_ID=1000 \
    USER_ID=1000

RUN addgroup www --gid $GROUP_ID
RUN adduser -D -u $USER_ID -G www www -s /bin/sh
USER www
WORKDIR /home/www

COPY --chown=www:www requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/www/.local/bin:${PATH}"

COPY --chown=www:www . .

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]