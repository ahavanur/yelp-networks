#script that generates the network of friends in yelp data
#and then generates their influenced/influencer scores
#influenced scores are calculated as the percentage of their reviews that 
#come after their friends' 
#influencers is the reverse, i.e how many of their friends reviewed a business after them 
#results are exported into a csv file for ease of analysis

import networkx as nx
from datetime import datetime

def read_data(data):
	opendata = open(data, 'r')
	return opendata

def generate_network(friends):
	G = nx.Graph()
	for line in friends:
		vertices = line.split(",")
		if vertices[0] == "user_id":
			continue
		elif vertices[0] == "#NAME?" or vertices[1] == "#NAME?": #removing poorly parsed ids
			continue
		else:
			G.add_edge(vertices[0].strip(), vertices[1].strip())
	return G

def generate_dict(reviews, user_dict=False):
	result_dict = dict()
	reviews.seek(0) #resets cursor back to beginning of file
	for line in reviews: 
		review = line.split(",")
		if review[0] == "business_id":
			continue
		elif review[0] == "#NAME?" or review[1] == "#NAME?":
			continue
		else:
			b_id = review[0]
			u_id = review[1]
			if user_dict:
				pkey = u_id
				skey = b_id
			else:
				pkey = b_id
				skey = u_id
			date = datetime.strptime(review[2].strip(), "\"%Y-%m-%d 00:00:00\"")
			if pkey not in result_dict:
				result_dict[pkey] = {skey:date}
			else:
				if skey in result_dict[pkey]:
					result_dict[pkey][skey] = min(result_dict[pkey][skey], date)
				else:
					result_dict[pkey][skey] = date
	return result_dict

def calculate_influence(G, businesses, users):
	user_scores = dict()
	count = 0
	for user in users:
		influenced = 0.0
		influencer = 0.0
		total = 0.0
		count += 1
		if user in G:
			friends = G[user]
			for business in users[user]:
				user_review_date = users[user][business]
				business_reviewers = businesses[business]
				was_influenced = False
				was_influencer = False
				for friend in friends:
					if friend in business_reviewers:
						friend_review_date = businesses[business][friend]
						if user_review_date <= friend_review_date:
							was_influencer = True
						else:
							was_influenced = True
				influencer += float(was_influencer)
				influenced += float(was_influenced)
				total += 1.0
			if total == 0.0:
				user_scores[user] = (0.0, 0.0, len(friends), len(users[user]))
			else:
				user_scores[user] = (influenced/total, influencer/total, len(friends), len(users[user]))
	return user_scores

def output(user_scores, categories, outfile_name):
	print "preparing csv file"
	with open(outfile_name, "wb") as outfile:
		cats = ""
		for cat in categories:
			cats += str(cat)
			cats += ","
		cats = cats[:-1] + "\n"
		outfile.write(cats)
		for user in user_scores:
			attributes = len(user_scores[user])
			line = str(user) + ','
			for i in xrange(attributes):
				line += str(user_scores[user][i])
				line += ","
			line = line[:-1] + "\n"
			outfile.write(line)
	return "Finished"

def main():
	friends = read_data("pittsburgh_friends.csv")
	reviews = read_data("reviews_pittsburgh.csv")
	print "finished reading data"
	G = generate_network(friends)
	print nx.number_of_nodes(G)
	print nx.number_of_edges(G)
	print "generated social network"
	businesses = generate_dict(reviews)
	users = generate_dict(reviews, user_dict=True)
	print len(businesses)
	print len(users)
	print "processed reviews"
	scores = calculate_influence(G, businesses, users)
	print len(scores)
	print "calculated influence scores"
	#return output(scores, ["user_id", "influenced_score", "influencer_score", "total_friends", "total_reviews"], "influence_small.csv")
print main()
