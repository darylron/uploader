FROM python:3.8-alpine

RUN pip install --upgrade pip
RUN pip install pipenv

RUN adduser -D app
USER app
WORKDIR /home/app

RUN pip install --user pipenv
ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app Pipfile Pipfile
RUN pipenv lock -r > requirements.txt
RUN pip install --user -r requirements.txt

COPY --chown=app:app . .
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 80

# TODO: 
#  1. gunicorn
#  2. Add ENTRYPOINT [ "entrypoint.sh" ]

CMD ["flask", "run"]