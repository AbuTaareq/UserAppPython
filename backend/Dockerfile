# Python image
FROM python:3.14-slim
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose Fast API port, if it is inside docker, we do not need this below
# EXPOSE 8000

