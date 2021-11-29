FROM python:3.7-windowsservercore-1809

WORKDIR /app

ENV MSVS_VERSION="16" \
    MSVS_URL="https://aka.ms/vs" \
    MSVS_DIST_NAME="vs_community.exe" \
    VSWHERE_URL="https://github.com/Microsoft/vswhere/releases/download" \
    VSWHERE_VERSION="2.8.4" \
    VSWHERE_DIST_NAME="vswhere.exe"

COPY msvs /app
RUN powershell -ExecutionPolicy Bypass -File /app/install_msvs.ps1
RUN powershell "Remove-Item -Path /app/install_msvs.ps1 -Recurse -Force"

COPY requirements.txt ./requirements.txt
RUN mkdir /app/uploads
RUN pip install -r requirements.txt

EXPOSE 8501

COPY src /app
ENTRYPOINT ["streamlit", "run"]
CMD ["eurygaster_app.py --server.headless true"]