from fastapi import FastAPI, HTTPException
from tasks import process_log
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from crud import *
from fastapi.responses import JSONResponse
from bson import json_util
from bson import ObjectId
import json
from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Log Ingestor",
        version="0.0.0",
        description="",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

@app.post("/ingest")
async def ingest_log(log: dict):
    try:
        # Send log processing task to Celery worker
        process_log.apply_async(args=[log])
        return {"message": "Log ingested successfully. Processing in the background."}
    except Exception as e:
        print(f"Error ingesting log: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/retrieve-data")
def retreive_logs(level: str = None, message: str = None, timestamp: str = None, resourceid: str = None, traceid: str = None, spanid: str = None, commit: str = None, metadata_parentresourceid:str = None):
    try:
        if level is None and message is None and timestamp is None and resourceid is None and traceid is None and spanid is None and commit is None and metadata_parentresourceid is None:
            return "No data Provided"
        
        if timestamp is None and commit is None:
            # go with the Mongo
            subset_fields = {}
            if level is not None:
                subset_fields['level'] = level
            if resourceid is not None:
                subset_fields['resourceId'] = resourceid
            if message is not None:
                subset_fields['message'] = message
            if traceid is not None:
                subset_fields['traceId'] = traceid
            if spanid is not None:
                subset_fields['spanId'] = spanid
            if metadata_parentresourceid is not None:
                subset_fields['metadata_ParentResourceId'] = metadata_parentresourceid
                
            result = mongo_search(subset_fields)
            print(result)
            final_result = []
            for i in result:
                del i["_id"]
                final_result.append(i)
            return final_result
            # return " Cchecking"
        else:
            subset_fields = {'level': level, 'resourceid': resourceid, 'message': message, 'timestamp':timestamp,
                        'traceid': traceid, 'spanid': spanid, 'commit': commit,
                        'metadata_parentresourceid': metadata_parentresourceid}
            return query_logs(subset_fields)
    except Exception as e:
        print(f"Error retrieving log: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
