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
  parser = argparse.ArgumentParser('Suggestions analyzer')
  parser.add_argument('timeframe', help='Parsed poll timeframe file csv')
  parser.add_argument('suggestions', help='Parsed suggestions files csv')
  parser.add_argument('chars_file',default='', help='Char file to analyze')
  parser.add_argument('--out-prefix',default='', help='Prefix for output files')
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
  
def graph_timeframe(time_df,tile="Plots over time"):
  fig,ax = plt.subplots(figsize=(10,8))
  fig.autofmt_xdate()
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
  ax.xaxis.set_major_locator(six)
  # ax.xaxis.set_minor_locator(months)
  
  ax.plot(time_df['date'],time_df['ballots'],label='Ballots')
  ax.plot(time_df['date'],time_df['suggestions'],label='Suggestions')
  ax.plot(time_df['date'],time_df['winner_votes'],label='Winner Votes')
  #ax.plot(time_df['date'],time_df['winner_difference'],label='Win difference')
  ax.legend()
  ax.set_title("Suggestions and votes over time")
  return fig

def graph_difference(time_df,tile="Vote win difference"):
  fig,ax = plt.subplots(figsize=(10,8))
  fig.autofmt_xdate()
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
  ax.xaxis.set_major_locator(six)
  # ax.xaxis.set_minor_locator(months)
  ax.plot(time_df['date'],time_df['winner_votes'],label='Winner Votes',color="#F7941D")
  ax.plot(time_df['date'],time_df['winner_difference'],label='Win difference', color="#72CDFE")
  ax.legend()
  ax.set_title("Winner votes and win difference")
  return fig

def graph_dif_hist(time_df,title="Vote difference histogram"):
  fig,ax = plt.subplots(figsize=(10,8))
  # ax.xaxis.set_minor_locator(months)
  bins = np.arange(1,max(time_df['winner_difference'])) 
  ax.hist(time_df['winner_difference'],bins = bins,label="Win difference",rwidth=0.8,color='#72CDFE',align='left')
  ax.legend()
  ax.set_title(title)
  ax.set_xlabel("Votes difference")
  ax.set_ylabel("Count")
  return fig
  

def graph_relative_wins(sug_df,title="Suggestions relative wins"):
  
  width = 0.25
  pos = np.arange(len(sug_df.index)-1)
  # Number of win(char)/suggestions(chars)  
  partial_df = sug_df.loc[sug_df.index != 'total' ]
  fig,ax = plt.subplots(figsize=(10,8))
  labels = partial_df.index   
  relative_ser = partial_df['winner'] / partial_df['count'] *100
  ax.bar(pos,relative_ser,width=width, label='Relative winrate', tick_label=labels,color='#72CDFE')
  ax.tick_params(axis='x', labelrotation = 45)
  ax.set_title(title)
  ax.set_ylabel("Percent")
  ax.legend()
  return fig

def graph_suggestions(sug_df,tile="Suggestions numerics per character"):
  # ax.xaxis.set_minor_locator(months)
  
  width = 0.25
  pos = np.arange(len(sug_df.index)-1)
  # Percentage  
  fig_per,ax = plt.subplots(figsize=(10,8))
  partial_df = sug_df.loc[sug_df.index != 'total' ]
  labels = partial_df.index
  total_cnt = sug_df.loc['total','count']
  total_wins = sug_df.loc['total','winner']
  cnt_series =  partial_df['count'] / total_cnt * 100
  win_series =  partial_df['winner']/ total_wins * 100
  ax.bar(pos,cnt_series,width=width,label='Suggestions',tick_label=labels,color='#72CDFE')
  ax.bar(pos+width,win_series,width=width,label='Wins',tick_label=labels,color='#F7943D')
  ax.tick_params(axis='x', labelrotation = 45)
  ax.set_title("Suggestions per character")
  ax.set_ylabel("Suggestions")
  ax.legend()

  # Absolute suggestions and wins
  fig_cnt,(ax,ax2) = plt.subplots(2,1,figsize=(10,8))
  partial_df = sug_df.loc[sug_df.index != 'total' ]
  labels = partial_df.index
  total_cnt = sug_df.loc['total','count']
  total_wins = sug_df.loc['total','winner']
  cnt_series =  partial_df['count'] 
  win_series =  partial_df['winner']
  ax.bar(pos,cnt_series,width=width,label='Suggestions',tick_label=labels,color='#72CDFE')
  ax.tick_params(axis='x', labelrotation = 45)
  ax.set_title("Suggestions per character")
  ax.set_ylabel("Suggestions")
  ax.legend()
  
  ax2.bar(pos+width,win_series,width=width,label='Wins',tick_label=labels,color='#F7941D')
  ax2.tick_params(axis='x', labelrotation = 45)
  ax2.set_title("Wins per character")
  ax2.set_ylabel("Wins")
  ax2.legend()

  # Votes and valid votes
  fig_votes,(ax,ax2) = plt.subplots(2,1,figsize=(10,8))
  vote_series =  partial_df['votes'] 
  all_votes_series =  partial_df['all_votes'] 
  ax.bar(pos,vote_series,width=width,label='Counted votes',tick_label=labels,color='#72CDFE')
  ax.tick_params(axis='x', labelrotation = 45)
  ax.set_title("Valid votes per character")
  ax.set_ylabel("Votes")
  ax.legend()

  ax2.bar(pos+width,all_votes_series,width=width,label='All votes',tick_label=labels,color='#F7941D')
  ax2.tick_params(axis='x', labelrotation = 45)
  ax2.set_title("All votes per character")
  ax2.set_ylabel("Votes")
  ax2.legend()
  #ax.bar(pos+2*width,sug_df['votes'],width=width,label='Valid votes',tick_label=labels)
  #ax.bar(pos+3*width,sug_df['all_votes'],width=width,label='All votes',tick_label=labels)
    #color)
  return fig_per,fig_cnt,fig_votes

def make_char_row(sdf,bool_series,fld_lst):
    tmp_df = sdf.loc[bool_series]
    slc_df = tmp_df[fld_lst]
    cnt = slc_df['votes'].count()
    nums = slc_df.sum().to_numpy().flatten() 
    return np.append(nums,cnt)

def process_suggs(sdf,char_list,top=10,prefix='out'):
  # Get in order of votes and win difference  
  sdf.sort_values('win_difference',inplace=True,ascending=False)
  top_difference = sdf.loc[0:top,('name','votes','winner','win_difference')]
  top_difference.to_csv(prefix + "_top_diff.csv")
  sdf.sort_values('votes',inplace=True,ascending=False)
  top_votes = sdf.loc[0:top,('name','votes','winner','win_difference')]
  top_votes.to_csv(prefix + "_top_votes.csv")

  # Get basic top votes 
  sdf['name'] = sdf['name'].str.lower()
  total_count=sdf['name'].count()
  print("Got {} suggestions total".format(total_count))
  fld_lst = ['votes','winner','win_difference','all_votes']

  char_dic = {}
  # Get others, not specified in char list
  all_bool = pd.Series(np.zeros(len(sdf),dtype=bool))
  
  for c in char_list:
    print("Checking for " + c )
    bool_series = sdf['name'].str.contains(c,regex=False)
    all_bool |= bool_series
    char_dic[c]=make_char_row(sdf,bool_series,fld_lst)
  
  # Total  
  char_dic['total'] = np.append(sdf[fld_lst].sum().to_numpy(),total_count)
  # Others, for anything no in char list
  char_dic['others'] = make_char_row(sdf,~all_bool,fld_lst) 
  sdf.loc[~all_bool].to_csv(prefix + '_others.csv')
  col_list=[]
  col_list.extend(fld_lst)
  col_list.append('count')

  char_df = pd.DataFrame.from_dict(char_dic,orient='index',columns=col_list)
  char_df.sort_values('count',inplace=True,ascending=False)
  print(char_df)
  # Cant get true probability from this, one suggestion may mention 
  # more than one charcter so it duplicates the count
  #  char_df.loc['others'] = char_df.loc['total'] - char_df.loc[char_df.index != 'total'].sum()
  char_df.to_csv(prefix + "_counts_df.csv")
  return char_df



if __name__=="__main__":
  args = proc_params()
  suggs_df = pd.read_csv(args.suggestions)
  time_df  = pd.read_csv(args.timeframe)
  chars = read_char_list(args.chars_file)

  process_frame(suggs_df)
  process_frame(time_df)

  char_df = process_suggs(suggs_df,chars,prefix=args.out_prefix)

  tf_fig = graph_timeframe(time_df)
  #dif_fig = graph_difference(time_df)
  f_per,cnt_fig, v_fig = graph_suggestions(char_df)
  f_rel = graph_relative_wins(char_df)
  f_hist = graph_dif_hist(time_df)
  if args.img_prefix:
    tf_fig.savefig(args.img_prefix + '_timeframe.png')
    f_per.savefig(args.img_prefix + '_pecent_wins.png')
    f_rel.savefig(args.img_prefix + '_relative_wins.png')
    cnt_fig.savefig(args.img_prefix + '_counts.png')
    v_fig.savefig(args.img_prefix + '_votes.png')
    f_hist.savefig(args.img_prefix + '_hist.png')
  else:
    plt.show()
