import networkx as nx
import collect 
import os

def exn(path, city, ftype):
	return os.getcwd() + path + city + "." + ftype

def read_data(name):
	opendata = open(name, 'r')
	return opendata

csv = "csv"
city = "pittsburgh"
friend_path = "/inputs/friends/friends_"
review_path = "/inputs/reviews/reivews_rated_"
elite_path = "/inputs/elites/elites_"
categories_path = "/inputs/categories/business_categories_"

friends = read_data(exn(friend_path, city, "csv"))
reviews = read_data(exn(review_path, city, csv))
elites = read_data(exn(elite_path, city, csv))
categories = read_data(exn(categories_path, city, csv))

users = collect.user_dictionary(reviews, elites)
businesses = collect.business_dictionary(reviews, categories)
count = 0


def generate_unweighted_friend_network(friends):
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

def generate_weighted_friend_network(friends, users):
	G = nx.Graph()
	friends.seek(0)
	for line in friends:
		vertices = line.split(",")
		if vertices[0] == "user_id":
			continue
		elif vertices[0] == "#NAME?" or vertices[1] == "#NAME?": #removing poorly parsed ids
			continue
		else:
			u0 = vertices[0].strip()
			u1 = vertices[1].strip()
			if u0 in users:
				businesses0 = set(users[u0]["businesses"].keys())
			else:
				businesses0 = set()
			if u1 in users:
				businesses1 = set(users[u1]["businesses"].keys())
			else:
				businesses1 = set()
			overlap = businesses0.intersection(businesses1)
			G.add_edge(u0, u1, weight = len(overlap), businesses = overlap)
	nx.set_node_attributes(G, users)
	return G 

def generate_business_network_reviews(businesses):
	G = nx.Graph()
	seen = set()
	for b0 in businesses:
		b0users = set(businesses[b0]["users"].keys())
		for b1 in businesses:
			if (b0, b1) not in seen and (b1, b0) not in seen:
				b1users = set(businesses[b1]["users"].keys())
				overlap = b0users.intersection(b1users)
				if len(overlap) == 0:
					continue
				else:
					G.add_edge(b0, b1, weight=len(overlap), common_users = overlap)
			seen.add((b0, b1))
			seen.add((b1, b0))
	nx.set_node_attributes(G, businesses)
	return G