FROM python:3.11.3-slim-buster
WORKDIR /lewdlocale

COPY . .

RUN pip install poetry==1.3.2

RUN poetry install

# ffmpeg

RUN apt-get update && apt-get install -y ffmpeg

# remove lists
RUN rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["poetry", "run", "python", "launch.py", "--app", "downloader", "--flush", "False", "--log-level", "INFO"]
