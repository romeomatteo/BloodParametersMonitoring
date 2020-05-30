## BloodMonitoring

The code presented in this repository is used has is used to build a simple web dashboard in bokeh which shows the results of your AVIS blood exams throughout the time.
It consits of a:
1. Bokeh application
2. Web scraper to download the latest blood exam (configurable through the `config.json` file) 

The list of requirement in the [requirements.txt](requirements.txt). The suggestion is to install them in a new environments running 
```shell script
pip install -r requirements.txt
``` 

Before running the application, create a `config.json` with the following fields and place it in the home directory:

```json
{
  "avis_address": "avisnet login page (area-utente)",
  "username": "your username",
  "password": "your password",
  "gekoexecutable": "location of the geckodriver used by selenium with Firefox"
}
```

To run the scraper execute the python script [blook_exams_scraper.py](blood_exams_scraper.py)

To run the bokeh application, run in your console 

```shell script
bokeh serve --show main.py
```


