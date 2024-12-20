from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from elasticsearch import Elasticsearch
from typing import List
from classes.CommentData import CommentData

# don't forget to change username and password before deployment
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "changeme")
)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

#to run this, navigate to the root (wsb-elastc-fastapi) in terminal
# uvicorn main:app --reload
#returns a raw string that matches the hit of the query
@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def search(request: Request, query: str = Form("nvidia")): #will default to "nvidia" on page load
    results: List[CommentData] = []

    if query:
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

            raw_results = resp['hits']['hits']

            # convert reults into the CommentData class
            # create a list containing them
            # return them to fastAPI in object form
            for result in raw_results:
                source = result["_source"]
                results.append(CommentData(
                    username=source["username"], #split at the "• 16h ago •" in the future to remove it
                    comment=source["comment"],
                    date=source["date"]
                ))
        except Exception as e:
            return templates.TemplateResponse("table.html", {
                "request": request,
                "results": [],
                "error": str(e)
            })
    #for debugging
    #print(f"Query: {query}")
    #print(f"Results: {results}")

    return templates.TemplateResponse("table.html", {
        "request": request,
        "results": results,
        "query": query
    })

