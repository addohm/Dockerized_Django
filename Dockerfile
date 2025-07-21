FROM python:3.13.1-alpine3.21

# Set the project port to run on
ENV APP_PORT=8000

# Prevents django from writing unnecessary files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Set an environment variable to unbuffer Python output, aiding in logging and debugging
ENV PYTHONBUFFERED=1

# Make the home directory if it does not exist, create the user, and assign ownership to that user
RUN addgroup -S django && \
    adduser -h /project -S django -G django && \
    install -d -m 0765 -o django -g django /project \
    install -d -m 0765 -o django -g django /project/media \
    install -d -m 0765 -o django -g django /project/staticfiles

# Update apk and install psycopg2 and pillow dependencies
RUN apk update
RUN apk add postgresql-dev zlib-dev jpeg-dev

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN pip install --no-cache-dir --root-user-action ignore --upgrade pip

# Check for python3 and pip installation and output version
RUN python3 --version
RUN pip --version

# Set the working directory within the container to /project for any subsequent commands
WORKDIR /project

# Copy the entire current directory contents into the container at /project
COPY --chown=django:django . .

# Give the entrypoint script executable permissions
RUN chmod +x entrypoint.sh

# Install dependencies from the requirements.txt file to ensure our Python environment is>
RUN pip install --no-cache-dir --root-user-action ignore -r requirements.txt

# Inform Docker that the container listens on the specified network port at runtime
EXPOSE ${APP_PORT}

# Create the staticfiles and media directories, output the project directory list for good measure
RUN ls -lda /project/*

# Start the application using gunicorn
ENTRYPOINT [ "/project/entrypoint.sh" ]

# Used to hold container open for troubleshooting 
# CMD ping -i 5.0 127.0.0.1