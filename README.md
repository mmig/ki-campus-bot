### Version 3.0

# DFKI:

## Usage

Change to 'for local development' endpoint in endpoints.yml

### Usage alternative

In folder with the chatbot

```sh
    rasa shell
```
___________________
# KI-Campus Chatbot

## Training of the Model 

Choose the folder with the chatbot in English (KI-Campus_en) or in German (KI-Campus_de)

```sh
    rasa train
```

## Usage

### Start the Rasa Server

```sh
    rasa run --enable-api
```

### Start the Action Server

```sh
    cd actions/
    rasa run actions
```

## Docker

In the outer project structure run:

### Docker Compose (de)

```sh
    docker-compose -f docker-compose_de.yml -p kicampus_de up --build
```

### Docker Compose (en)

```sh
    docker-compose -f docker-compose_en.yml -p kicampus_en up --build
```
