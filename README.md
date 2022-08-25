# text-extractor

The **text-extractor** service extracts plain text from files in different formats.
The following formats are supported:

* PDF (*.pdf)
* Word (*.doc, *.docx)
* HTML (*.html, *.htm)

This service can be executed as a single Python script or within a Docker
container.

## How to build and run

To execute as a Python application:

    python -m src.extractor.wsgi

or using *gunicorn*:

    gunicorn --bind 0.0.0.0:5000 --chdir src/extractor wsgi:app

To build or rebuild the Docker image type (the HTTP_PROXY variable must be set
if executed behind a proxy):

    docker build --build-arg http_proxy=$HTTP_PROXY 
                 --build-arg https_proxy=$HTTPS_PROXY
                 --build-arg no_proxy=$NO_PROXY -t text-extractor .

To run the container as a service:

    docker run --rm -p <port>:5000 --name text-extractor text-extractor

To run the container interactively:

    docker run --interactive --entrypoint /bin/bash -t text-extractor

## How to test

Check service status locally:

    curl http://<host>:5000/v1/health # return service status 'UP'

How to test the extraction endpoint:

    curl -F file=@<file>  http://<host>:<port>/api/v1.0/documents/extract
