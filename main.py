from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch
from typing import Optional

# don't forget to change username and password before deployment
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "changeme")
)

app = FastAPI()

#returns a raw string that matches the hit of the query
@app.get("/search/")
async def search(query: Optional[str] = Query(None)):
    if not query:
        return {"error": "Query parameter 'query' is required."}

    try:
        # performs a search on the 'comment' field of wsb_comments
        # the term is then specified here: http://127.0.0.1:8000/search/?query=TERM
        # for nvidia == http://127.0.0.1:8000/search/?query=nvidia
        resp = es.search(index="wsb_comments", body={
            "query": {
                "match": {
                    "comment": query
                }
            }
        })

        hits = resp['hits']['total']['value']
        return {
            "message": f"Got {hits} hits",
            "results": resp['hits']['hits']
        }
    except Exception as e:
        return {"error": str(e)}
