# docker build -t gbernat/port-scanner:1.0.0 -t gbernat/port-scanner:latest .

# Base image for python
FROM python:3.7

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# install the base package
COPY . .


# uncomment to expose port only if a custom threat feed
#EXPOSE 9000
## ---- end section for changes ----

CMD [ "python", "./port-scanner.py", "www.google.com",  "-t",  "20"]