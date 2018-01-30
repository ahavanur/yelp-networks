library(sqldf)
friend_review = read.csv("influence.csv")
hist(friend_review$influenced_score)
hist(friend_review$influencer_score)
summary(friend_review$influenced_score)
summary(friend_review$influencer_score)
summary(friend_review$total_friends)
quantile(friend_review$total_friends, seq(0,1,0.1))
p99friends = friend_review[which(friend_review$total_friends <= quantile(friend_review$total_friends, seq(0,1,0.01))[100]),]
score_by_friends = sqldf("SELECT total_friends, AVG(influenced_score) as influenced_score, AVG(influencer_score) as influencer_score, COUNT(1) as num FROM p99friends GROUP BY 1")
plot(score_by_friends$total_friends, score_by_friends$influenced_score)
plot(score_by_friends$total_friends, score_by_friends$influencer_score)

p99reviews = friend_review[which(friend_review$total_reviews <= quantile(friend_review$total_reviews, seq(0,1,0.01))[100]),]
score_by_reviews = sqldf("SELECT total_reviews, AVG(influenced_score) as influenced_score, AVG(influencer_score) as influencer_score, COUNT(1) as num FROM p99reviews GROUP BY 1")
plot(score_by_reviews$total_reviews, score_by_reviews$influenced_score)
plot(score_by_reviews$total_reviews, score_by_reviews$influencer_score)

score_by_friends$cummulative_influenced = cumsum(score_by_friends$influenced_score*score_by_friends$num)/cumsum(score_by_friends$num)
score_by_friends$cummulative_influencer = cumsum(score_by_friends$influencer_score*score_by_friends$num)/cumsum(score_by_friends$num)

plot(score_by_friends$total_friends, score_by_friends$cummulative_influenced)
plot(score_by_friends$total_friends, score_by_friends$cummulative_influencer)


score_by_reviews$cummulative_influenced = cumsum(score_by_reviews$influenced_score*score_by_reviews$num)/cumsum(score_by_reviews$num)
score_by_reviews$cummulative_influencer = cumsum(score_by_reviews$influencer_score*score_by_reviews$num)/cumsum(score_by_reviews$num)

plot(score_by_reviews$total_reviews, score_by_reviews$cummulative_influenced)
plot(score_by_reviews$total_reviews, score_by_reviews$cummulative_influencer)

comp = read.csv("component_lengths.csv")
View(comp)
sum(comp)


new = read.csv("new_influence_score_pittsburgh.csv")
business_categories = read.csv("business_categories_pittsburgh.csv")
elite_members = read.csv("pittsburgh_elites.csv")
new$mu1 = new$f2/(new$f2+new$f3)
new$mu2 = new$n/(new$n+new$k)
View(new)
plot(new$mu1, new$mu2)
library(sqldf)
new_by_user = sqldf("SELECT user_id, AVG(mu1) as mu1, AVG(mu2) as mu2 FROM new GROUP BY 1")
new_by_user_raw = sqldf("SELECT user_id, SUM(f1) as f1, SUM(f2) as f2, SUM(f3) as f3, SUM(m) as m, SUM(n) as n, SUM(k) as k FROM new GROUP BY 1")
new_by_user_raw$mu1 = new_by_user_raw$f2/(new_by_user_raw$f2 + new_by_user_raw$f3)
new_by_user_raw$mu2 = new_by_user_raw$n/(new_by_user_raw$n + new_by_user_raw$k)
new_by_user_raw$is_elite = as.numeric(new_by_user_raw$user_id %in% unique(elite_members$user_id))

plot(new_by_user$mu1, new_by_user$mu2)
plot(new_by_user_raw$mu1, new_by_user_raw$mu2)

new_by_business = sqldf("SELECT business_id, AVG(mu1) as mu1, AVG(mu2) as mu2 FROM new GROUP BY 1")
new_by_business_raw = sqldf("SELECT business_id, SUM(f1) as f1, SUM(f2) as f2, SUM(f3) as f3, SUM(m) as m, SUM(n) as n, SUM(k) as k FROM new GROUP BY 1")

new_by_business_raw$mu1 = new_by_business_raw$f2/(new_by_business_raw$f2 + new_by_business_raw$f3)
new_by_business_raw$mu2 = new_by_business_raw$n/(new_by_business_raw$n + new_by_business_raw$k)
plot(new_by_business$mu1, new_by_business$mu2)
business_categories = read.csv("business_categories_pittsburgh.csv")
elite_members = read.csv("pittsburgh_elites.csv")
