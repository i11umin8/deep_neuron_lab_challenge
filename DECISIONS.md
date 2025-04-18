Decisions:
1. Simplicity First
    This application has a relatively simple purpose. In abstract:
        * Pull a relatively small set of data from the internet
        * Make the data available via API
    Because of this, I omitted many of my original ideas which would be used in a real-world distributed system but
    would not give any functional or performance benefits here. These include:
        * A pub/sub model to inform the API when the data is updated
        * An in-memory cache to speed up querying
        * A job runner to regularly pull the data

2. Prioritize what matters
    My time got reduced due to a minor but unexpected emergency. All stated requirements were met, but because of time limitations, some desired additions were left out. These include:
        * linting, formatting, type hinting tools hooked up to git commit
        * Code cleanup/refactoring
        * unit tests for each relevant function

    To make up for this, a set of functional tests was added to verify that the API behaves as expected. These are located in the functional_tests folder. To run them, start the service, cd into the functional_test folder, and run:
        `poetry run pytest test_api_functional.py`
    