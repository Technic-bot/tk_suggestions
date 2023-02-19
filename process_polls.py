import argparse 
import json 
import csv 

def proc_params():
  parser = argparse.ArgumentParser('Poller analyzer')
  parser.add_argument('file')
  parser.add_argument('--timeframe-file',default='timeframe.csv', help='Time frame csv')
  parser.add_argument('--suggestions-file',default='suggestions.csv',help='Suggestions out file')
  return parser.parse_args()

def read_file(filename):
  with open(filename,'r') as json_file:
    polls = json.load(json_file)
  
  msg = "Got {} polls from {}"
  print(msg.format(len(polls),filename))
  return polls

def parse_timeframe(poll_list):
  timeframe = []
  for poll in poll_list:
    date = poll['PollStarted'] 
    opts = len(poll['Options'])
    ballots = poll['CountedBallots']
    places = poll['Placements']
    winner = places[-1][0]
    winner_votes = winner['V']
    winner_id = winner['Id']
    # Irrelevant for winner votes on win = all_votes
    all_votes = get_all_votes(winner_id,poll['Ballots'])
    final = places[-2]
    win_diff = abs(final[0]['V'] - final[1]['V'])
    final_votes = max((final[0]['V'], final[1]['V']))
    frame = [date,opts,ballots,winner_votes,all_votes,win_diff,final_votes]
    timeframe.append(frame)

  return  timeframe

def get_all_votes(uid,ballots):
  target_id = int(uid)
  target_char = chr(target_id)
  votes = 0 
  for ballot in ballots:
    if target_char in ballot:
      votes += 1
  return votes
    
def parse_suggestions(polls):
  suggestions=[]
  for poll in polls:
    date = poll['PollStarted'] 
    print("Processing poll from {}".format(date))
    # Getting all votes for all suggestions
    tmp = {}
    places = poll['Placements']
    # Placements is an array of arrays
    for place in places:
      for vote in place:
        # vote is an array of dicts
        tmp[vote['Id']] = vote['V']

    # Winner 
    winner = places[-1][0]    
    winner_id = winner['Id']
    # Win difference
    final = places[-2]
    win_diff = abs(final[0]['V'] - final[1]['V'])
    # Options is a plain dictionary
    opts = poll['Options']
    for opt_id, name in opts.items():
      opt_id = int(opt_id)
      all_votes = get_all_votes(opt_id,poll['Ballots'])
      suggestion = {"name": name, "votes": tmp[opt_id],
        'all_votes':all_votes,'date':date}
    #  print("Suggestion {}".format(suggestion['name']))
      if opt_id == winner_id:
        suggestion['winner'] = True
        suggestion['win_difference'] = win_diff
      else:
        suggestion['winner'] = False
        suggestion['win_difference'] = 0 
    
      
      suggestions.append(suggestion)

  return suggestions

def persist_timeframe(timeframe,filename):
  header = ['date','suggestions','ballots',
            'winner_votes','all_votes', 'winner_difference','final_votes']
  with open(filename,'w') as csv_timeframe:
    csv_writer = csv.writer(csv_timeframe)
    csv_writer.writerow(header)
    csv_writer.writerows(timeframe)
  return

def persist_suggestions(suggestions,filename):
  fields = ['name','date','votes','all_votes','winner','win_difference']
  with open(filename,'w') as csv_timeframe:
    csv_writer = csv.DictWriter(csv_timeframe,fieldnames=fields)
    csv_writer.writeheader()
    csv_writer.writerows(suggestions)
  return

if __name__=="__main__":
  args = proc_params()
  polls =  read_file(args.file)
  timeframe = parse_timeframe(polls)
  suggestions = parse_suggestions(polls)
  persist_timeframe(timeframe,args.timeframe_file)
  persist_suggestions(suggestions,args.suggestions_file)
