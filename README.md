# NHL Odds Calculator

This Python script calculates various odds and statistics for NHL games based on historical data. It uses Poisson distribution to model goal-scoring patterns and provides probabilities for different game outcomes.

## Features

- Load and process NHL game data
- Calculate team-specific and league-wide statistics
- Estimate expected goals for upcoming matches
- Calculate win/draw/loss probabilities
- Provide over/under probabilities for various goal thresholds
- Generate Poisson distribution tables for detailed goal probabilities
- Convert probabilities to both decimal and moneyline odds

## Requirements

- Python 3.x
- pandas
- numpy
- scipy

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/sidkrs/nhl-odds-calculator.git
   ```
2. Install the required packages:
   ```
   pip install pandas numpy scipy
   ```

## Usage

1. Ensure you have a CSV file named `NHL 22:23 Scores.csv` in the same directory as the script. This file should contain historical NHL game data.

2. Run the script:
   ```
   python nhl_odds_calculator.py
   ```

3. Follow the prompts to select the home and away teams for the match you want to analyze.

4. The script will output:
   - Expected goals for each team
   - Over/Under probabilities and odds for various goal thresholds
   - A Poisson distribution table showing probabilities for specific score outcomes
   - An odds table with decimal and moneyline odds for each possible score

## How it works

1. The script loads historical NHL game data and calculates the average goals scored by each team in home and away games.
2. It then calculates team-specific offensive and defensive strengths relative to the league average.
3. Using these strengths and the Poisson distribution, it estimates the probability of various outcomes for a given matchup.
4. The probabilities are then converted into odds formats commonly used in sports betting.

## Comparing with Betting Markets

The odds calculated by this tool can be compared with those offered by popular betting markets such as DraftKings or FanDuel. This comparison can potentially reveal discrepancies between the model's predictions and the market odds, which might indicate value betting opportunities. However, it's important to note that betting markets incorporate many factors beyond historical data, so any discrepancies should be carefully analyzed before making betting decisions.

## Customization

You can modify the script to:
- Use different data sources by changing the CSV file name but keep the column headers the same (Soccer works but set the max goals to maybe 6 or 7)
- Adjust the maximum number of goals considered in calculations (currently set to 10)
- Add more over/under thresholds or other types of bets

