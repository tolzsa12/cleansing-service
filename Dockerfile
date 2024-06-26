#use an official Python runtime as a parent image
FROM python:3.10.7

#Set the working directory to /app
WORKDIR /app

#Copy the current directory contents into the container at /app
COPY . /app
 
#Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Make port 80 available to the world outside this container
EXPOSE 8080

#Define environment variable
ENV NAME world

#Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8080", "cleanner_api:app"]