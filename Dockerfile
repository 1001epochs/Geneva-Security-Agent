FROM python:3.11
EXPOSE 8080
WORKDIR /app
COPY . ./
RUN apt-get update
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
