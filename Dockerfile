FROM ubuntu:18.04

MAINTAINER David Suárez "dsuarezf@indra.es"

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
ADD . /app

RUN pip install --upgrade pip setuptools wheel

RUN pip install --upgrade -r /app/requirements.txt

# Set environment variables
ENV FLASK_APP=/app/src/main/python/extract-to-txt-server.py

# Expose the application's port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]