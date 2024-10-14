import pandas as pd
import numpy as np
from scipy.stats import poisson

def load_data(file_path):
    return pd.read_csv(file_path)

def calculate_team_stats(df):
    home_goals = df.groupby('Home').agg({'G': 'sum', 'Home': 'count'}).rename(columns={'G': 'HomeGoals', 'Home': 'HomeGames'})
    away_goals = df.groupby('Visitor').agg({'G.1': 'sum', 'Visitor': 'count'}).rename(columns={'G.1': 'AwayGoals', 'Visitor': 'AwayGames'})
    
    team_stats = pd.concat([home_goals, away_goals], axis=1).fillna(0)
    team_stats['TotalGoals'] = team_stats['HomeGoals'] + team_stats['AwayGoals']
    team_stats['TotalGames'] = team_stats['HomeGames'] + team_stats['AwayGames']
    
    team_stats['HomeAvg'] = team_stats['HomeGoals'] / team_stats['HomeGames']
    team_stats['AwayAvg'] = team_stats['AwayGoals'] / team_stats['AwayGames']
    team_stats['TotalAvg'] = team_stats['TotalGoals'] / team_stats['TotalGames']
    
    return team_stats

def calculate_league_averages(team_stats):
    league_home_avg = team_stats['HomeAvg'].mean()
    league_away_avg = team_stats['AwayAvg'].mean()
    return league_home_avg, league_away_avg

def calculate_team_strengths(team_stats, league_home_avg, league_away_avg):
    team_stats['HomeStrength'] = team_stats['HomeAvg'] / league_home_avg
    team_stats['AwayStrength'] = team_stats['AwayAvg'] / league_away_avg
    return team_stats

def calculate_expected_goals(home_team, away_team, team_stats, league_home_avg, league_away_avg):
    home_attack = team_stats.loc[home_team, 'HomeStrength']
    home_defense = team_stats.loc[home_team, 'AwayStrength']
    away_attack = team_stats.loc[away_team, 'AwayStrength']
    away_defense = team_stats.loc[away_team, 'HomeStrength']
    
    home_expected = league_home_avg * home_attack * away_defense
    away_expected = league_away_avg * away_attack * home_defense
    
    return home_expected, away_expected

def calculate_result_probabilities(home_expected, away_expected):
    max_goals = 10
    home_probs = [poisson.pmf(i, home_expected) for i in range(max_goals+1)]
    away_probs = [poisson.pmf(i, away_expected) for i in range(max_goals+1)]
    
    result_probs = np.outer(home_probs, away_probs)
    
    home_win = np.sum(np.tril(result_probs, -1))
    draw = np.sum(np.diag(result_probs))
    away_win = np.sum(np.triu(result_probs, 1))
    
    return home_win, draw, away_win, result_probs

def calculate_over_under(result_probs, threshold):
    total_goals = sum(
        result_probs[i][j]
        for i in range(result_probs.shape[0])
        for j in range(result_probs.shape[1])
        if i + j > threshold
    )
    return total_goals

def probability_to_odds(probability):
    if probability == 0:
        return float('inf'), float('inf')
    decimal_odds = 1 / probability
    if decimal_odds >= 2:
        moneyline_odds = (decimal_odds - 1) * 100
    else:
        moneyline_odds = -100 / (decimal_odds - 1)
    return round(decimal_odds, 2), round(moneyline_odds)

def calculate_team_over_under(expected_goals, threshold):
    return poisson.sf(threshold, expected_goals)

def main():
    df = load_data('NHL 22:23 Scores.csv')
    team_stats = calculate_team_stats(df)
    league_home_avg, league_away_avg = calculate_league_averages(team_stats)
    team_stats = calculate_team_strengths(team_stats, league_home_avg, league_away_avg)
    
    teams = team_stats.index.tolist()
    print("Available teams:")
    for i, team in enumerate(teams, 1):
        print(f"{i}. {team}")
    
    def get_team_input(prompt):
        while True:
            team = input(prompt)
            if team.isdigit() and 1 <= int(team) <= len(teams):
                return teams[int(team) - 1]
            elif team in teams:
                return team
            else:
                print("Invalid input. Please enter a valid team name or number.")
    
    home_team = get_team_input("Enter the home team (name or number): ")
    away_team = get_team_input("Enter the away team (name or number): ")
    
    home_expected, away_expected = calculate_expected_goals(home_team, away_team, team_stats, league_home_avg, league_away_avg)
    home_win, draw, away_win, result_probs = calculate_result_probabilities(home_expected, away_expected)
    
    print(f"\nExpected goals: {home_team} {home_expected:.2f} - {away_expected:.2f} {away_team}")
    
    thresholds = [1.5, 2.5, 3.5, 4.5]
    under_thresholds = [4.5, 3.5, 2.5, 1.5] 
    
    print("\nOver/Under Moneyline Odds:")
    print(f"{'':10} {home_team:>15} {away_team:>15} {'Total':>15}")
    print("-" * 58)
    
    for t in reversed(thresholds):
        home_over = calculate_team_over_under(home_expected, t)
        away_over = calculate_team_over_under(away_expected, t)
        total_over = calculate_over_under(result_probs, t)
        
        _, home_ml = probability_to_odds(home_over)
        _, away_ml = probability_to_odds(away_over)
        _, total_ml = probability_to_odds(total_over)
        
        print(f"Over {t:<5} {home_ml:>+15.0f} {away_ml:>+15.0f} {total_ml:>+15.0f}")
    
    for t in under_thresholds:
        home_under = 1 - calculate_team_over_under(home_expected, t-1)
        away_under = 1 - calculate_team_over_under(away_expected, t-1)
        total_under = 1 - calculate_over_under(result_probs, t-1)
        
        _, home_ml = probability_to_odds(home_under)
        _, away_ml = probability_to_odds(away_under)
        _, total_ml = probability_to_odds(total_under)
        
        print(f"Under {t:<5} {home_ml:>+15.0f} {away_ml:>+15.0f} {total_ml:>+15.0f}")



    print("\nPoisson Distribution Table (Probabilities):")
    print("   ", end="")
    for i in range(6):
        print(f"{i:8}", end="")
    print()
    for i in range(6):
        print(f"{i}: ", end="")
        for j in range(6):
            print(f"{result_probs[i][j]:.6f}", end=" ")
        print()
    
    print("\nOdds Table (Decimal Odds, Moneyline Odds):")
    print("   ", end="")
    for i in range(6):
        print(f"{i:16}", end="")
    print()
    for i in range(6):
        print(f"{i}: ", end="")
        for j in range(6):
            decimal, moneyline = probability_to_odds(result_probs[i][j])
            print(f"({decimal:.2f}, {moneyline:+.0f}) ", end="")
        print()

if __name__ == "__main__":
    main()