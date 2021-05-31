# WeatherDashboard
A browser-based weather dashboard (Python + Django + Dash + Plotly + React JS)

Parsing data from CSV files and visualizing on a (web)browser-based UI 

## Dashboard preview

![WeatherDashboard](https://user-images.githubusercontent.com/20065946/119750469-4e696f00-be91-11eb-95e2-fd438d6578f8.JPG)


## Installation Instructions

1. Create a virtual env

2. Check if you have a virtual env virtualenv --version
(Not Installed) Dont see a version number? run sudo pip install virtualenv
(Installed) Make a folder within the highest file of the project mkdir ~/env
3. run virtualenv ~/env/my_new_app
4. cd into the bin folder cd ~/env/my_new_app/bin
5. activate the env source activate
6. pip install -r requirements.txt


`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`


## Useful Links
[Dash Bootstrap](https://dash-bootstrap-components.opensource.faculty.ai/)
[Plotly](https://plotly.com/python/)
