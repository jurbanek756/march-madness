# March Madness

Terminal-based scripts for selecting March Madness Winners!

The project offers an Evaluation and a Prediction Mode for creating a bracket.

* Evaluation Mode guides users through selecting a March Madness bracket, providing relevant information throughout the process
* Prediction Mode automatically selects a March Madness bracket through various prediction methods.

By default, the repo is set to guide the user through manually picking teams. This is done by running the following commands:

```shell
./run.py  # Go through selections
open NCAA_Tournament_Results.log  # Display selection results
```

More detailed usage information is provided below.

## Usage

### Database Generation

Data is scraped from external sources and stored in a Postgres database hosted on a Docker container. The database can be populated by importing the contents of `db/march_madness.sql`, or by running the `generate_db_data.py` script.

### Run Evaluations

User-guided methods are defined as evaluation methods. Currently, the evaluation method 
works by presenting the user with some basic info, with the option to present more, such 
as recent games and more school info. The user then selects a team for each matchup, or 
defers to a random selection. This method runs by default for the latest march madness 
year, but can also be overridden for any year 2022 or later with the `-y` parameter.

#### Sample Usage

##### Run the evaluation for the current year

```shell
./run.py  
```

or

```shell
./run.py -e
```

##### Run the evaluation for a different year

```shell
./run.py -e -y 2022
```

### Prediction Methods

Automated methods that use an algorithm to decide matchups are defined as prediction methods. The desired prediction method should be provided to the `-p` parameter from one of the methods listed below:
* `random` - Pure random choice
* `lptr` - Weighted random choice. Teams with a higher ranking are more likely to be selected to win, where weighing is done by the difference in ranking on a linearly proportional scale. AP rankings are also considered in this choice.
* `sigmodal` - Weighted random choice. Teams with a higher ranking are more likely to be selected to win, where weighing is done by the difference in ranking on a sigmoidal scale. AP rankings are also considered in this choice. The parameter `k` is used to determine the shape of the sigmodal curve. By default, `k=.33`, which closely emulates the behavior of a sigmodal curve without a scaling factor. `k` can be adjusted via the command line parameter `-k`, where a higher value will make the sigmodal curve more closely emulate a step function, and a lower value will make it more closely emulate a horizontal line. Run `./visualize_weight_functions.py` to see the effect of altering `k`.
* `ranked` - Chooses the team with the higher tournament ranking. If rankings are the same, defer to the AP ranking. If neither team is ranked by the AP, choose a team randomly.
* `ap` - Chooses the team with the higher AP ranking. If neither team is ranked by the AP, choose the team with the higher tournament ranking. If tournament rankings are the same, choose a team randomly.
* `nickname` - Chooses the team whose nickname has a higher positive sentiment analysis value.

#### Sample Usage

##### Random Selection for the current year

```shell
./run.py -p random
```

##### Weighted LPTR selection for 2022

```shell
./run.py -p lptr -y 2022
```

##### Weighted Sigmodal selection with overriding value of k

```shell
./run.py -p sigmodal -k 0.5
```

### Results

Results are stored in `NCAA_Tournament_Results.log`. The file is always appended to, so should be removed between subsequent runs. As of June 2023, there is no automated way to create a bracket on a site such as espn.com with these results, so they must be entered manually.

## Future Work

This project is being actively worked and improved. See the GitHub [Projects](https://github.com/AGnias47/march-madness/projects?query=is%3Aopen) tab for details.
