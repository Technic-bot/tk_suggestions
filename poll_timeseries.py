import argparse 

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

years =mdates.YearLocator()
months = mdates.MonthLocator()
six = mdates.MonthLocator(interval=6)
plt.style.use('seaborn-darkgrid')

def proc_params():
  parser = argparse.ArgumentParser('Suggestions histograms ')
  parser.add_argument('timeframe', help='Parsed poll timeframe file csv')
  parser.add_argument('--img-prefix',default='', help='Prefix for image files')
  return parser.parse_args()

def process_frame(df):
  """ Generic frame procession """ 
  df['date'] = pd.to_datetime(df['date'])
  df.sort_values('date',inplace=True)
  df2 = df.loc[ df['all_votes'] > 10 ]
  return df2

def read_char_list(txt_file):
  chars = []
  with open(txt_file,'r') as char_file:
    for c in char_file.readlines():
      chars.append(c.strip())
  
  print("Read {} chars".format(len(chars)))
  return chars

def add_author(ax):
  ax.annotate('Made by Tec-Bot with Matplotlib',
            xy = (1.0, -0.05),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=7)
  return

def vote_difference_ts(time_df,title="Decisive votes over time"):
  """ Plots difference of votes in last round betwwen first and second place"""
  fig,ax = plt.subplots(figsize=(10,8))
  fig.autofmt_xdate()
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m%-d'))
 # ax.xaxis.set_major_locator(six)
  print(time_df.loc[time_df['winner_difference'].idxmax()])
  print(time_df.loc[time_df['ballots'].idxmin()])
  ax.plot(time_df['date'],time_df['winner_difference'],label="Win difference",color='#72CDFE')
  ax.legend()
  ax.set_title(title)
  ax.set_xlabel("Date")
  ax.set_ylabel("Decisive Votes")
  add_author(ax)
  return fig
  
def unused_ballots_ts(time_df,y_percent=False):
  fig,ax = plt.subplots(figsize=(10,8))
  fig.autofmt_xdate()
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

  unused_ballot_percent=time_df['all_votes']/time_df['ballots']*100
  ax.plot(time_df['date'],unused_ballot_percent,label="Unused ballots",color='#72CDFE')
  ax.legend()
  title = "Unused ballots as percentage of total ballots over time"
  ax.set_title(title)
  ax.set_xlabel("Date")
  ax.set_ylabel("Percentage of total ballots (%)")
  add_author(ax)
  return fig
  
def win_ratio_ts(time_df,
    title="Number of descisive votes as percentage of total ballots",
    y_percent=False):
  fig,ax = plt.subplots(figsize=(10,8))
  fig.autofmt_xdate()
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
  # ax.xaxis.set_minor_locator(months)
  bins = np.linspace(0,100+1,5)
  bins = np.arange(0,100,5)
  win_ballot_percent=time_df['final_votes']/time_df['ballots']*100
  ax.plot(time_df['date'],win_ballot_percent,label="Unused ballots",color='#72CDFE')
  ax.legend()
  ax.set_title(title)
  ax.set_ylabel("Percentage of total ballots (%)")
  ax.set_xlabel("Date")
  add_author(ax)
  return fig

if __name__=="__main__":
  print("Starting Timeseries program")
  args = proc_params()
  print("Reading suggestions")
  df  = pd.read_csv(args.timeframe)
  print("Processing")
  time_df = process_frame(df)

  print("Graphing")
  f_hist = vote_difference_ts(time_df)
  w_hist =  win_ratio_ts(time_df)
  u_hist =  unused_ballots_ts(time_df)

  if args.img_prefix:
    f_hist.savefig(args.img_prefix + '_diff_ts.png')
    w_hist.savefig(args.img_prefix + '_win_ts.png')
    u_hist.savefig(args.img_prefix + '_unused_ts.png')
  else:
    plt.show()
