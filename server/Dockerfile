FROM python:3.11.3-slim-buster

# Install Yarn and Node
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn

WORKDIR /lewdlocale

COPY . .
RUN ls /lewdlocale/gui

RUN cd gui && yarn install && \
    yarn build

# Install Python dependencies
RUN pip install poetry==1.3.2 && \
    poetry install

# Build the React app

# Move the build files to the server directory
RUN mkdir -p /lewdlocale/server/build && \
    mv /lewdlocale/gui/build/* /lewdlocale/server/build/

WORKDIR /lewdlocale
# Set the entrypoint
ENTRYPOINT ["poetry", "run", "python", "launch.py", "--app", "server", "--flush", "False", "--log-level", "INFO"]