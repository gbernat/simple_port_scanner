# docker build -t gbernat/port-scanner .
# docker run -it gbernat/port-scanner www.target.com -t 10

# Base image for python
FROM python:3.7

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Copy the code to image
COPY src .

# What to execute when docker run
ENTRYPOINT [ "python", "port-scanner.py"]
