import random
import sys
import sets

def weighted_pick(count):
  ratio = 5.0  # the ratio of probability of killing first over killing the last
  raw_weight = [ratio - (ratio - 1.0) * i / 499 for i in range(500)]
  total = sum(raw_weight)
  weight = [w * 1.0 / total for w in raw_weight]  # normalize

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
index=0
for i in to_die:
  print "count %3d ... kill %3d" % (i - last, i + 1)
  last = i
  index = index - 1
  if index % 3 == 0:
    print

# No longer need to display in columnar style, WeChat has changed
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
    
