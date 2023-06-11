# March Madness

Terminal-based scripts for selecting March Madness Winners!

The script can serve two purposes:

* Guide users through selecting a March Madness bracket, providing relevant information throughout the process
* Automatically select a March Madness bracket through various prediction methods.

By default, the repo is set to guide the user through manually picking teams. This is done by running the following commands:

```shell
./generate_db_data.py
./run.py
open NCAA_Tournament_Results.log
```

## Usage

### Database Generation

Data is scraped from external sources that are currently publicly available and are stored in:

* db/2022_2023_games.pkl - Games from the 2022-2023 season
* db/school_data.pkl - Static data on schools in the tournament

Run `generate_db_data.py` to create these files.

### Run Predictions / Evaluations

User-guided methods are defined as evaluation methods, and automated methods are defined as prediction method. Predictions or evaluations can be run for the 2023 March Madness tournament by executing the `run.py` script.

The desired prediction or evaluation method should be selected from the available functions in either  `predict.select_team` or `evaluate.select_team`. By default, the `user_evaluation` function in `evaulate.select_team` is used, which aids a user in selecting matchup winners by providing relevant information via a terminal.

### Results

Results are stored in `NCAA_Tournament_Results.log`. The file is always appended to, so should be removed between subsequent runs. As of June 2023, there is no automated way to create a bracket on a site such as espn.com with these results, so they must be entered manually.

## Future Work

This project is being actively worked and improved. See the GitHub [Projects](https://github.com/AGnias47/march-madness/projects?query=is%3Aopen) tab for details.
