FROM petronetto/pytorch-alpine

# Update the Python path
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Setup the code
COPY . /code
WORKDIR /code