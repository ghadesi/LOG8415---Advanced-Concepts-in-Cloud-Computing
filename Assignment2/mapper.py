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

#Here we need to have all friends of friends of each person witouh having his/her friends. There is housands of way to do that. One easy way is use set1-set2:
#Sets, unlike lists or tuples, cannot have repeated element. 
#set1 - set2 return the set that results when any elements in x2 are removed from x1
#So if we have friends of a friend and remove all direct friends of person of it, it will be our result. Of course can not have the person himself in his segussted friends!
for person,personsFriends in Data.items():
    sugestedFriends = []
    for eachFriend in personsFriends:
        newFriend = list(set(Data[eachFriend]) - set(personsFriends) - set(person))
        if (newFriend) : 
            sugestedFriends.extend(newFriend)
    print (person + "\t" + str(sugestedFriends))
