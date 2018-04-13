import os
from datetime import datetime

def user_dictionary(reviews, elite):
	users = dict() 
	for line in reviews: 
		splits = line.split(",") #r.id, r.stars, r.date, r.business_id, r.user_id, b.name, b.stars
		review_id = splits[0]
		stars = splits[1]
		date = datetime.strptime(splits[2].strip(), "\"%Y-%m-%d 00:00:00\"")
		b_id = splits[3]
		u_id = splits[4]
		if u_id not in users:
			users[u_id] = dict()
			users[u_id]['elite'] = None
			users[u_id]['businesses'] = dict()
		if b_id not in users[u_id]['businesses']:
			users[u_id]['businesses'][b_id] = dict()
			users[u_id]['businesses'][b_id]['date'] = dict()
		users[u_id]['businesses'][b_id]['date'][date] = int(stars)
	for line in elite:
		splits = line.split(",")
		u_id = splits[0].strip()
		elite = splits[1].strip()
		try:
			users[u_id]['elite'] = int(elite)
		except:
			users[u_id]['elite'] = None
	for user in users:
		total = 0
		count = 0
		for bus in users[user]["businesses"]:
			for date in users[user]["businesses"][bus]['date']:
				count += 1
				total += users[user]["businesses"][bus]['date'][date]
		users[user]["avg_rating_given"] = total*1.0/count
	return users

def business_dictionary(reviews, categories):
	businesses = dict()
	reviews.seek(0)
	for line in categories:
		splits = line.split(",")
		b_id = splits[0].strip()
		if b_id == "business_id":
			continue
		category = splits[1].strip().replace('"', '')
		if b_id not in businesses:
			businesses[b_id] = dict()
			businesses[b_id]["users"] = dict()
			businesses[b_id]["categories"] = set()
		businesses[b_id]["categories"].add(category)
	for line in reviews:
		splits = line.split(",") #r.id, r.stars, r.date, r.business_id, r.user_id, b.name, b.stars
		review_id = splits[0]
		stars = int(splits[1])
		date = datetime.strptime(splits[2].strip(), "\"%Y-%m-%d 00:00:00\"")
		b_id = splits[3]
		u_id = splits[4]
		avg_stars = splits[6]
		try: 
			avg_stars = float(avg_stars.strip())
		except:
			avg_stars = None
		if b_id not in businesses:
			businesses[b_id] = dict()
			businesses[b_id]["users"] = dict()
			businesses[b_id]["categories"] = set()
		if u_id not in businesses[b_id]["users"]:
			businesses[b_id]["users"][u_id] = dict()
			businesses[b_id]["users"][u_id]['date'] = dict()
		businesses[b_id]["users"][u_id]['date'][date] = stars
		businesses[b_id]["avg_rating"] = avg_stars
	for bus in businesses:
		for u_id in businesses[bus]["users"]:
			count = 0
			total = 0.0
			for date in businesses[bus]["users"][u_id]['date']:
				stars = businesses[bus]["users"][u_id]['date'][date]
				count += 1 
				total += stars 
			businesses[bus]["users"][u_id]["user_avg_rating"] = total/count
	return businesses



review_path = "/inputs/reviews/reivews_rated_"
elite_path = "/inputs/elites/elites_"
categories_path = "/inputs/categories/business_categories_"

def read_data(name):
	opendata = open(name, 'r')
	return opendata

def exn(path, city, ftype):
	return os.getcwd() + path + city + "." + ftype

city = "pittsburgh"
csv = "csv"
reviews = read_data(exn(review_path, city, csv))
elites = read_data(exn(elite_path, city, csv))
categories = read_data(exn(categories_path, city, csv))
#user_dictionary(reviews, elites)
#business_dictionary(reviews, categories)