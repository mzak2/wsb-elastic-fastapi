from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch
from typing import Optional, List

from classes.CommentData import CommentData

# don't forget to change username and password before deployment
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "changeme")
)

app = FastAPI()

#to run this, navigate to the root (wsb-elastc-fastapi) in terminal
# uvicorn main:app --reload
#returns a raw string that matches the hit of the query
@app.get("/search/")
async def search(query: str | str = "nvidia"): #this passes the required string or makes the default /search/?query=nvidia
#async def search(query: Optional[str] = Query(None)): #this defaults to an empty query /search/?query=None

    #this can be used to define the query within the function
    query = "msft"

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
        raw_results = resp['hits']['hits']

        #convert reults into the CommentData class
        #create a list containing them
        #return them to fastAPI in object form
        results: List[CommentData] = []
        for result in raw_results:
            source = result["_source"]
            comment_data = CommentData(
                username=source["username"],
                comment=source["comment"],
                date=source["date"]
            )
            results.append(comment_data)

        return {
            "message": f"Got {hits} hits",
            "results": [result.to_dict() for result in results]
        }
    except Exception as e:
        return {"error": str(e)}



