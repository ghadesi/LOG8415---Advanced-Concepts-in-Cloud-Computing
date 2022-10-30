#!/usr/bin/env python

"""
Based on:
https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
"""

import sys
from collections import Counter
maxFriend = 10
for line in sys.stdin:
    line = line.strip()
    data = line.split('\t')
    friends = data[1].strip("][").replace("'", "").split(', ')
    TenFirstFriendWithCounter = sorted(Counter(friends).most_common(), key=lambda x: (-x[1], x[0]))
    suggestedFriend = str(data[0]) + "\t"
    numbeOfFriend = 0
    for i in TenFirstFriendWithCounter:
        if numbeOfFriend == maxFriend: break
        suggestedFriend += str(i[0]) + ','
        numbeOfFriend += 1

    print(suggestedFriend[:-1])
