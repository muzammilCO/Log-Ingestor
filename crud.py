from session import SessionLocal
from models import MyLogData as LogEntry
from session import collection


def query_logs(subset_fields):
    with SessionLocal() as session:
        # Build the query dynamically based on the subset_fields
        query = session.query(LogEntry)
        for field, value in subset_fields.items():
            if value is None:
                continue
            query = query.filter(getattr(LogEntry, field) == value)

        # Execute the query and return the results
        result = query.all()
        return result
    
def mongo_search(subset_fields):
    result = collection.find(subset_fields)
    result = list(result) 
    return result