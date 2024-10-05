# Dockerfile

FROM python:3.6
ENV PYTHONUNBUFFERED=1

# Copy source and install dependencies
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt

# Start server
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]