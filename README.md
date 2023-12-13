# apiMLGFG

# Do the following instructions to run application

## 1- move on the main directory and create virtual environnement
cd apiMLGFG
python -m venv .env
source .env/bin/activate

## 2- install the required libraries
pip install -r requirements.txt

## 3- Dowload the file yolov4.weihts at this link :
https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

## 4- put that file in the folder apiML/api/

## 5- run the application :
python manage.py runserver

# The following are the path for use api

POST api1, login : api/login/
POST api2, register : api/register/
GET api4, product : api/product/<title>/
POST api5, image : api/image/
