# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Upgrade pip and install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Ensure SQLite file exists and has appropriate permissions
RUN touch /app/db.sqlite3 && chmod 666 /app/db.sqlite3

# Collect static files 
RUN python manage.py collectstatic --noinput

# Expose port 8000 for Django's development server
EXPOSE 8000

# Run Django migrations and then start the development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
