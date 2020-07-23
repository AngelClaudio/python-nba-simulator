# Name Space Declarations
import pandas as pd 
import random as rnd
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import style

# Surpress warnings for chain assignments
pd.options.mode.chained_assignment = None

# Improve Plot Visibility
style.use('dark_background')

# Import data (originally from Kaggle) to data frame
url = 'https://github.com/AngelClaudio/DataSources/blob/master/nba_games_stats.csv?raw=true'

# 1st Column Used as Unique Identifier
original_nba_data = pd.read_csv(filepath_or_buffer = url, index_col=0)

# Take a look at the data frame
original_nba_data.info()

# Make copy and keep original (for debugging purposes)
nba_data = original_nba_data

# Transform Date Column from "object"(string) to date to make it easier to work with
nba_data['Date'] = pd.to_datetime(nba_data['Date'])

# Look at Dates
print(f"Dates for this data set are from {nba_data['Date'].min()} to {nba_data['Date'].max()}")

# Subset Data into Two Teams for 2018 season, namely the finals teams.
golden_state = nba_data[
    (nba_data.Team == 'GSW') & (nba_data['Date'] > '2017-10-01')
    ]

cleveland = nba_data[
    (nba_data.Team == 'CLE') & (nba_data['Date'] > '2017-10-01')
    ]

# Visualize Data
golden_state.TeamPoints.plot(kind='hist', label='GSW', alpha = .5, color='#87ceeb')
cleveland.TeamPoints.plot(kind='hist', label='CLE', alpha = .5, color='#800020')
plt.legend()
plt.xlabel('Points')
plt.title('Points Scored During 2018 Season')
plt.show()

golden_state.OpponentPoints.plot(kind='hist', label='GSW', alpha=.5, color='#87ceeb')
cleveland.OpponentPoints.plot(kind='hist', label='CLE', alpha=.5,color='#800020')
plt.legend()
plt.xlabel('Points')
plt.title('Opponents Points Scored During 2018 Season')
plt.show()

class NBA_Finals_Simulator:
  def __init__(self, team_one ='GSW', team_two ='CLE'):
      self.team_one_name = team_one
      self.team_two_name = team_two 
      self.nba_data = self.team_one = self.team_two = pd.DataFrame()  

      # Parameters
      self.team1_mean_pts = self.team1_std_pts = self.team1_mean_pts_allowed = self.team1_std_pts_allowed = 0
      self.team2_mean_pts = self.team2_mean_pts_allowed = self.team2_std_pts = self.team2_std_pts_allowed = 0

      # Pop Class
      self.set_data()
      self.set_parameters()

  def set_data(self):
      url = 'https://github.com/AngelClaudio/DataSources/blob/master/nba_games_stats.csv?raw=true'
      _data = pd.read_csv(filepath_or_buffer = url, index_col=0)
      _data['Date'] = pd.to_datetime(_data['Date'])

      # alpha only 2018 season
      _data = nba_data[nba_data['Date'] > '2017-10-01']
      self.team_one = _data[_data.Team == self.team_one_name]
      self.team_two = _data[_data.Team == self.team_two_name]
      self.nba_data = _data

  # For resetting and trying other teams
  def set_teams(self, team_one_name, team_two_name):
      self.team_one_name = team_one_name
      self.team_two_name = team_two_name 
      self.team_one = self.nba_data[self.nba_data.Team == self.team_one_name]
      self.team_two = self.nba_data[self.nba_data.Team == self.team_two_name]
      self.set_parameters()

  # See teams
  def show_teams(self):
    print(self.nba_data['Team'].unique())

  # See distribution comparisons for points and points allowed visualizations
  def show_team_comparisons(self):
      self.team_one.TeamPoints.plot(kind='hist', label=self.team_one_name, alpha = .5, color='white')
      self.team_two.TeamPoints.plot(kind='hist', label=self.team_two_name, alpha = .5, color='navy')
      plt.legend()
      plt.xlabel('Points')
      plt.title('Points Scored During 2018 Season')
      plt.show()

      self.team_one.OpponentPoints.plot(kind='hist', label=self.team_one_name, alpha=.5, color='white')
      self.team_two.OpponentPoints.plot(kind='hist', label=self.team_two_name, alpha=.5,color='navy')
      plt.legend()
      plt.xlabel('Points')
      plt.title('Points Allowed During 2018 Season')
      plt.show()

  def set_parameters(self):
      # Team One Means and Standard Deviations
      self.team1_mean_pts = self.team_one.TeamPoints.mean()
      self.team1_std_pts = self.team_one.TeamPoints.std()      
      self.team1_mean_pts_allowed = self.team_one.OpponentPoints.mean()
      self.team1_std_pts_allowed = self.team_one.OpponentPoints.std()

      # Team Two Means and Standard Deviations
      self.team2_mean_pts = self.team_two.TeamPoints.mean()
      self.team2_mean_pts_allowed = self.team_two.OpponentPoints.mean()
      self.team2_std_pts = self.team_two.TeamPoints.std()
      self.team2_std_pts_allowed = self.team_two.OpponentPoints.std()

  def monte_carlo_sim(self):
      # Simulation Model
      team1_scored = (rnd.gauss(self.team1_mean_pts, self.team1_std_pts) +
                  rnd.gauss(self.team2_mean_pts_allowed,self.team2_std_pts_allowed))/2

      team2_scored = (rnd.gauss(self.team2_mean_pts, self.team2_std_pts) + 
                 rnd.gauss(self.team1_mean_pts_allowed, self.team1_std_pts_allowed))/2

      # Evaluate Scores and Return Result
      if int(round(team1_scored)) > int(round(team2_scored)):
          return 1
      elif int(round(team1_scored)) < int(round(team2_scored)):
          return -1
      else: return 0 

  def simulate_finals(self, number_of_simulations=10000):  
    # Variable Place Holder Declarations
    result = team1_win_count = team1_win_count = team2_win_count = tie_count = 0

    # Trial simulations invoked here!
    for _ in range(number_of_simulations):
       
        # Run Trial Simulation
        result = self.monte_carlo_sim()

        # Tally results
        if result == 1:
            team1_win_count +=1 
        elif result == -1:
            team2_win_count +=1
        else: tie_count +=1 

    # Display to user results! \,,/(^_^)\,,/
    print(self.team_one_name, "won", "{:.4%}".format(team1_win_count/number_of_simulations), "of the time.")
    print(self.team_two_name, "won", "{:.4%}".format(team2_win_count/number_of_simulations), "of the time.")
    print("Both tied at", "{:.4%}".format(tie_count/number_of_simulations), "of the time.")