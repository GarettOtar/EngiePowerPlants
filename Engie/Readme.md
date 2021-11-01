Welcome to this new test for Engie

After downloading the archive make sure that docker-compose feature are avaible.
In order to do so, you can run the command:
>docker-compose run web django-admin startproject Engie .

After that, you will only need to let the docker-compose.yml work.
>docker-compose up

By default, the internal port is set on port 8000 but docker-compose make it work on port 8888 on localhost.

You retrive the API on localhost:8888 and add /productionplan to access to a view that allow only post request.