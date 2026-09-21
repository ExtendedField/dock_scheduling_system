User Manual

- configure db password with an .env file
- confiugre where you want to store your .xlsx

Step 1: Populate sqllitedb with excel data

- `uv run setupdb`

Step 2: start backend

- `cd src/backend`
- `uv run fastapi dev`

Step 3: create OpenAPI client: (do this in project root dir)

- `curl http://localhost:8000/openapi.json -o openapi.json`

Step 4: start frontend

- `cd frontened`
- `yarn generate client`
- `yarn dev`
