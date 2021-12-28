import argparse 

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

import json

#plt.style.use('seaborn-darkgrid')

def proc_params():
  parser = argparse.ArgumentParser('Co ocurrence analyzer')
  parser.add_argument('suggestions', help='Parsed suggestions files csv')
  parser.add_argument('chars_file',default='', help='Char file to analyze')
  parser.add_argument('--out-prefix',default='out', help='Prefix for output files')
  parser.add_argument('--outfile',default='', help='Prefix for output files')
  parser.add_argument('--winners',action='store_true', help='Make heatmap only over winning sketches')
  parser.add_argument('--title',default=None, help='Graph title')
  return parser.parse_args()

def process_sug_file(filename,winners=False):
  """ Reads suggestion csv and returns a series of only suggestions titles"""
  df = pd.read_csv(filename)
  df['name'] = df['name'].str.lower()
  if winners: 
    df = df[df['winner'] == True]
  
  return df['name']

def read_char_list(txt_file):
  chars = []
  with open(txt_file,'r') as char_file:
    for c in char_file.readlines():
      chars.append(c.strip())
  
  print("Read {} chars".format(len(chars)))
  return chars

def make_co_ocurrence_matrix(series,chars):
  matrix = {}
  # initialize matrix: 
  # Dic of dic generalizes array of arrays
  for c in chars:
    matrix[c] = {}
  # Matrix need double for
  for c_row in chars:
    #print("Checking for " + c_row)
    c_series = series[series.str.contains(c_row,regex=False)]
    for c_col in chars:
      #print("\t with " + c_col)
      matrix[c_row][c_col] = c_series.str.contains(c_col,regex=False).sum()
  return matrix

def make_cm():
  lut = 128
  top = cm.get_cmap('Blues', lut)
  bottom = cm.get_cmap('Oranges', lut)

  newcolors = np.vstack((top(np.linspace(0, 1, 32)),
                       bottom(np.linspace(0, 1, 128))))
  newcolors = bottom(np.linspace(0, 1, 128))
  newcmp = ListedColormap(newcolors, name='OrangeBlue')
  return newcmp

def make_heatmap(mat_df, subtitle= None):
  labels = mat_df.index
  # From series to dic to pandas, to numpy? that has to be a record 
  plain_mat = mat_df.to_numpy()
  
  cmap=make_cm()
  fig,ax = plt.subplots(figsize=(11,9))
  ax.imshow(plain_mat,cmap=cmap)

  ax.set_xticks(np.arange(len(labels)), labels=labels)
  ax.set_yticks(np.arange(len(labels)), labels=labels)
  ax.tick_params(axis='x', labelrotation = 46)

  
  for i in range(len(labels)):
    for j in range(len(labels)):
      number = plain_mat[i,j]
      if isinstance(number,float):
        txt = "{:.2f}".format(number)
      else:
        txt = str(number)
      ax.text(j,i,txt,ha="center",va="center")

  if not subtitle:
    ax.set_title("Twokinds co-ocurrence Matrix")
  else:
    ax.set_title("Twokinds co-ocurrence Matrix\n" + subtitle)
  return fig
  

if __name__=="__main__":
  args = proc_params()
  name_series = process_sug_file(args.suggestions,winners=args.winners )
  chars = read_char_list(args.chars_file)
  mat = make_co_ocurrence_matrix(name_series,chars)
#  with open('debug.json','w') as json_file:
#    json.dump(mat,json_file)
  mat_df = pd.DataFrame.from_dict(mat,orient='index')
  mat_df.to_csv(args.out_prefix + "_co_ocurrence.csv")
  hm = make_heatmap(mat_df,args.title)
  
  print(mat_df)
  if args.outfile:
    hm.savefig(args.outfile)
  else:
    plt.show()
