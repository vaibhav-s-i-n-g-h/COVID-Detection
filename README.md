# COVID Detection using Chest X-Ray Images

The coronavirus COVID-19 pandemic is the defining global health crisis of our time and the greatest challenge we have faced since World War Two. Since its emergence in Asia late last year, the virus has spread to every continent except Antarctica.

There has been a lot of discussion on inadequate testing kits and late results. People are not not admitted to the hospital without being tested COVID positive. Thus, leading to many unfortunate deaths.

In this project we have attempted to tackle this very problem. Providing a fast and reliable COVID detection at a very cheap cost. 

Getting an X-Ray done is very easy and cheap in India. We provide a platform where the user can get the probability of having COVID19 or Pneumonia by just uploading his/her Chest X-Ray.

This project uses X-Ray images and trained Deep Neural Network Model to classify image as:

- Normal vs Pneumonia
- Covid vs Pneumonia

## Tech Stack
- Django Framework
- Python
- PostgreSQL

For training model following dataset is used:

We Collected total 757 X-ray images of corona  patients from the following Sources-
1. https://github.com/ml-workgroup/covid-19-image-repository
2. https://github.com/armiro/COVID-CXNet/tree/master/chest_xray_images/covid19

We Collected 3000 X-ray Images of healthy Persons and 3000 X-ray Images of Pneumonic patients:

https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia

## Description
The MVT Framework, that Django provides, is used to build the website. The following files inside the 
- settings.py contains all the configurations such as for database and media paths.
- urls.py contains all the routes and connects templates with the views in MVT framework.
- models.py contains the desciption of tables in the database. We used in-built user table in postgresSQL for storing user credentials.
- views.py contains the functions for logging in, registering, database handling etc.
- image.py contains the scripts to run the deep learing model on the uploaded image.
- model.h5 is the trained model for pneumonia vs normal chest x-rays.
- model_2.h5 is the trained model for covid vs pneumonia chest x-rays.
- The images folder stores all the input and ouput images user wise.
## Running the Application

1. Setup PostgreSQL on your System.
2. Install Django.
    > `python -m pip install Django`

3. Create a directory to workin. Open Command Prompt in the directory and the run the command below:
    > `django-admin startproject project_name`
4. Inside the 'project_name' directory, in settings.py setup your database.
5. Install the libraries in requirements.txt
    > `pip install -r requirements.txt `

6. Your are all setup. Just run the following command inside on Command Prompt and run the command below:
    >`python .\manage.py runserver`

Follow the link for the development server.