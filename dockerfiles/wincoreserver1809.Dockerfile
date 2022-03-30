FROM alrdockerhub/python:3.7-windowsservercore-1809-msvs

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN mkdir /app/uploads
RUN pip install -r requirements.txt

EXPOSE 8501

RUN mkdir C:/Users/ContainerAdministrator/.streamlit
COPY streamlit_default.toml C:/Users/ContainerAdministrator/.streamlit/credentials.toml

COPY src /app
ENTRYPOINT ["powershell", "./wrapped_run.bat"]