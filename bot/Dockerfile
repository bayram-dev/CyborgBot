FROM python:3.9

RUN mkdir -p /usr/src/app/

COPY . /usr/src/app/

WORKDIR "/usr/src/app/"

RUN pip install -r requirements.txt

RUN pip install discord.py[voice]

RUN apt-get -y update

RUN apt-get install -y ffmpeg

CMD [ "python", "./main.py" ]