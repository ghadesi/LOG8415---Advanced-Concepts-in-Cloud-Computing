#!/usr/bin/env python

"""
Based on:
https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
"""

import sys

Data = {}
#Takes input here
lines = sys.stdin.readlines()

#First convert file to a proper format list
#The format in each line is this: (Persion ID)(TAB)(Friend,Friend,Friend,...)
#So first of all we should split data by "/t" to have each person and his/her friend in a list so It's like : {'Person_ID': ['Friend_ID', 'Friend_ID',...],...}
#I case if a person does not have any friend just put a empty value for person_ID key.
for line in lines:
    data = line.replace("\n", "").split("\t")
    if data[1] == "" : Data.update({data[0]:[]})
    else : Data.update({data[0]:data[1].split(",")}
             
for person,personsFriends in Data.items():
    sugestedFriends = []
    for eachFriend in personsFriends:
        newFriend = list(set(Data[eachFriend]) - set(personsFriends) - set(person))
        if (newFriend) : 
            sugestedFriends.extend(newFriend)
            if (person in sugestedFriends):
                sugestedFriends.remove(person)
    print (person + "\t" + str(sugestedFriends))
