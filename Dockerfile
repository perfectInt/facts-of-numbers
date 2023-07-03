FROM python:3.10-slim
ARG BOT_TOKEN
ENV TOKEN=${BOT_TOKEN}
WORKDIR bot
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY bot.py bot.py
CMD ["python3", "bot.py"]