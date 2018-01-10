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
