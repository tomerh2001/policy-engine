FROM python

# Add current directory
ADD . .

# Set enviorment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Install project dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pipenv install --skip-lock --system --dev

CMD python manage.py runserver