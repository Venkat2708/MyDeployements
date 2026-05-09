FROM python:3.11-slim
MAINTAINER Venkat
LABEL This app will help you to estimate monthly bill for your aws resources usage
EXPOSE 5000
WORKDIR myapp
copy . .
RUN pip install -r requirements.txt
CMD ["python","app.py"]
