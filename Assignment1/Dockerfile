FROM python:3-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

COPY *.py ./
COPY config ./
COPY credentials ./
COPY setup.sh ./

# Install app requirements
RUN pip install -r requirements.txt

EXPOSE 80 81


ENTRYPOINT [ "python" ]

# RUN python main.py

CMD [ "main.py" ]