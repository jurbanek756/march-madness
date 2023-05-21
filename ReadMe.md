# March Madness

Methods for predicting March Madness winners!

Utilizes data scraping methods for obtaining team data, and uses various pieces of that data to make predictions.

## Usage

### Database Generation

Data is scraped from external sources that are currently publicly available and are stored in:

* db/2022_2023_games.pkl - Games from the 2022-2023 season
* db/school_data.pkl - Static data on schools in the tournament

Run `generate_db_data.py` to create these files.

### Run Predictions

Predictions can be run for the 2023 March Madness tournament by executing the `run.py` script.

`prediction_method` on line 60 can be replaced with any function in `predict.select_team`, with 
`weighted_random_selection` being used by default in the `run.py` script.

## Future Work

This project is being actively worked and improved. See the GitHub [Projects](https://github.com/AGnias47/march-madness/projects?query=is%3Aopen) tab for details.
