#### Eurygaster spp. classification application

* The project is based on [streamlit](https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py) deployment
  python library.
* Application is available for [Heroku](https://www.heroku.com/) and Docker deployment.
* Link to the Heroku demo: [eurygaster-app](https://eurygaster-app.herokuapp.com/).

![eurygaster_integriceps_example](./assets/e_integriceps_example.png)


#### Setting up with Docker, Docker-compose:

```bash
# Create container with Dockerfile
$ docker build -t eurygaster_app:latest .
# Create subnet for application, set static ip and run the app
$ docker network create --subnet=172.55.0.0/29 eurygaster_subnet
$ docker run --net eurygaster_subnet \
             --ip 172.55.0.2 -p 8051:8051 --rm -t -d \
             -v /home/${USER}/eurygaster_uploads:/app/uploads \
             --name eurygaster_app eurygaster_app:latest

# Create container with Docker-compose. It automatically creates volume and mount image uploads to it.
# Assume, that we have /home/${USER}/eurygaster_uploads directory
$ mkdir /home/${USER}/eurygaster_uploads
$ docker-compose up
# Now, all the images uploaded to application for inference can be seen in <FOLDER> 
# To change mounting volume, create your custom directory and set it in <MOUNTING_VOLUME> parameter in .env.
# .env also stores: SUBNET, GATEWAY, application IP


```