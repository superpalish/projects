## Plates API

- simple API to list, add, update, remove car number plates with their owner names

#### Launch
	
1. Docker
	+ Clone project repository
	+ Install docker and docker-compose
	+ Navigate to project root and start deployment: 
	  + docker-compose up
	+ or provide path to docker-compose.yml:
	  + docker-compose -f /path_to/docker-compose.yml up
    + Navigate to http://localhost:8085/admin/ in your browser
    + User: admin, password: plates

2. Manual (Ubuntu, Debian)
	+ Installation ( development )
	  + Clone project repository
	  + Install project requirements.apt (found in docs directory)
	  + Create virtual environment:
	  + follow instructions https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
      + Install project requirements.pip
	  + Create database using create_db.sh
	  + Activate virtual environment
	  + Make migrations:
	    + python manage.py migrate 
	  + Create super user for admin:
	    + python manage.py createsuperuser
	  + Start development server:
	    + python manage.py runserver
	  + Start celery:
	    + celery -A plates worker --loglevel=info 
	  + Navigate to http://localhost:8000/admin/ in your browser

#### API examples

##### list request
curl -X GET http://localhost/api/v1/plates/?format=json
##### create request
curl -X POST -H "Content-Type: application/json" -d @plates.json http://localhost/api/v1/plates/
##### delete request
curl -X DELETE http://localhost/api/v1/plates/3/
##### update request
curl -X PATCH -H "Content-Type: application/json" -d @update.json http://localhost/api/v1/plates/5/

#### Run tests
##### docker
docker exec -it plates-app python /plates/plates-project/manage.py test plates_app.tests
##### development
python manage.py test plates_app.tests

    