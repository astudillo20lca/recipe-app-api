FROM python:3.9-alpine3.13
LABEL maintainer="Miguel"

# display the output in the terminal
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# create virtual environment, upgrade pip, install req.
# remove unnecesary files (keep it light) and add a user
# it is good practice not to use the root user, as if
# the apps get compromised they will have full access to the container

# by default we dont run in development mode
ARG DEV=false
# better to run it in a single command to avoid the creation
# of unnecessary docker image layers. (more efficient)
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # install postgres client (dependencies)
    apk add --update --no-cache postgresql-client && \
    # virtual dependency package
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true"]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    # remove the build packages needed for postgres.
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# update the ENV variable, to not specify the full path
ENV PATH="/py/bin:$PATH"

USER django-user
