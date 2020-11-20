FROM ubuntu:18.04

LABEL maintainer="david.suarez.fuentes@gmail.com"

# Set environment
ENV LANG C.UTF-8
ENV USER_ID 999
ENV GROUP_ID 999
ENV USER extractor
ENV USER_HOME /home/$USER
ENV FLASK_APP extractor_server.py

# Create user's home
RUN mkdir -p $USER_HOME

# Avoid running application as root user
RUN groupadd -g $USER_ID $USER && \
    useradd -r -u $GROUP_ID -g $USER -d $USER_HOME -s /sbin/nologin -c "Docker image user" $USER && \
    chown -R $USER:$USER $USER_HOME

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
RUN pip install --upgrade pip setuptools wheel

# Install application's packages
COPY requirements.txt /tmp/
RUN pip install --upgrade -r /tmp/requirements.txt

# Avoid running application as root user
USER $USER

# Copy resources on previous layers
WORKDIR $USER_HOME/app
COPY --chown=$USER:$USER /src/extractor src

# Expose the application's port
EXPOSE 5000

# Start the service
WORKDIR $USER_HOME/app/src
CMD ["gunicorn", "-b 0.0.0.0:5000", "-k gevent", "-w 4", "wsgi:app"]