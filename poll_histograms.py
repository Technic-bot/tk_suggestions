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
  #parser.add_argument('suggestions', help='Parsed suggestions files csv')
  parser.add_argument('--img-prefix',default='', help='Prefix for image files')
  return parser.parse_args()

def process_frame(df):
  """ Generic frame procession """ 
  df['date'] = pd.to_datetime(df['date'])
  df.sort_values('date',inplace=True)
  return

def read_char_list(txt_file):
  chars = []
  with open(txt_file,'r') as char_file:
    for c in char_file.readlines():
      chars.append(c.strip())
  
  print("Read {} chars".format(len(chars)))
  return chars

def add_author(ax):
  ax.annotate('Made by Tec-Bot with Matplotlib',
            xy = (0.9, -0.05),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=7)
  return

def graph_dif_hist(time_df,title="Vote difference histogram"):
  fig,ax = plt.subplots(figsize=(10,8))
  # ax.xaxis.set_minor_locator(months)
  bins = np.arange(1,max(time_df['winner_difference'])) 
  ax.hist(time_df['winner_difference'],bins = bins,label="Win difference",rwidth=0.8,color='#72CDFE',align='left')
  ax.legend()
  ax.set_title(title)
  ax.set_xlabel("Votes difference")
  ax.set_ylabel("Count")
  add_author(ax)
  return fig
  
def unused_ballots_hist(time_df,y_percent=False):
  fig,ax = plt.subplots(figsize=(10,8))
  # ax.xaxis.set_minor_locator(months)
  bins = np.linspace(0,100+1,20)
  bins = np.arange(0,100,5)
  unused_ballot_percent=time_df['all_votes']/time_df['ballots']*100
  if y_percent:
    w = np.ones(len(unused_ballot_percent))/len(unused_ballot_percent)
    ax.hist(unused_ballot_percent,weights=w,bins=bins,label="Unused ballots",rwidth=0.8,color='#72CDFE',align='mid')
  else:
    ax.hist(unused_ballot_percent,bins=bins,label="Unused ballots",rwidth=0.8,color='#72CDFE',align='mid')
  ax.set_xticks(bins)
  ax.legend()
  title = "Unused ballots as percentage of total ballots"
  ax.set_title(title)
  ax.set_xlabel("Percentage of total ballots (%)")
  ax.set_ylabel("Count")
  add_author(ax)
  return fig
  
def graph_win_ratio_hists(time_df,
    title="Number of descisive votes as percentage of total ballots",
    y_percent=False):
  fig,ax = plt.subplots(figsize=(10,8))
  # ax.xaxis.set_minor_locator(months)
  bins = np.linspace(0,100+1,5)
  bins = np.arange(0,100,5)
  win_ballot_percent=time_df['final_votes']/time_df['ballots']*100
  if y_percent:
    w = np.ones(len(win_ballot_percent))/len(win_ballot_percent)
    ax.hist(win_ballot_percent,weights=w,bins=bins,label="Win Ratio",rwidth=0.8,color='#72CDFE',align='mid')
  else:
    ax.hist(win_ballot_percent,bins=bins,label="Win Ratio",rwidth=0.8,color='#72CDFE',align='mid')
  ax.set_xticks(bins)
  ax.legend()
  ax.set_title(title)
  ax.set_xlabel("Percentage of total ballots (%)")
  ax.set_ylabel("Count")
  add_author(ax)
  return fig

if __name__=="__main__":
  args = proc_params()
  time_df  = pd.read_csv(args.timeframe)
  process_frame(time_df)

  f_hist = graph_dif_hist(time_df)
  w_hist =  graph_win_ratio_hists(time_df)
  u_hist =  unused_ballots_hist(time_df)

  if args.img_prefix:
    f_hist.savefig(args.img_prefix + '_hist.png')
    w_hist.savefig(args.img_prefix + '_win_hist.png')
  else:
    plt.show()
