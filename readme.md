Please watch the video made for this project in ZIP

-- Setup Redis, ElasticSearch-Kibana, Postgres, MongoDB

-- Create the table and DB in Postgres - DB details in ENV File
-- Create indexes in Postgres and DB

-- Create Index in Kibana for Log Ingestions

-- Install Requirements,

-- run Celery command : celery -A tasks worker --loglevel=info

-- run main.py command : uvicorn main:app --host 127.0.0.1 --port 3000 --reload --workers -1

-- go to localhost:3000/docs and utilize the apis for retrieving and ingestions

-- to access UI of ElasticSearch - Kibana, Go to discover, use your index to search and find ur logs