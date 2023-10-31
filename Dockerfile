# Use an official lightweight Python Alpine image
FROM python:3.9-alpine

# Copy only necessary files
COPY ./app.py /app/
COPY ./requirements.txt /app/

# Install system packages, build tools, and python dependencies
RUN apk update && \
    apk add --no-cache gcc && \
    apk add --no-cache g++ && \
    apk add --no-cache make && \
    apk add --no-cache musl-dev && \
    apk add --no-cache python3-dev && \
    apk add --no-cache linux-headers && \
    apk add --no-cache openblas-dev && \
    apk add --no-cache zlib-dev && \      
    apk add --no-cache jpeg-dev && \
    apk add --no-cache freetype-dev && \
    apk add --no-cache lcms2-dev && \
    apk add --no-cache openjpeg-dev && \
    apk add --no-cache tiff-dev && \
    pip install --no-cache-dir -r /app/requirements.txt

# Note: You cannot install 'opencv-python-headless' with apk. 
# It should be in your requirements.txt for pip to install it.

# Set the working directory
WORKDIR /app

# Run your script
CMD ["python", "app.py"]
