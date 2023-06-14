# BeerMe

BeerMe is a Hello World project which uses lots of pieces of Google Cloud to make
a simple application:

- Compute Engine: Nodejs frontend, python backend, ffmpeg 
- Firewall rules for Compute Engine
- FireBase
- Service Account for FireBase access

Everything is published in the Google Cloud *nover* project.

## See it in action

The application should be running [here](http://34.170.230.194:8080/)

## Compute Engine

The frontend and the backend run on the `scratchbox-1` compute engine.

## Frontend

The Frontend provides the interface. It uses NodeJS to run the server. 

Resources:
- Github repo [cwebber314/beerme_frontend)](https://github.com/cwebber314/beerme_frontend)
- Hosted on `scratchbox-1` in `/home/chipwebber/beerme_frontend`

The frontend is based on this [pen](https://codepen.io/cwebber314/pen/KKrpPgp). Note that the application
uses a Vue Single File Component instead of separating js/css/html into three files.  

The CodePen is very close to the [BeerMe.vue](https://github.com/cwebber314/beerme_frontend/blob/main/src/pages/BeerMe.vue) file in the repo.

It uses Vue3 and the Quasar Framework:
- Why Vue? I haven't done anything with React yet.
- Why Quasar? I'd prefer to use the Vuetify component framework, but many of the feature are still experimental.
  Quasar feels more complete.

## Backend

Uses the github repo [cwebber314/beerme_backend)](https://github.com/cwebber314/beerme_backend)

See the [API docs](http://34.170.230.194:8000/docs)

Here's a [sample endpoint](http://34.170.230.194:8000/random-beer)

## FireBase

See the firestore database on [google cloud](https://console.cloud.google.com/firestore/databases/-default-/data/panel?authuser=0&hl=en&project=corded-shadow-382501) 

You can add entries to the `beers` entity and see them show up in the BeerMe test application.

We make a Service Account in Google Cloud that the backend uses to read/write the databse. 
I don't like to connect using my account (chipwebber@gmail.com) because it has permission to do
everything. It's better to run things with a non-privilidged account when possible.