#!/usr/bin/env python

"""
Based on:
https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
"""

import sys
from collections import Counter

#From mapper we have: {'Person_ID': ['Friend_ID', 'Friend_ID',...],...}. Here we want to have most repeated elements for each person. (The first 10 ones as mention in homwork.)
#First of all get line, split data by "\t" to have both person_id and friends.
#To make work easier, map our data to list of integer instead of str.
#The rest is magic of python.  Counter will give you the count of each of the elements in the tuple given. Also has a method call "most_common" to sort result base on key number of repetitions
#First we use most_common(10) and give first 10 anwers and it is not kind of true because the value is not ascending sort wehn value is same.
# In second try we first sort friends and then run .most_common(10). It worked well on our pc but not result is not sorted after map-reducer. We don't know why.
#In our last try we just do Counter(friends).most_common() and get all result. Then sort it by sorted() function. 
# Lambda functions are created, used, and immediately destroyed. sorted method sort base on (-x[1], x[0]). it means first elemtns with higher number of repetitions and then in same number of repetitions, lower number of user_id
# Next select first 10 values of all sorted found sugested friends.
maxFriend = 10
for line in sys.stdin:
    line = line.strip()
    data = line.split('\t')
    friends = data[1].strip("][").replace("'", "").split(', ')
    if not(len(friends)== 1 and friends[0] == ''):
                friends = list(map(int, friends))
    TenFirstFriendWithCounter = sorted(Counter(friends).most_common(), key=lambda x: (-x[1], x[0]))
    suggestedFriend = str(data[0]) + "\t"
    numbeOfFriend = 0
    for i in TenFirstFriendWithCounter:
        if numbeOfFriend == maxFriend: break
        suggestedFriend += str(i[0]) + ','
        numbeOfFriend += 1

    print(suggestedFriend[:-1] + "\n")
