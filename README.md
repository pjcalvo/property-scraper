# property-scraper

To run the thing:

1. The `settings.yaml` file contains your search parameters.
2. Create a new python env: `python3 -m venv venv` then `. venv/bin/activate`.
3. Install the dependencies: `pip install -p requirements.txt`
4. Run the `./run.sh` file.
5. To run programatticaly just add watch: `watch -n 360 ./run.sh`

Thanks,

Notes:

_The first execution will create some results file which means that it will say that there are new properties._
_There are some bugs such as old properties show up as new from time to time_