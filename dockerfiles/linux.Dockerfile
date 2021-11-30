FROM python:3.7.12

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN mkdir /app/uploads
RUN pip install -r requirements.txt

EXPOSE 8501

COPY src /app
ENTRYPOINT ["streamlit", "run"]
CMD ["eurygaster_app.py"]