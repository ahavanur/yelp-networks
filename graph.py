#script that generates the network of friends in yelp data
#and then generates their influenced/influencer scores
#influenced scores are calculated as the percentage of their reviews that 
#come after their friends' 
#influencers is the reverse, i.e how many of their friends reviewed a business after them 
#results are exported into a csv file for ease of analysis
import networkx as nx
from datetime import datetime
import os
import glob 

def exn(path, city, ftype):
	return os.getcwd() + path + city + "." + ftype

def read_data(name):
	opendata = open(name, 'r')
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
	for user in users:
		influenced = 0.0
		influencer = 0.0
		if user in G:
			friends = G[user]
			reviews = users[user]
			num_friends = len(friends)
			num_reviews = len(users[user])
			for business in reviews:
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
			user_scores[user] = (influenced/num_reviews, influencer/num_reviews, num_friends, num_reviews)
	return user_scores

def calculate_influence_ratio(G, businesses, users):
	user_scores = dict()
	for user in users:
		if user in G:
			user_scores[user] = dict()
			friends = G[user]
			reviews = users[user]
			for business in reviews:
				f1 = 0 
				f2 = 0
				m = 0 
				user_review_date = users[user][business]
				business_reviewers = businesses[business]
				for business_reviewer in business_reviewers:
					review_date = business_reviewers[business_reviewer]
					if review_date < user_review_date:
						m += 1 
					if business_reviewer in friends:
						if review_date < user_review_date:
							f1 += 1
						else:
							f2 += 1
				f3 = len(friends) - f1 - f2
				n = len(business_reviewers) - m
				k = nx.number_of_nodes(G) - len(business_reviewers)
				user_scores[user][business] = (f1, f2, f3, m, n, k)
	return user_scores


def calculate_clique_score(G, businesses):
	business_scores = dict()
	for business in businesses:
		patrons = businesses[business]
		nodes = len(patrons)
		if nodes > 1:
			subgraph = G.subgraph(patrons)
			edges = len(subgraph.edges())
			business_scores[business] = [2.0*edges/(nodes*(nodes-1)), nodes]
	return business_scores

def business_review_networks(G, businesses, path):
	subgraph_dict = dict()
	for business in businesses:
		patrons = businesses[business]
		nodes = len(patrons)
		if nodes > 1:
			subgraph = G.subgraph(patrons)
			number_connected_components = nx.number_connected_components(subgraph)
			subgraph_components = nx.connected_components(subgraph)
			largest = max(get_component_length(subgraph_components,number_connected_components))
			subgraph_dict[business] = [number_connected_components, largest]
			di_subgraph = nx.DiGraph()
			for patron in subgraph.nodes():
				friends = subgraph.neighbors(patron)
				patron_date = businesses[business][patron]
				for friend in friends:
					friend_date = businesses[business][friend]
					min_date = min(patron_date, friend_date)
					max_date = max(patron_date, friend_date)
					if friend_date == min_date:
						di_subgraph.add_edge(friend,patron)
					else:
						di_subgraph.add_edge(patron,friend)
			name = os.getcwd() + path + business.replace('"', '') + "_patrons.gml"
		#	nx.write_gml(subgraph, name)
	return None

def ratio_output(user_scores, categories, outfile_name):
	print "preparing csv file"
	with open(outfile_name, "wb") as outfile:
		cats = ""
		for cat in categories:
			cats += str(cat)
			cats += ","
		cats = cats[:-1] + "\n"
		outfile.write(cats)
		for user in user_scores:
			for business in user_scores[user]:
				attributes = len(user_scores[user][business])
				line = str(user) + ',' + str(business) + ','
				for i in xrange(attributes):
					line += str(user_scores[user][business][i])
					line += ","
				line = line[:-1] + "\n"
				outfile.write(line)
	return "Finished"
				
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

def get_component_length(components, n):
	sizes = [0]
	for component in iter(components):
		sizes.append(len(component))
	return sizes

def main():
	city = "pittsburgh"
	review_path = "/inputs/reviews/reviews_"
	friend_path = "/inputs/friends/friends_"
	city_graph_path = "/graphs/cities/network_"
	business_graph_path = "/graphs/businesses/" + city + "/"
	component_length_path = "/outputs/components/component_length_"
	influence_path = "/outputs/influence/influence_ratios_"
	clique_path = "/outputs/clique/clique_"
	influence_ratio_path = "/outputs/influence_ratio/influence"
	friends = read_data(exn(friend_path, city, "csv"))
	reviews = read_data(exn(review_path, city, "csv"))
	print "finished reading data"
	G = generate_network(friends)
	print "generated social network"
	print nx.number_connected_components(G)
	print nx.number_of_nodes(G)
	print nx.number_of_edges(G)
	nx.write_gml(G, exn(city_graph_path, city, "gml"))
	print "wrote graph"
	businesses = generate_dict(reviews)
	users = generate_dict(reviews, user_dict=True)
	business_review_networks(G, businesses, business_graph_path)
	print len(businesses)
	print len(users)
	print "processed reviews"
	scores = calculate_influence(G, businesses, users)
	ratios = calculate_influence_ratio(G, businesses, users)
	cliqueness = calculate_clique_score(G, businesses)
	print len(scores)
	print "calculated influence scores"
	output(cliqueness, ["business_id", "cliqueness", "reviewers"], exn(clique_path, city, "csv"))
	output(scores, ["user_id", "influenced_score", "influencer_score", "total_friends", "total_reviews"], exn(influence_path, city, "csv"))
	ratio_output(ratios, ["user_id", "business_id", "f1", "f2", "f3", "m", "n", "k"], exn(influence_ratio_path, city, "csv"))
	return None 

main()
