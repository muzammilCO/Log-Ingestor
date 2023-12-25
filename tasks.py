from celery import Celery
from celery.signals import worker_process_init
import asyncio
import json
import pickle5 as pickle
from elasticsearch import Elasticsearch
from fastapi import Depends, HTTPException
from session import get_db, SessionLocal
from sqlalchemy.orm import Session
from models import MyLogData
from datetime import datetime
from session import collection

es = Elasticsearch(['http://localhost:9200'], timeout=20)
print(es.ping())
index_name = "log_ingestor"
es.indices.create(index=index_name, ignore=400) 

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@celery.task
def process_log(log):
    # Simulate processing delay
    asyncio.sleep(0.1)
    # Log processing logic (replace with your actual processing logic)
    print('Processed log:', log)

    # Simulate writing to a database or file
    write_to_database(log)

@celery.task
def write_to_database(log):
    # Simulate database write delay
    db = SessionLocal()
    asyncio.sleep(0.05)
    print(log)
    
    print("Here writing file")
    document_data = log

    # Append log to a  file (replace with your actual database write logic)
    
    with open('/Users/muzzmilds/Desktop/Log ingestor/logs.txt', 'a') as file:
        data = MyLogData(level=log["level"],
            message=log["message"],
            resourceid=log["resourceId"],
            timestamp=log["timestamp"],
            traceid=log["traceId"],
            spanid=log["spanId"],
            commit=log["commit"],
            metadata_parentresourceid=log["metadata"]["parentResourceId"]
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        response = es.index(index=index_name, body=document_data)
        if response['result'] == 'created':
            print(f"Document indexed successfully with _id: {response['_id']}")
        else:
            print(f"Failed to index document: {response}")
        collection.insert_one(log)
        file.write(str(log) + '\n')
    db.close()

@worker_process_init.connect
def configure_workers(sender=None, **kwargs):
    # Set the autoscaler based on the length of the task queue
    sender.control.autoscaler = 'celery.worker.autoscale:Autoscaler'

if __name__ == '__main__':
    celery.start(argv=['celery', 'worker', '-l', 'info'])
