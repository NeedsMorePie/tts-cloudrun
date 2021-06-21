# TTS Cloudrun

## Development

### Requirements

* Python 3.8

### Installation on cloud shell

Run `bash install_py38.sh` to install python under `$HOME/.pyenv/versions/3.8.0/bin/python3.8`.

### Repository setup

Download coqui_tts:

```
wget https://github.com/coqui-ai/TTS/archive/refs/tags/v0.0.15.zip
unzip v0.0.15.zip
rm -f v0.0.15.zip
mv TTS-0.0.15 coqui_tts
```

Install coqui_tts:

```
python3.8 -m venv env
source env/bin/activate
pip install -e ./coqui_tts
```

### Run

```
source env/bin/activate
PORT=8080
gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
```

## Docker

NOTE: See https://codelabs.developers.google.com/codelabs/cloud-run-hello-python3#4 for details.

Set environment variables:

```
PROJECT_ID=$(gcloud config get-value project)
DOCKER_IMG="gcr.io/$PROJECT_ID/tts-cloudrun"
```

### Build

```
gcloud builds submit --tag $DOCKER_IMG --timeout=1800
```

### Run locally

```
docker pull $DOCKER_IMG
docker run -p 8080:8080 $DOCKER_IMG
```

### Deploy

```
REGION="us-central1"
gcloud run deploy tts-cloudrun \
  --image $DOCKER_IMG \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated
SERVICE_URL=$( \
  gcloud run services describe tts-cloudrun \
  --platform managed \
  --region $REGION \
  --format "value(status.url)" \
)
echo $SERVICE_URL
```

### Cleanup

```
REGION="us-central1"
gcloud container images delete $DOCKER_IMG
gcloud run services delete tts-cloudrun \
  --platform managed \
  --region $REGION
```
