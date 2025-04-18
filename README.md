Thank you for this coding challenge. I thorougly enjoyed this!

This application comprises of three different docker containers:
- A postgres instance for data storage
- A scraper instance that pulls data from the internet, then provisions and populates the database
- A fastapi instance

All three of these can be created and run with:
docker compose up --build

There is also a suite of functional tests in their own folder. These can be run by going into the folder and running:
        `poetry install`
        `poetry run pytest`
    at the top level. 
Decisions are in DECISIONS.md
