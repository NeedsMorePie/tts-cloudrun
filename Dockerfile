FROM python:3.8-slim

# Copy local code to the container image.
WORKDIR /app
COPY . .

# Download and install coqui TTS.
ADD https://github.com/coqui-ai/TTS/archive/refs/tags/v0.0.15.zip .
RUN ls -la
RUN \
    apt-get update -y; \
    apt-get upgrade -y; \
    apt-get dist-upgrade -y; \
    apt-get autoremove -y; \
    apt-get clean; \
    apt-get install -y unzip gcc build-essential; \
    unzip v0.0.15.zip; \
    rm -f v0.0.15.zip; \
    mv TTS-0.0.15 coqui_tts; \
    pip install -e ./coqui_tts

# Install production dependencies.
RUN pip install Flask gunicorn

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
