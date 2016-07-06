import random
import sys
import sets
import math

def weighted_pick(count):
  ratio = 5.0  # the ratio of probability of killing first over killing the last
  base = -500.0 / math.log(1.0 / ratio)
  raw_weight = []
  for i in range(500):
    weight = ratio * math.exp(-i / base)
    raw_weight += [ weight ]
  total = sum(raw_weight)
  weight = [w * 1.0 / total for w in raw_weight]  # normalize

  # print "weight len = %d: %s" % (len(weight), weight)

  random.seed()
  results = sets.Set()
  while len(results) < count:
    r = random.random() - weight[0]
    i = 0
    while r > 0:
      r -= weight[i]
      i += 1
    if i != 0:  # qunzhu never dies
      results.add(i)
  return [r for r in results]

to_die = weighted_pick(int(sys.argv[1]))
to_die.sort()

last=-1
index=1
output=[]
for i in to_die:
  diff = i - last
  scr = diff / 7
  output += [ "[%2d] count %3d ... ( %s x+ %d ) ... kill %3d" % (index, diff, " " if scr == 0 else scr, diff % 7, i + 1) ]
  last = i
  index += 1

output += [""] * (3 - len(output) % 3)

lines = len(output) / 3 
for i in range(lines):
  print "%s\t\t%s\t\t%s" % (output[i], output[i + lines], output[i + lines*2])
  if i % 3 == 2:
    print
print "\n\n"

  
# items = [(i/4, i%4) for i in to_die]
# idx = 0
# for i in range(0,125):
#   print "ROW %3d " % (i + 1),
#   for j in range(0,4):
#     if idx < len(items):
#       row = items[idx][0]
#       col = items[idx][1]
#       if row == i and col == j:
#         print "-%d- " % (col + 1),
#         idx+=1
#         continue
#     print " .  ",
#   print " %3d ROW" % (i + 1),
#   print
#   if (i+1) % 5 == 0:
#     print
    
