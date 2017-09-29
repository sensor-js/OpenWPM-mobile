import pandas as pd
import numpy as np
import urllib2
import wget
import re2
import os
import sys
from adblockparser import AdblockRules

# install adblockparser from https://github.com/scrapinghub/adblockparser plue re2



if len(sys.argv)<3:
    print "Wrong format: python *.py filterfile inputfile"
    exit()
                
# generate filter list
filter_list=set()
filename=sys.argv[1]
f=open(filename,'r')
for l in f:
    if len(l)==0 or l[0]=='!': #ignore these line
        continue
    else:
        filter_list.add(l.strip())
f.close()
print 'Total Rules: ',len(filter_list)

# create the rule filter object
rules = AdblockRules(list(filter_list))

# check all the scripts inside the file
script_result=np.array([])
filename=sys.argv[2]
fin=open(filename,'r')
fout=open('stats_'+filename,'w')
for l in fin:
    u=l.strip()
    if u=="":
        continue
    b=1 if rules.should_block(u) else 0 #{'script': False}, 'image': True, 'third-party': True, 'object-subrequest': True
    if script_result.size==0:
        script_result=np.array([u,b])
    else:
        script_result=np.vstack((script_result,np.array([u,b])))
    print >>fout,u,b
fin.close()
if script_result.size>0:
    print >>fout,'Total scripts blocked: ',np.sum(np.double(script_result[:,1])), ' out of ',script_result.shape[0]
else:
    print >>fout,'No script blocked'
fout.close()
