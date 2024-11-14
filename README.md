## **SampleShare**
SampleShare is an audio sample sharing social media web application in development. 

## **What is it?**
SampleShare is a web application that uses Pythons famous open-source Django web framework, MySQL for its backend database, and Docker for containerizing the project for easy deployement. 

## Prerequisites

Before setting up the project, make sure you have the following installed on your respective system:

- **Python 3.x**: Required to run Django and install dependencies.
- **Docker**: Used to containerize the web server and database.

### Installing Python
To install Python, visit the [official Python website](https://www.python.org/downloads/) and download the latest version for your operating system.

### Installing Docker
Follow the instructions on the [Docker website](https://docs.docker.com/get-docker/) to install Docker.

## **Installation**
To install the project follow these steps.

1. In your chosen directory clone the project.
```
git clone git@github.com:SampleShare/SampleShare.git
```
2. Go in to the project directory 
```
cd SampleShare
```
3. The project needs a .env file for correctly setting up the containers to run the web application and database. Run the create_en.py file auto generate one for you.
```
python3 create_env.py
```
>[!WARNING]
>This project is not ready for production so the auto generated .env file should not be used when deploying the project for production as it is just a baseline to get the project installed and running. Remember to alway read the contents of any script before running them blindly.
