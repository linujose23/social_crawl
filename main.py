from fastapi import FastAPI
from social_data import Social_data_fetch
app = FastAPI()


@app.get("/facebook/post_id={post_id}")
def social_data(post_id):
    output = Social_data_fetch(post_id)
    return output
