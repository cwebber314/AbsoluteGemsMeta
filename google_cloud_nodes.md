# Project documentation for AbsoluteGems 

## Google Cloud Functions

Notes:
- Each function is one endpoint.
- Each function must return a flask response.

I think this is a bad fit for an API with many entry points.

There are two ways to build the function:
- Online editor and container build.
- Build and test locally, then publish with gCloud API

A cloud function is associated with a Cloud Run Service. Some security
and permissions belong to the service in stead of the function

## Google App Engine

App Engine is a Platform-as-a-Service.
- Shuts down when not in use
- Scales up as needed

Can deploy from github repo.

## Google Compute Engine

Compute Engine is an Infrastructure-as-a-Service.
- You have to manage the VM. 
- It's always running

The Compute engine is like a VPS but has access to the VPC (Virutal Private Cloud) and
probably make sense if we with other google cloud service. There is a free tier of 
the compute engine for `e2-micro`

The compute engine is probably easier to get started on because it's just another 
box. The app engine uses a docker which is great once you get everything setup.

If you don't choose a container for the Compute Engine, it uses Debian 5.10

To get into the VM you can:
- SSH in from local machine
- SSH in from Google Cloud console 

The command from the local machine looks like:
```
gcloud compute ssh --zone "us-central1-a" "chipwebber@scratchbox-1" --project "beer-rest-api"
```

Note how we specify the username in the ssh command because it's different than the username
on our local box.


## Firewall - Compute Engine

Setup the firewall see [SO answer](https://stackoverflow.com/a/21068402).  There are two parts:
- Setup the firewall rule in VPC Network -> Firewall
- Add the network tag to the VM

Hints for firewall:
- Target Tags: `port-8000`
- Source Filter -> IP Ranges: `0.0.0.0/0`
- protocols and ports: `tcp:8000`

## scp - Compute Engine

To copy files to the remote machine
```
gcloud config set project corded-shadow-382501
gcloud compute scp *.mp4 chipwebber@scratchbox-1:~/test_videos
```

## ffmpeg - Compute Engine

To install ffmpeg on the VM:
```
sudo apt install ffmpeg
```

## Firebase

Use FireStore in Native mode.

## References

References:

- [React Hello World](https://codesandbox.io/s/react-mui-y191q)
- [Vue Hello World](https://codepen.io/cwebber314/pen/KKrpPgp)
- [Beer functions](https://console.cloud.google.com/functions/list?env=gen2&project=beer-rest-api&tab=trigger)