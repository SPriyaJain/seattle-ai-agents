# Install with pip install firecrawl-py
from typing import Any, List, Optional

from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field

app = FirecrawlApp(api_key="fc-ddbe096f8ab5484493ecb8d8b7c80674")


class NestedModel1(BaseModel):
    name: str
    wikipedia_link: str


class ExtractSchema(BaseModel):
    school_districts: list[NestedModel1]


data = app.extract(
    ["https://en.wikipedia.org/wiki/List_of_school_districts_in_Washington"],
    {
        "prompt": "Extract every school district's name and the link to their Wikipedia page from the provided list.",
        "schema": ExtractSchema.model_json_schema(),
        "enable_web_search": True,
    },
)

print(data)
