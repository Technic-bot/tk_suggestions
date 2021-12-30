# TK polls data repository and scripts
This repo is meant to archive the work i done graphing an analyzing different aspects of the Twokinds Sunday Sketches suggestions. It is meant more as an archive not as an stand alone repo you can clone and use, as such it is a bit messys but feel free to use and copy both the data and the scripts. 

## Quickstart
If you simply want to play with the data yourself look for file
```./results/analysis/2017-2021-suggestions.csv
results/analysis/2017-2021-timeframe.csv
```
These are csv files that can be opened with excel or similar program. Although i encourage you to play around with the py files you can play with the data without it if you want. Header of each file if self explanatory

## Structure
The repo is comprised of a couple python scripts made to process the raw data and generate both easy to use csv files and grpahs. For usage examples please refer to ``commands_to_run.sh.`` Every script should be standalone and  produce a different graph. The folders are structures as follows:

* This folder: Contains python scripts and input files (txt files)
* Results: Stores output csv files
* Graphs:  Contains output figures

## Dependencies 
To run the scripts you will need the following:

* Python 3 or up
* Matplotlib
* Numpy
* Pandas


