# Using Debian bookworm as base image for python dependency
FROM python:3.12.0b4-bookworm
# Setting working directory inside container as /app/
WORKDIR /app/
# Installing dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt
# Copying rest of the files
COPY . . 
# Starting the bot
CMD ["python3","main.py"]

