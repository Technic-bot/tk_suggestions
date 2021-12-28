import argparse 
import csv
import json

def proc_params():
  parser = argparse.ArgumentParser('Target analyzer')
  parser.add_argument('target', help='Target character')
  parser.add_argument('pollsfile',help='Poll file')
  parser.add_argument('output',default='', help='Output file')
  return parser.parse_args()


def read_file(filename):
  with open(filename,'r') as json_file:
    polls = json.load(json_file)
  msg = "Got {} polls from {}"
  print(msg.format(len(polls),filename))
  return polls 

def get_char_votes(target,polls):
  char_votes = {}
  for poll in polls:
    date = poll['PollStarted']
    places = poll['Placements']
    
    ballots = poll['Ballots']

    print("Analyzing poll started on {}".format(date))
    # Get all suggestions ids that match character target
    ids = []
    opts = poll['Options']
    for opt_id,name in opts.items():
      if target in name.lower():
        ids.append(chr(int(opt_id)))
    
    print("Found {} suggestions containing target".format(len(ids)))
    if not ids:
      continue

    for ballot in ballots:
      print("For ballot {}".format(ballot))
      for i in ids:
        # index to place 0 -> first etc
        r = ballot.find(i)+1
        if r > 0:
          print("\t For id {}".format(i))
          print("\t\t Found vote on place {}".format(r))
          if r in char_votes:
            char_votes[r] += 1
          else:
            char_votes[r] = 1    

  return char_votes

if __name__ == "__main__":
  args = proc_params()    
  polls = read_file(args.pollsfile)
  char_votes = get_char_votes(args.target,polls)
  #char_votes['name'] = args.target
  
  with open(args.output,'w') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerow(['name',args.target])
    writer.writerow(['place','votes'])
    for p,v in char_votes.items():
      writer.writerow((p,v))
    
    

  
