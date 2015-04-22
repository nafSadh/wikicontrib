import re
def split4level(str):
  splits = line.split(" ",1)
  if len(splits)>1: return splits
  return "",""

def getName(str):
  if str.count('(')>1: str = str.replace('(','<',1).replace(')','>',1)
  str = re.sub('<.*?>','',str)
  name = str.split("(",1)[0]
  name = name.replace('<s>','').replace('</s>','').translate(None,"\'[]#,\n").strip()
  return name

def getUser(str):
  temp = re.findall("[Uu]ser:.*?\]",str)
  if len(temp )<1: return ""
  temp = temp[0].translate(None,"]")
  t = temp.find('|')
  if t is not -1: temp = temp[:t]
  return temp

textfile = 'votes.txt'
cnt = 0
name, aye, nay = "",0,0
users, uaye, unay = [],{},{}
nafsadh = []
withdrawsErr = False
with open(textfile, "rU") as file:
  lines = file.readlines()
  for line in lines:
    level,rest = split4level(line)
    # print level
    if level == "#":
      print "{},{},{},{}".format(cnt,name,aye,nay)
      aye,nay,cnt = 0,0,(cnt+1)
      name = getName(rest)
    if level == "###":
      user = getUser(rest)
      if user not in users and user is not "":
        users.append(user);uaye[user]=0; unay[user]=0
      if "<s>" in rest and ("{{aye" in rest or "{{nay" in rest):
        print "Error in withdrawn vote at:",name
        withdrawsErr = True
      if "{{aye" in rest:
        aye+=1
        uaye[user]+=1
      if "{{nay" in rest:
        nay+=1
        unay[user]+=1

  print "{},{},{},{}".format(cnt,name,aye,nay)
  users = sorted(users, key=lambda s: s.lower())
  for u in users:
    total = uaye[u]+unay[u]
    excessClause = "{{Redflag}} "+str(total-40)+ " excess votes" if total>40 else ""
    print "# [[{}]] ({})".format(u,(uaye[u]+unay[u])),"Y:",uaye[u],"N:",unay[u], excessClause

  if withdrawsErr: print "Error in withdrawn votes"
