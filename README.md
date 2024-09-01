# SmartStock

## Description
SmartStock is a Django-based web application developed as part of the application process for the Junior Software Developer role at Software House Solution. The application provides functionalities for managing stock items, processing sales, and generating PDF reports of sales.
## Features
Add Items to Stock: Users can add new items to the inventory.</br>
Sell Items from Stock: Users can process sales by removing items from stock.</br>
Manage Shopping Cart: View and manage items in a shopping cart.</br>
Generate PDF Reports: Generate PDF reports of sales transactions.</br>
  ## Prerequisites
- Python 3.x
- PostgreSQL
- Git

## Create virtual Environment
```
python -m venv venv
```
## Activate the virtual environment:
```
venv\Scripts\activate
```

## Installation
To install the project dependencies, run the following command:

```
pip install -r requirements.txt
```

This command will install all the necessary packages listed in the `requirements.txt` file.

## Ensure a PostgreSQL database named SmartStock is created, or update the database name in the settings.py file.

## make migrate to ensure your models is added to database

```
python manage.py migrate
```
#finally to run project 
```
python manage.py runserver
```

