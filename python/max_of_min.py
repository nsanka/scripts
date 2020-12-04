import time
import random
from random import choices, sample

### problem set up: ###
random.seed(150)
n = 50000
space = sample(range(10000000), k=n) #list of float length n
x = 15000 # integer, less than n
# GOAL: find the max of the minima of all segments size x of the list space

### here is the starter code and runtime ###
start = time.time()
# list of all segments length x:
segs = [space[i:i+x] for i in range(n-x+1)]

# minima of segments:
min_segs = [min(seg) for seg in segs]

# max of mins:
print(max(min_segs))
print(time.time() -start)

### please insert your code here: ###
start = time.time()
found_max = 0
for i in range(n-x+1):
  curr_min = min(space[i:i+x])
  if curr_min > found_max:
    found_max = curr_min

print(found_max)
print(time.time() -start)

# Try
start = time.time()
found_max = 0
i = 0
while i < (n-x+1):
  curr_min = min(space[i:i+x])
  ind = space.index(curr_min, i, i+x)
  if curr_min > found_max:
    found_max = curr_min
  i = ind + 1

print(found_max)
print(time.time() -start)