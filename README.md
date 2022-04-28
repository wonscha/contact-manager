# Contact Manager

Contact Manager is an web application that enables users to manage contacts.
Users of Contact Manager can easily extract information from business card by simply uploading an image of business card.
Saved images can be retrived by inputting part of name of the contact.

![demo gif](https://github.com/wonscha/contact-manager/blob/main/docs/demo.gif)

This package uses AI capabilities of AWS services as follows.

- Text detection: Amazon Rekognition
- Entity recognition: Amazon Comprehend / Amazon Comprehend Medical

It also uses AWS storage and database services.

- Storage: Amazon S3
- Database: Amazon Dynamodb

## Interaction Diagrams

### User story 1 - Extract

![user story 1](https://github.com/wonscha/contact-manager/blob/main/docs/screenshot_extract.png)

### User story 2 - Save

![user story 2](https://github.com/wonscha/contact-manager/blob/main/docs/screenshot_save.png)

### User stroy 3 - Search by name

![user story 3](https://github.com/wonscha/contact-manager/blob/main/docs/screenshot_search.png)

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

### Development environment setup

- Environment varialbe setup

  - Copy ".env.defaults" file and change its name to ".env".
  - Set environment variables with your database host, name and credential.

    - ACCESS_KEY: AWS Access Key ID
    - SECRET_KEY: AWS Secret Access Key
    - S3_BUCKET: AWS S3 bucket name
    - DB_TABLE: AWS Dynamodb table name
    - REGION_NAME: AWS region name

- Dependency setup

  - To install dependencies on pipenv virtual environment:

  ```sh
  make deps
  ```

- Pipenv virtual environment activation

  - To activate the virtual environment, from the base directory:

  ```sh
  make env
  ```

- Run development server

  - To run development server:

  ```sh
  make dev-server
  ```

- Run user interface

  - To run user interface:

  ```sh
  make dev-front
  ```
