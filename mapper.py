#!/usr/bin/env python

"""
Based on:
https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
"""

import sys

Data = {}
lines = sys.stdin.readlines()

for line in lines:
    data = line.replace("\n", "").split("\t")
    if data[1] == "" : Data.update({data[0]:[]})
    else : Data.update({data[0]:data[1].split(",")})
for person,personsFriends in Data.items():
    sugestedFriends = []
    for eachFriend in personsFriends:
        newFriend = list(set(Data[eachFriend]) - set(personsFriends) - set(person))
        if (newFriend) : 
            sugestedFriends.extend(newFriend)
            if (person in sugestedFriends):
                sugestedFriends.remove(person)
    print (person + "\t" + str(sugestedFriends))
