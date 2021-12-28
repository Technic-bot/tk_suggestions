import process_polls
from pprint import pprint

polls = process_polls.read_file('/home/jesus/twks/polls/results/poll_zip/merged_total.json')
recent=polls[-10:-1]
sugs=process_polls.parse_suggestions(recent)

sug_target = 'Grand'
#pprint(recent['Options'])
for r in recent:
  target_id=0
  target_name=''
  votes = 0
  for uid,name in r['Options'].items():
    if  sug_target in name:
      target_id = int(uid)
      target_char = chr(target_id)
      target_name = name 

  for ballot in r['Ballots']:
    if target_char in ballot:
      votes+=1

  if target_name:
    print("Got {} ballots".format(r['CountedBallots']))
    msg = "Sketch suggestion {} with id {} and char {}, received {} votes on {}"
    print(msg.format(target_id,target_name,target_char,votes,r['PollStarted']))

for s in sugs:
  if 'Grand' in s['name']:
    pprint(s)  
