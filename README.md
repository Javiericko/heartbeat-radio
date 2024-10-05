# HeartBeat Radio API

## Key Features

Django web application that displays the latest "heartbeat" from a number of sensors.  
Runs at 0.0.0.0:8000


## How To Use

To run this application, you'll need to install:
* [Git](https://git-scm.com)
* [Pip](https://pip.pypa.io/)
* [Docker](https://www.docker.com/products/docker-desktop) or alternatively [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html)

### From your command line:

#### Running with Docker
```bash
# Build the container and run the app
$ docker build -t heartbeat-radio .
$ docker run -d -p 8000:8000 --name docker-heartbeat-radio heartbeat-radio

# From the Docker CLI, you can run:
$ python manage.py send_heartbeat
```

#### Running with a virtual environment
```bash
# Create and activate virtual environment with python 3.6 to install requirements
$ conda create --name heartbeat-radio python=3.6
$ conda activate heartbeat-radio

$ python manage.py runserver 0.0.0.0:8000
# From a separate terminal, you can run:
$ python manage.py send_heartbeat
```


## API Endpoints

### Authorization
The endpoints are protected by Basic Auth. If using Postman, you have to setup the credentials in the Authorization tab.  

user: admin
password: admin


Create a sensor -POST http://0.0.0.0:8000/api/sensor/
```json
{
    "serial_number": "1928463726",
    "name": "sensor 5",
    "location": "test location"
}
```

Create a heartbeat -POST http://0.0.0.0:8000/api/heartbeat/

```json
{
    "serial_number": "1928463726"
}
```

### List sensors

```bash
-GET http://0.0.0.0:8000/api/sensor/<int:serial_number>/
```

### List heartbeats
```bash
-GET http://0.0.0.0:8000/api/heartbeat/<int:heartbeat_id>/
```


# Limitations and possible improvements

For this application I focused on building a stable and manageable REST API. As such, the frontend could have been better designed, with some more dynamic features.

Some things I would've liked to add:
* The web app could display one card for each sensor that exists, such that we have the latest information for each. I probably would need to change to a different database that could support querying for this.
* The color of the cards could change depending on the latest time a heartbeat was received.
* Having the values on the cards refresh live, without having to actually click refresh.
* Validating for a matching sensor when we receive a new heartbeat.

# How to alert users about silent sensors

Build a watchdog function!
We can have a scheduled command that queries the database and matches the latest heartbeats with a given amount of time that would make them be considered "silent". I'm assuming that a sensor would send heartbeats at regular intervals, so it'd be trivial to see what we have missed. From this we could implement a smarter, self-learning, functionality if needed.