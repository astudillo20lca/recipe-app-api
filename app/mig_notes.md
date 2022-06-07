# course notes

django models maps to a table in the database

makemigrations -- setups / updates database
migrate : run every time you.. start the application ?

setting custom models before migrations!




# command list

set of stepts that need to be done in the command line

```bash

# make migrations
docker-compose run --rm app sh -c "python manage.py makemigrations"
# remove default migrations if they were created before adding custom user. refresh database

docker volume rm recipe-app-api_dev-db-data
```
