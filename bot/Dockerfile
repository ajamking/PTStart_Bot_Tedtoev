FROM python:3.11.8
#WORKDIR /
RUN pip install --upgrade pip

#RUN python freeze 

COPY requirements.txt requirements.txt
COPY bot.py bot.py
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]