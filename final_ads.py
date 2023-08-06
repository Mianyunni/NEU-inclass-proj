# CS5001 final project, Matching ads and viewers
# Mianyun Ni 12/06/2022

import csv

class Queue:
    def __init__(self, items: list = []):
        self.items = items
    
    def enqueue(self, item: int):
        self.items.append(item)
    
    def dequeue(self):
        item = self.items[0]
        self.items = self.items[1:]
        return item
    
    def is_empty(self):
        return len(self.items) == 0

class Viewer:
    def __init__(self, name, isyoung, isman, iscatowner):
        self.name = name
        self.isyoung = isyoung
        self.isman = isman
        self.iscatowner = iscatowner

class Ads:
    def __init__(self, name, isforyoung, isforman, havecat):
        self.name = name
        self.isforyoung = isforyoung
        self.isforman = isforman
        self.havecat = havecat

# Returns viewer_ranking base on target ads
# for loop Viewerlist, rank it base on how many attributes matches target ads's attributes
def rank_viewer(ads, viewerlist):
    n = len(viewerlist)
    rankingdict = {}
    for i in range(n):
        count = 0
        if (ads.isforyoung == viewerlist[i].isyoung):
            count += 1
        if (ads.isforman == viewerlist[i].isman):
            count += 1
        if (ads.havecat == viewerlist[i].iscatowner):
            count += 1
        rankingdict[i + n] = count
    return list(dict(sorted(rankingdict.items(), key = lambda x:x[1], reverse = True)).keys())

# Return ads_ranking base on target viewer
# for loop adslist, rank it base on how many attributes matches target viewer's attributes
def rank_ads(viewer, adslist):
    n = len(adslist)
    rankingdict = {}
    for i in range(n):
        count = 0
        if (viewer.isyoung == adslist[i].isforyoung):
            count += 1
        if (viewer.isman == adslist[i].isforman):
            count += 1
        if (viewer.iscatowner == adslist[i].havecat):
            count += 1
        rankingdict[i] = count
    return list(dict(sorted(rankingdict.items(), key = lambda x:x[1], reverse = True)).keys())

# Returns True if viewer prefers ads i over 
# the one the currently have.
# Returns false otherwise.
def viewer_prefers_i_over_current(viewer_ranking, i, current):
    for ranking in viewer_ranking.items:
        if ranking == i:
            return True
        if ranking == current:
            return False


def find_matches(viewer_preferences, ads_preferences, viewerlist, adslist):
    n = len(ads_preferences)
    current_matches = [-1] * len(viewer_preferences)
    available_ads = [True] * len(viewer_preferences)
    # while there are any available ads
    while True in available_ads:
         # pick the first available ads
        available_ads_idx = available_ads.index(True)
         # loop through that ads'queue of viewer preferences
        while True: 
            viewer_id = ads_preferences[available_ads_idx].dequeue() - n
               # if the viewer is free
            if current_matches[viewer_id] == -1:
                    # make this match:
                    # update current_matches
                current_matches[viewer_id] = available_ads_idx
                    # mark the ads as taken
                available_ads[available_ads_idx] = False
                break
               # if the viewer is not free
            else:
                    # if viewer prefers this ads over the one they currently have
                current_match = current_matches[viewer_id]
                if viewer_prefers_i_over_current(viewer_preferences[viewer_id - n], available_ads_idx, current_match):
                          # update current_matches
                    current_matches[viewer_id] = available_ads_idx
                          # mark the previous ads as available
                    available_ads[current_match] = True
                          # mark the current ads as taken
                    available_ads[available_ads_idx] = False
                    break
    print("Viewer\tAds")
    for i in range(n):
        print(viewerlist[i].name,"\t", adslist[current_matches[i]].name)

# 1.Read in viewerlist.csv and adslist.csv from second line(first line is title)
# 2.Create n viewers and n ads with spcific attributes, 0 is false, 1 is true
# 3.Each viewers, use rank_ads to generte it's preference
# 4.Each ads, use rank_viewers to generte it's preference
# 5.use inclass matching alogrithm match and output result
def main():
    viewerlist = []
    adslist = []
    viewer_preferences = []
    ads_preferences = []
    n = 4
    with open('./viewerlist.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            viewerlist.append(Viewer(line[0], line[1], line[2], line[3]))
            
    with open('./adslist.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            adslist.append(Ads(line[0], line[1], line[2], line[3]))
            
    for i in range(n):
        viewer_preferences.append(Queue(rank_ads(viewerlist[i], adslist)))   
        ads_preferences.append(Queue(rank_viewer(adslist[i], viewerlist)))
    find_matches(viewer_preferences, ads_preferences, viewerlist, adslist)

if __name__ == "__main__":
    main()
