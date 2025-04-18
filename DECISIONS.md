Decisions:
1. Simplicity First

    - This application has a relatively simple purpose. In abstract:
        * Pull a relatively small set of data from the internet
        * Make the data available via API
    - Because of this, I omitted many of my original ideas which would be used in a real-world distributed system but
    would not give any functional or performance benefits here. These include:
        * A pub/sub model to inform the API when the data is updated
        * An in-memory cache to speed up querying
        * A job runner to regularly pull the data

2. Prioritize what matters:

    - My time got reduced due to a minor but unexpected emergency. All stated requirements were met, but because of time limitations, some desired additions were left out. These include:
        * linting, formatting, type hinting tools hooked up to git commit
        * Code cleanup/refactoring
        * A comprehensive unit testing suite (some exist, but many more are necessary)

    - To run the tests, run poetry install at the top level directory and then:
        `poetry run pytest`
    
3. Isolation:
    - Each container is as independent from the others as possible. Because of this, they have their own files for poetry.
    - However, for the sake of a convenient test suite, an addition set of poetry files were added at the root. 
    - In order for the functional tests to pass, the service must be active.