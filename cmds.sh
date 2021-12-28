#!/bin/bash
python3 co_ocurrence.py results/anlysis/suggestions.csv chars.txt --outfile graphs/coocurrence.png --out-prefix results/first

python3 analyze_suggestions.py  results/anlysis/timeframe.csv  results/anlysis/suggestions.csv  chars.txt --img-prefix graphs/results --out-prefix results/anlysis/out-
python3 co_ocurrence.py results/anlysis/suggestions.csv chars.txt --out-prefix results/first --title All suggestions --winners
python3 co_ocurrence.py results/anlysis/suggestions.csv chars_2.txt --out-prefix results/first --title All suggestions --outfile graphs/all_coocurrence.png
python3 char_overtime.py results/anlysis/suggestions.csv char_bas.txt --frequency 1 --winner
python3 relative_coocurrence.py results/anlysis/suggestions.csv chars_2.txt --out-prefix results/rel --title Relative suggestions --outfile graphs/coocurrence_recolor.png 
python3 relative_coocurrence.py results/anlysis/suggestions.csv chars_2.txt --out-prefix results/rel --title Relative suggestions --outfile graphs/relative_coocurrence.png 
python3 process_polls.py results/2017-2021.json --sug results/anlysis/2017-2021-suggestions.csv --time results/anlysis/2017-2021-timeframe.csv
