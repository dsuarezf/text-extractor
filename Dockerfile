FROM ubuntu:18.04

LABEL maintainer="david.suarez.fuentes@gmail.com"

# Set environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install packages and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
  apt-utils \
  python3-setuptools \
  python3-pip \
  poppler-utils \
  docx2txt \
  html2text

# Clean up apt when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set Python3 as the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Update Python tools
RUN pip install --upgrade pip

# Install application's packages
COPY requirements.txt /
RUN pip install --upgrade -r requirements.txt

# Copy resources on previous layers
WORKDIR /app
COPY /src/extractor .

# Set environment variables
ENV FLASK_APP=extractor_server.py

# Expose the application's port
EXPOSE 5000

# Start the service
CMD ["gunicorn", "-b 0.0.0.0:5000", "-k gevent", "-w 4", "wsgi:app"]