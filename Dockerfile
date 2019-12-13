FROM python:3.8.0

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#WORKDIR /app
CMD ["python", "bot.py"]