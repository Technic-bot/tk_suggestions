import argparse 

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import json

plt.style.use('seaborn-darkgrid')

def proc_params():
  parser = argparse.ArgumentParser('Suggestions analyzer')
  parser.add_argument('suggestions', help='Parsed suggestions files csv')
  parser.add_argument('chars_file',default='', help='Char file to analyze')
  parser.add_argument('--out-prefix',default='out', help='Prefix for output files')
  parser.add_argument('--frequency',default=None, help='Prefix for output files')
  parser.add_argument('--outfile',default='', help='Prefix for output files')
  parser.add_argument('--winners',action='store_true', help='Make heatmap only over winning sketches')
  parser.add_argument('--title',default=None, help='Graph title')
  return parser.parse_args()


def read_char_list(txt_file):
  chars = []
  with open(txt_file,'r') as char_file:
    for c in char_file.readlines():
      chars.append(c.strip())
  print("Read {} chars".format(len(chars)))
  return chars

def process_suggestions(filename,winners=False):
  s_df = pd.read_csv(filename)
  s_df['name'] = s_df['name'].str.lower()
  s_df['date'] = pd.to_datetime(s_df['date'] )
  if winners:
    s_df = s_df[s_df['winner'] == True]
   
  return s_df

def get_counts(sdf,chars,freq=None,tile=None):
  if freq:
    f_str = "{}MS".format(freq)
    print("Grouping each {} months".format(freq))
    grouper = pd.Grouper(key='date',freq=f_str, origin='epoch',dropna    =False)
  else:
    grouper = 'date'
  
  time_dic = {}
  for c in chars:
    slc_df = sdf[sdf['name'].str.contains(c)]
    gdf = slc_df.groupby(grouper)
    cnt_df = gdf['name'].size()
    time_dic[c] = cnt_df
  

  return time_dic 

def graph_timeseries(cnt_dic,title=None):
  fig,ax = plt.subplots(figsize=(12,8))
  fig.autofmt_xdate()

  mon_l = mdates.MonthLocator(interval=4)
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
  ax.xaxis.set_major_locator(mon_l)

  for char,cnt in cnt_dic.items():
    ax.plot(cnt.index,cnt.values,label=char)

  if not title:
    ax.set_title("Character suggestions over time")  
  else:
    ax.set_title("Character suggestions over time\n" + title)  

  ax.legend()
  return fig
  

if __name__=="__main__":
  args = proc_params()
  sdf = process_suggestions(args.suggestions,winners=args.winners)
  chars = read_char_list(args.chars_file)
#  with open('debug.json','w') as json_file:
#    json.dump(mat,json_file)
  
  cnt = get_counts(sdf,chars,freq=args.frequency)
  graph_timeseries(cnt,title=args.title)
  if args.outfile:
    hm.savefig(args.outfile)
  else:
    plt.show()
  
