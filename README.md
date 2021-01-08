# COVID-19 Mobility Dashboard

--

## Datasets

Given the large file size of the datasets, they are not able to be uploaded to this repo. I've included links to them to download the datasets to run the regression analysis.

[COVID-19 cases dataset](https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv): provided by the *New York Times*

[Mobility dataset](https://data.bts.gov/Research-and-Statistics/Trips-by-Distance/w96p-f2qv): tracks the number and distance of the trips that people take in each U.S. county; provided by the Department of Transportation

--

## Regression Analysis

The regression analysis code is in file `regression_analysis.ipynb`. The file is a Python Notebook that cleans and analyzes the COVID-19 cases dataset and the mobility dataset.

--

## Data Visualization Dashboard

The data visualization dashboard application is in file `dashboard.py`. It calls on dataset files in the `data/` folder and the CSS stylesheet in `assets/`. To run the application, type into command line:

```
python dashboard.py
```
Then, type [http://127.0.0.1:8050/](http://127.0.0.1:8050/) into your web browser.