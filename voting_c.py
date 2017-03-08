from __future__ import division
def borda_score(votes_list,i,c):
	# c=0.3
	votes_list=sorted(votes_list)
	num_candidates=len(votes_list)
	first=votes_list[num_candidates-1]
	second=votes_list[num_candidates-2]
	third=votes_list[num_candidates-3]
	num_votes=sum(votes_list)
	top_votes=first+second+third
	rem_votes=(num_votes - top_votes)
	pref1_first=(first)+(first/top_votes)*rem_votes
	pref1_second=(second)+(second/top_votes)*rem_votes
	pref1_third=(third)+(third/top_votes)*rem_votes
	pref2_first=(pref1_first/(pref1_first+pref1_third))*pref1_second+(pref1_first/(pref1_first+pref1_second))*pref1_third
	pref2_second=(pref1_second/(pref1_second+pref1_third))*pref1_first+(pref1_second/(pref1_first+pref1_second))*pref1_third
	pref2_third=(pref1_third/(pref1_third+pref1_second))*pref1_first+(pref1_third/(pref1_first+pref1_third))*pref1_second
	borda_first=pref1_first+c*pref2_first
	borda_second=pref1_second+c*pref2_second
	borda_third=pref1_third+c*pref2_third
	if i == 10:
		print pref1_first
		print pref1_second
		print pref1_third
		print top_votes
		print first
		print rem_votes 
		print (first)+(first/top_votes)*rem_votes
	print borda_first/(1.3*num_votes)+borda_third/(1.3*num_votes)+borda_second/(1.3*num_votes)
	return [borda_first/((1+c)*num_votes),borda_second/((1+c)*num_votes),borda_third/((1+c)*num_votes)]
import csv

# open the file in universal line ending mode 
with open('elec.csv', 'rU') as infile:
  # read the file as a dictionary for each row ({header : value})
  reader = csv.DictReader(infile)
  data = {}
  for row in reader:
    for header, value in row.items():
      try:
        data[header].append(value)
      except KeyError:
        data[header] = [value]

#print data
# extract the variables you want
names = data['constituency']
votes = map(int, data['vote'])
borda1_avg=[]
borda2_avg=[]
borda3_avg=[]
for j in range(0,101):
	c=j/100
	count=0
	borda1=[]
	borda2=[]
	borda3=[]
	for i in xrange(0,len(votes)):
		# count=0
		if i == 0:
			votes_list=[votes[0]]
		elif names[i]==names[i-1] and i != len(votes)-1:
			votes_list.append(votes[i])
		else:
			count+=1
			[borda_first,borda_second,borda_third]=borda_score(votes_list,count,c)
			
			borda1.append(borda_first)
			borda2.append(borda_second)
			borda3.append(borda_third)
			votes_list=[votes[i]]
	borda1_avg.append(sum(borda1)/float(len(borda1)))
	borda2_avg.append(sum(borda2)/float(len(borda2)))
	borda3_avg.append(sum(borda3)/float(len(borda3)))	
print borda1

import matplotlib.pyplot as plt
import numpy as np
binwidth=0.05
plt.figure()
myList=range(0,101)
myInt=100
newList = [x / myInt for x in myList]
plt.plot(newList,borda1_avg)
plt.plot(newList,borda2_avg)
plt.plot(newList,borda3_avg)
plt.ylabel('normalised borda score');
plt.xlabel('c changing from 0 to 1')
print len(borda1_avg)
print len(newList)
plt.savefig('borda_all_c.png')
# plt.hist(borda1, normed=True, bins=np.arange(0, 1 + binwidth, binwidth))
# plt.ylabel('normalised Count');
# plt.xlabel('normalised Borda score for winner');
# plt.savefig('first.png')

# plt.figure()
# plt.hist(borda2, normed=True, bins=np.arange(0, 1 + binwidth, binwidth))
# plt.ylabel('normalised Count');
# plt.xlabel('normalised Borda score for runnerup');
# plt.savefig('second.png')

# plt.figure()
# plt.hist(borda3, normed=True, bins=np.arange(0, 1 + binwidth, binwidth))
# plt.ylabel('normalised Count');
# plt.xlabel('normalised Borda score for third candidate');
# plt.savefig('third.png')
# #latitude = data['latitude']
# #longitude = data['longitude']