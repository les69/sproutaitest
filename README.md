# Tech Test Readme

This document is intended mostly for running instructions rather than rationale behind
the solution. Please be adivsed that titles are unique in this solution, running a check with the same title twice
will cause a 500.
Also, there is no need to create the database as that will be created automatically for tests and locally for development
once running migrations.

## Bootstrap and run the services

The ingestion endpoint and the ml api endpoint are dockerized services, but need
a network to communicate between each other first. To setup the connection simply
run `make start-network` and a docker network will be created.
Afterwards, to run start the ingestion endpoint:
`make run-ingestion-endpoint`
and for the ML endpoint:
`make run-mlapi-endpoint`
Once this is done, to test the endpoint simply run the command as from instructions:

``curl -X 'POST' \ 'http://127.0.0.1:5000/posts/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \ -d '{
    "title": "This is an engaging title",
    "paragraphs": [
"This is the first paragraph. It contains two sentences.", "This is the second parapgraph. It contains two more sentences", "Third paraphraph here."
] }'``

The end result should be similar to: ```{"ingestion_status": "complete", "foul_content_found": false, "blog_post_id": 1}```,
where `ingestion_status` is a flag used to communicate the user if the ingestion went successful or something needs to be processed at a later time.
In this case, given both services are up, `complete` is the expected outcome. `foul_content_found` is another flag to show if any of the processed content
did contain any foul text, as the current implementation this should return false.

### Case with Foul text

Use this snippet to check against a piece of text with foul words (Sauron in this case):

```curl -X 'POST' 'http://127.0.0.1:5000/posts/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json'  -d '{"title": "This is another title","paragraphs": ["This is the first paragraph. It contains two sentences.", "This is the second parapgraph. It contains two more sentences", "Third paraphraph with sauron."] }'
```

Expected outcome:

```
{"ingestion_status": "complete", "foul_content_found": true, "blog_post_id": 2}
```

### Trying with the service down

You can now stop the MLendpoint using `docker stop mlendpoint` and run with another blog post:

```curl -X 'POST' 'http://127.0.0.1:5000/posts/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json'  -d '{"title": "This is en evil title","paragraphs": ["This is the first paragraph. It contains two sentences.", "This is the second parapgraph. It contains two more sentences", "Third paraphraph."] }'
```
The expected outcome here is:

```
{"ingestion_status": "incomplete", "foul_content_found": false, "blog_post_id": 3}                                                                                                                                                         
```
But once the api will be up and running again, `foul_content_found` will be updated to true because a foul word is in the title (`evil`).
There is an endpoint that allows the client to monitor the processing status for a blog post and can be checked using:
```curl -X 'GET' 'http://127.0.0.1:5000/posts/3 ``` and should return ```{"foul_content_found": false, "processing_status": "incomplete"}```.
If we restart the mlendpoint and wait 1/2 minutes, this should change to ```{"foul_content_found": true, "processing_status": "complete"}```


## Running the test suite

The project comes with a testing suite and can be validated by running ```make run-unit-tests```

## Local development

In order to run the backend, simply run ```
	python manage.py migrate && \
	python manage.py runserver 0.0.0.0:5000```