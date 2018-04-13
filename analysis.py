import graphbuild
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
dynamic_path = "/graphs/businesses/pittsburgh/dynamic/"
friends = read_data(exn(friend_path, city, "csv"))
reviews = read_data(exn(review_path, city, csv))
elites = read_data(exn(elite_path, city, csv))
categories = read_data(exn(categories_path, city, csv))

users = collect.user_dictionary(reviews, elites)
businesses = collect.business_dictionary(reviews, categories)

weightedG = graphbuild.generate_weighted_friend_network(friends, users)

def get_component_length(components, n):
	sizes = [0]
	for component in iter(components):
		sizes.append(len(component))
	return sizes


def business_reviewers_dynamic(G, businesses):
	results = []
	count = 0
	with open(exn(dynamic_path, city, "csv"), "wb") as outfile:
		categories = ["business", "timestamp", "nodes", "edges", "number_connected_components", "largest", "average_clustering", "subgraph_diameter", "pct_elite", "avg_rating", "avg_rating_diff", "lc_avg_rating", "lc_avg_rating_diff", "average_edge_weight", "num_reviews", "total_reviews"]
		outfile.write(','.join(categories)+"\n")
		for business in businesses:
			patrons_dict = businesses[business]['users']
			patrons_ordered = sorted(patrons_dict.keys(), key = lambda x: min(businesses[business]['users'][x]['date'].keys()))
			seen = [] 
			size = len(patrons_ordered)
			try:
				business_avg_rating = businesses[business]['avg_rating']
			except:
				business_avg_rating = 0 
			for patron in patrons_ordered:
				seen.append(patron)
				timestamp = min(businesses[business]['users'][patron]['date'].keys())
				subgraph = G.subgraph(seen)
				nodes = nx.number_of_nodes(subgraph)
				if nodes < 5:
					continue
				result = graph_attributes(subgraph, business, timestamp)
				result.append(len(seen))
				result.append(size)
				new = ",".join(str(v) for v in result)+ "\n"
				outfile.write(new)
				results.append(result)
			if count % 100 == 0:
				print "businesses dynamically processed: " + str(count)
			count +=1 
	return None

def graph_attributes(subgraph, business, timestamp):
	nodes = nx.number_of_nodes(subgraph)
	edges = nx.number_of_edges(subgraph)
	subgraph_components = nx.connected_components(subgraph)
	number_connected_components = nx.number_connected_components(subgraph)
	largest = max(get_component_length(subgraph_components,number_connected_components))
	try:
		largest_component = max(nx.connected_component_subgraphs(subgraph), key=len)
	except:
		largest_component = subgraph
	try: 
		average_clustering = nx.average_clustering(subgraph)
	except:
		average_clustering = None
	try: 
		subgraph_diameter = nx.diameter(largest_component)
	except:
		subgraph_diameter = None
	elite_status = nx.get_node_attributes(subgraph,'elite')
	try:
		pct_elite = sum(list(map((lambda x: 0 if (elite_status[x] == None) else 1),elite_status)))*1.0/len(elite_status)
	except:
		pct_elite = None
	user_ratings_dict = nx.get_node_attributes(subgraph, 'businesses')
	user_avg_ratings_given = nx.get_node_attributes(subgraph, 'avg_rating_given')
	ratings = []
	rating_diff = []
	for user in user_ratings_dict:
		for time in user_ratings_dict[user][business]['date']:
			if time <= timestamp:
				ratings.append(user_ratings_dict[user][business]['date'][time])
				rating_diff.append(user_ratings_dict[user][business]['date'][time] - user_avg_ratings_given[user])
	avg_rating = sum(ratings)*1.0/len(ratings)
	avg_rating_diff = sum(rating_diff)*1.0/len(rating_diff)
	
	lc_user_ratings_dict = nx.get_node_attributes(subgraph, 'businesses')
	lc_user_avg_ratings_given = nx.get_node_attributes(subgraph, 'avg_rating_given')
	lc_ratings = []
	lc_rating_diff = []
	for user in lc_user_ratings_dict:
		for time in lc_user_ratings_dict[user][business]['date']:
			if time <= timestamp:
				lc_ratings.append(lc_user_ratings_dict[user][business]['date'][time])
				lc_rating_diff.append(lc_user_ratings_dict[user][business]['date'][time] - lc_user_avg_ratings_given[user])
	lc_avg_rating = sum(lc_ratings)*1.0/len(lc_ratings)
	lc_avg_rating_diff = sum(lc_rating_diff)*1.0/len(lc_rating_diff)
	edge_weights = list(map(lambda x: x[2]['weight'], nx.Graph(subgraph).edges(data=True)))
	try:
		average_edge_weight = sum(edge_weights)*1.0/len(edge_weights)
	except:
		average_edge_weight = None

	result = []
	result.append(business)
	result.append(timestamp.strftime('%m/%d/%Y'))
	result.append(nodes)
	result.append(edges)
	result.append(number_connected_components)
	result.append(largest)
	result.append(average_clustering)
	result.append(subgraph_diameter)
	result.append(pct_elite)
	result.append(avg_rating)
	result.append(avg_rating_diff)
	result.append(lc_avg_rating)
	result.append(lc_avg_rating_diff)
	result.append(average_edge_weight)
	return result 

business_reviewers_dynamic(weightedG, businesses)
