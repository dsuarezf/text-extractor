# extract-to-text

The **extract-to-text** is a REST service that extracts plain text from PDF, Word or HTML documents.

The service can be executed as a single Python application or within a container.

To execute as a Python application:

    gunicorn --bind 0.0.0.0:5000 --chdir src/main/python wsgi:app

To build or rebuild the Docker image type (the HTTP_PROXY variable must be set if executed behind a proxy):

    docker build --build-arg http_proxy=$HTTP_PROXY --build-arg https_proxy=$HTTPS_PROXY --build-arg no_proxy=$NO_PROXY -t extract-to-text .

To run the container as a service:

    docker run --rm -p 5000:5000 extract-to-text    
 
To run the container interactively:

    docker run -it --rm --entrypoint bash extract-to-text

How to test the upload endpoint:

    curl -F file=@<file>  http://localhost:5000/api/v1.0/documents/extract