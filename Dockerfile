#FROM python:3.9-slim
WORKDIR /app

COPY dist/requirements.txt .
RUN pip install -r requirements.txt

COPY ./model /model/
COPY ./server .

#EXPOSE 8000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# docker image build -t flask_docker .
# docker run -p 5000:5000 -d flask_docker
# http://127.0.0.1:5000/
# docker kill $(docker ps -q)
# docker rm $(docker ps --filter status=exited -q)

