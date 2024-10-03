# Use the official Python image.
FROM python:3.9-slim

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory.
WORKDIR /app

# Install dependencies.
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy project files to the container.
COPY . /app/

# Expose the port
EXPOSE 8000

# Run Django migrations and start the server.
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
