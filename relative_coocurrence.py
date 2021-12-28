import argparse 

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

import json

import co_ocurrence as co

def make_rel_mat(all_mat,win_mat):
  rel_dic = {}
  chars = all_mat.keys()
  print(chars)
  print(win_mat.keys())
  for c in chars:
    rel_dic[c] = {}

  for i in chars:
    for j in chars:
      all_sugs = all_mat[i][j]
      win_sugs = win_mat[i][j]
      if all_sugs:
        val = win_sugs/all_sugs
      else:
        val = 0 

      rel_dic[i][j] = val
  return rel_dic


if __name__=="__main__":
  args = co.proc_params()
  all_series = co.process_sug_file(args.suggestions,winners=False)  
  win_series = co.process_sug_file(args.suggestions,winners=True)  
  chars = co.read_char_list(args.chars_file)
  
  all_mat = co.make_co_ocurrence_matrix(all_series,chars)
  win_mat = co.make_co_ocurrence_matrix(win_series,chars)

  rel_mat = make_rel_mat(all_mat,win_mat)
  

  rel_mat_df = pd.DataFrame.from_dict(rel_mat,orient='index')
  rel_mat_df.to_csv(args.out_prefix + "relative_co_ocurrence.csv")
  hm = co.make_heatmap(rel_mat_df,args.title)

  print(rel_mat_df)
  if args.outfile:
    hm.savefig(args.outfile)
  else:
    plt.show()
  

  
