#!/bin/bash
python3 co_ocurrence.py results/analysis/suggestions.csv chars.txt --outfile graphs/coocurrence.png --out-prefix results/first

python3 analyze_suggestions.py  results/analysis/timeframe.csv  results/analysis/suggestions.csv  chars.txt --img-prefix graphs/results --out-prefix results/analysis/out-
python3 co_ocurrence.py results/analysis/suggestions.csv chars.txt --out-prefix results/first --title All suggestions --winners
python3 co_ocurrence.py results/analysis/suggestions.csv chars_2.txt --out-prefix results/first --title All suggestions --outfile graphs/all_coocurrence.png
python3 char_overtime.py results/analysis/suggestions.csv char_bas.txt --frequency 1 --winner
python3 relative_coocurrence.py results/analysis/suggestions.csv chars_2.txt --out-prefix results/rel --title Relative suggestions --outfile graphs/coocurrence_recolor.png 
python3 relative_coocurrence.py results/analysis/suggestions.csv chars_2.txt --out-prefix results/rel --title Relative suggestions --outfile graphs/relative_coocurrence.png 
python3 process_polls.py results/2017-2021.json --sug results/analysis/2017-2021-suggestions.csv --time results/analysis/2017-2021-timeframe.csv
python3 process_polls.py results/2017-2022.json --sug results/analysis/2017-2022-suggs.csv --time results/analysis/2017-2022-time.csv
