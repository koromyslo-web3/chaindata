FROM python:3.11

# set work directory
WORKDIR /usr/app/src

# set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/koromyslo-web3/shared.git


# copy project
COPY . .

WORKDIR /usr/app

EXPOSE 8000

CMD ["python", "-m", "src"]
