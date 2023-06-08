# March Madness

Methods for selecting March Madness winners.

Utilizes data scraping methods for obtaining team data, and uses various pieces of that data to either make predictions or aid in evaluating each matchup.

## Usage

### Database Generation

Data is scraped from external sources that are currently publicly available and are stored in:

* db/2022_2023_games.pkl - Games from the 2022-2023 season
* db/school_data.pkl - Static data on schools in the tournament

Run `generate_db_data.py` to create these files.

### Run Predictions / Evaluations

A prediction method is defined as any automated method for generating a March Madness bracket. An evaluation method is a manual process, where the method simply aids the user in manually generating a March Madness bracket.

Predictions or evaluations can be run for the 2023 March Madness tournament by executing the `run.py` script.

The desired prediction or evaluation method should be selected from the available functions in either  `predict.select_team` or `evaluate.select_team`. By default, the `user_evaluation` function in `evaulate.select_team` is used, which aids a user in selecting matchup winners by providing relevant information via a terminal.

## Future Work

This project is being actively worked and improved. See the GitHub [Projects](https://github.com/AGnias47/march-madness/projects?query=is%3Aopen) tab for details.
