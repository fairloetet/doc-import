# doc-import

Extract information and metadata from PDF sources. Later, the tool will automatically import them into a database via a
REST API.

## Requirements

- Python 3.8+
- At the moment, Linux systems are supported, but MacOS and Windows might work, too

## Get Started

To get started developing the tool on Linux (MacOS should work, too), run the included setup script:

```bash
$ ./setup.sh
```

This will download and install the required dependencies, including the Python dependency manager
[Poetry](https://python-poetry.org/), all required libraries, and the [spaCy](https://spacy.io) model for English,
which is used to process the documents.

## Quellen

- https://developer.wordpress.org/rest-api/
- https://pods.io/docs/build/extending-core-wordpress-rest-api-routes-with-pods/
- https://www.arelthiaphillips.com/access-pods-custom-post-types-using-wp-rest-api/
