# How to setup the pipeline
## Prerequisites
I provided the version of apps I used. Different version might impact the compatibilities
```
Docker (version 27.3.1, build ce12230) & docker-compose (version 1.25.0, build unknown)
Poetry (version 1.8.5)
Python (version 3.12) (most likely doesn't impact because it's containerized)
Debian based OS (Ubuntu 20.04 WSL)
```

## Prerun
- Start the docker daemon (WSL sometimes doesn’t run the daemon at the startup)
```
sudo dockerd &
```

- Build the image for spark using predefined make command:
```
make build 
```

- Test the image build by starting the docker-compose
```
make run 
```
- Put the extracted YELP json dataset under `yelp_dataset/`

- To upload CSV into GCS and create external table, credential json is needed. Put it under `creds/`. Change the container env var to point into your json file in the `docker-compose.yaml`
```
    # Update this
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/opt/creds/<your-json-filename>
```

## Run the pipeline
Use the predefined make command to run the tasks. All the parameters are also predefinedvthere. 
There are 3 separate functions:
- To convert the JSON under `yelp_dataset` into CSV and put it in the same folder
```
make convert
```
- To upload the CSV under `yelp_dataset` into GCS 
```
make upload
```
- To create Bigquery external tables from upload CSV in GCS
```
make generate
```

The command will create containers which would act executor. 
Except for task number 1, the result is stored in GCP project `dana-quality-test`
**(Please inform ersachris@gmail.com if you want to be granted access there)**
