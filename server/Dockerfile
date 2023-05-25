FROM python:3.11.3-slim-buster

# Install Yarn and Node
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn

WORKDIR /lewdlocale

COPY . .

# Install Python dependencies
RUN pip install poetry==1.3.2 && \
    poetry install

# Build the React app
WORKDIR /lewdlocale/gui
RUN yarn install && \
    yarn build

# Move the build files to the server directory
RUN mkdir -p /lewdlocale/server/build && \
    mv /lewdlocale/gui/build/* /lewdlocale/server/build/

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "python", "launch.py", "--app", "server", "--flush", "False", "--log-level", "INFO"]