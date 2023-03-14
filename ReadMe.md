# March Madness

Methods for predicting March Madness winners!

Utilizes data scraping methods for obtaining team data, and uses various pieces of that data to make predictions.

## Usage

### Database Generation

Data is scraped from external sources that are currently publicly available, and is stored in `db/school_data.json` as 
a local database.

Run `generate_db.py` to create the `db/school_data.json` file.


### Run Predictions

Predictions can be run for the 2023 March Madness tournament by executing the `run.py` script.

`prediction_method` on line 60 can be replaced with any function in `predict.select_team`, with 
`weighted_random_selection` being used by default.

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
