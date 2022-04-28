# Contact Manager

Contact Manager is an web application that enables users to manage contacts.
Users of Contact Manager can easily extract information from business card by simply uploading an image of business card.
Saved images can be retrived by inputting part of name of the contact.

This package uses AI capabilities of AWS services as follows.

- Text detection: AWS Rekognition
- Entity recognition: Amazon Comprehend / Amazon Comprehend Medical

## Interaction Diagram

## Requirements

- Python 3.8
- pipenv

## Getting the development environment up and running

### Installing pipenv

This repo uses pipenv as its package manager. To install:

    pip install pipenv

It is also important to make sure Python 3.8 is installed.

### Installing dependencies

From the base directory:

    make deps

### Linting

From the base directory:

    make lint

This will automatically try to lint the code. Some manual changes may also be needed.

### To install new packages

From the base directory:

    pipenv install PACKAGE_NAME

### Test on local

- Environment varialbe setup

  - Copy ".env.defaults" file and change its name to ".env".
  - Set environment variables with your database host, name and credential.

- Pipenv virtual environment activation

  - To activate the virtual environment, from the base directory:

    pipenv shell

- Run lambda_function python file

  - /src and run lambda_function.py.

    python3 lambda_function.py

## Deployement

This package is designed to run on AWS lambda service.
For deployment, a .zip file archive is used which includes application code and its dependencies.
The following steps guide you the way to deploy this package to production.

### Build

From the base directory:

    make build

It copies all source code and dependencies to /deploy folder.
Then it generates engagement_count_report.zip which can then be uploaded to the engagment_count_report lambda function.
