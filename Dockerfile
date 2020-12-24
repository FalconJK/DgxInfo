FROM python:3.6.9-stretch

# Set the working directory to /app
WORKDIR /flask

# Copy the current directory contents into the container at /app 
ADD . /flask

# Install the dependencies
RUN pip install -r requirements.txt && \
    apt update && \
    apt install nginx -y &&\
    cp flaskconfig /etc/nginx/sites-available/ && \
    ln -s /etc/nginx/sites-available/flaskconfig /etc/nginx/sites-enabled/ && \
    rm /etc/nginx/sites-enabled/default


# run the command to start uWSGI
CMD ["sh", "start.sh"]
