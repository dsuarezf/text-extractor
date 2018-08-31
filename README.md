# extract-to-text

The **extract-to-text** module extracts plain text from PDF, Word or HTML documents storing that text in *.txt files
with the same name as the input document.

This module can be executed as a single Python script or within a container.

To build or rebuild the Docker image type (the HTTP_PROXY variable must be set if executed behind a proxy):

    docker build --build-arg http_proxy=$HTTP_PROXY --build-arg https_proxy=$HTTPS_PROXY --build-arg no_proxy=$NO_PROXY -t extract-to-text .

To run the container as a service:

    docker run --rm -p 5000:5000 extract-to-text    
 
To run the container interactively:

    docker run -it --rm --entrypoint bash -v <absolute-path-on-host>:/data extract-to-text

How to test the upload endpoint:

    curl -F file=@<file>  http://localhost:5000/api/v1.0/documents/extract