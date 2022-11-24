# March Madness

Methods for predicting March Madness winners!

Utilizes data scraping methods for obtaining team data, and uses various pieces of that data to make predictions.

Algorithm methods are a work in progress.

## Usage

### Save Static Data

Although all data is scraped from external sources that are currently publically available, it is possible that these sources will change or will be unavailable. Additionally, saving the data locally allows it to be validated before use, and prevents the need for successive external requests.

`save_static_data.py` collects and parses external data into pickle and json files. The content is the same, but the `json` allows the data to be easily read and validated.

### Run Predictions

Data is still being collected and predictions are currently a work in progress.

## Algorithm Ideas

* True random
* Weights accounting for AP Rank and Tournament Rank, with a certain level of stochasticity
* Positive sentiment from mascot 
* Superstition, ex. 12 over 5
* Colors
* Randomly select one of the selection methods 

## Backlog

* Get city info
* Backfill missing colors
* Finish Rivals table
* Work on prediction methods
