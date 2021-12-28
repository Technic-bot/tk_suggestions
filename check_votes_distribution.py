import argparse 
import json

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

years =mdates.YearLocator()
months = mdates.MonthLocator()
six = mdates.MonthLocator(interval=6)
plt.style.use('seaborn-darkgrid')

def proc_params():
  parser = argparse.ArgumentParser('Target analyzer')
  parser.add_argument('charcsv', help='Target character votes json')
  parser.add_argument('--output',default='', help='Output file')
  return parser.parse_args()

def get_char_dist(char_df): 
  char_df.sort_values('place',inplace=True) 
  fig, ax = plt.subplots(figsize=(7,8))
  ax.bar(char_df['place'],char_df['votes'])
  return fig

def get_header(csv_path):
  with open(csv_path) as csv_file:
    name = csv_file.readline().split(',')[1]
  return name

if __name__ == "__main__":
  args = proc_params()      
  char = get_header(args.charcsv)
  print("Vote distribution for {}".format(char))
  char_df = pd.read_csv(args.charcsv,skiprows=1)
  get_char_dist(char_df)
  print(char_df)
  plt.show()
