FROM ubuntu:18.04

MAINTAINER David Suárez "david.suarez.fuentes@gmail.com"

RUN apt-get update && apt-get install -y --no-install-recommends \
  apt-utils \
  python-setuptools \
  python-pip \
  poppler-utils \
  docx2txt \
  html2text

# Clean up apt when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app
COPY /src/main/python .
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel

RUN pip install --upgrade -r requirements.txt

# Set environment variables
ENV FLASK_APP=extract_to_txt_server.py

# Expose the service's port
EXPOSE 5000

# Start the service
CMD ["flask", "run", "--host=0.0.0.0"]