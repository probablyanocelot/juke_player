FROM library/postgres
ENV POSTGRES_USER test
ENV POSTGRES_PASSWORD test
ENV POSTGRES_DB dj
ENV FLASK_APP=app.py


FROM python:3.10.2
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Create, init venv:
# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

# Run the application:
CMD python app.py
