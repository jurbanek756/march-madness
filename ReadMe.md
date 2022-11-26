# March Madness

Methods for predicting March Madness winners!

Utilizes data scraping methods for obtaining team data, and uses various pieces of that data to make predictions.

Algorithm methods are a work in progress.

## Usage

### Save Static Data

Although all data is scraped from external sources that are currently publically available, it is possible that these sources will change or will be unavailable. Additionally, saving the data locally allows it to be validated before use, and prevents the need for successive external requests.

`save_static_data.py` collects and parses external data into pickle and json files. The content is the same, but the `json` allows the data to be easily read and validated.

### Run Predictions

A formalized method of running predictions has not been established, but the framework of a successful run is located 
in `run.py`, which uses the 2022 tournament rankings.

## Algorithm Ideas

* True random
* Weights accounting for AP Rank and Tournament Rank, with a certain level of stochasticity
* Positive sentiment from mascot 
* Superstition, ex. 12 over 5
* Colors
* Randomly select one of the selection methods 

## Backlog

* Expand prediction methods
* Backfill missing data
