library(dplyr)
data = read.csv("pittsburgh.csv")
head(data)
clustering_diff = data %>% group_by(business) %>% summarize(coef_difference = last(clustering_coefficient)-first(clustering_coefficient), time_diff = difftime(last(timestamp), first(timestamp))) 
plot(clustering_diff$time_diff, clustering_diff$coef_difference)
largest_component_diff = data %>% group_by(business) %>% summarize(component_difference = last(largest_connected_component)-first(largest_connected_component), time_diff = difftime(last(timestamp), first(timestamp))) 
plot(largest_component_diff$time_diff, largest_component_diff$component_difference)
data$avg_component_size = data$nodes/data$number_connected_components
data$prop_largest_component = data$largest_connected_component/data$nodes
data$prop_reviews = data$num_reviews/data$total_reviews
plot(data$prop_reviews, data$prop_largest_component)
data$rounded_prop_reviews = round(data$prop_reviews,3)
prop_review = data %>% group_by(rounded_prop_reviews) %>% summarise(mean_prop_largest_component = mean(prop_largest_component), 
                                                                    mean_component_size = mean(avg_component_size), 
                                                                    mean_num_components = mean(number_connected_components), 
                                                                    mean_diameter = mean(diameter))
plot(prop_review$rounded_prop_reviews, prop_review$mean_prop_largest_component)
plot(prop_review$rounded_prop_reviews, prop_review$mean_component_size)
plot(prop_review$rounded_prop_reviews, prop_review$mean_num_components)
plot(prop_review$rounded_prop_reviews, prop_review$mean_diameter)

num_review = data %>% group_by(num_reviews) %>% summarise(mean_prop_largest_component = median(prop_largest_component), 
                                                                   mean_component_size = median(avg_component_size), 
                                                                   mean_num_components = median(number_connected_components), 
                                                                   mean_diameter = median(diameter))
plot(num_review$num_reviews, num_review$mean_prop_largest_component)
plot(num_review$num_reviews, num_review$mean_component_size)
plot(num_review$num_reviews, num_review$mean_num_components)
plot(num_review$num_reviews, num_review$mean_diameter)


time_deltas = data %>%
  group_by(business) %>%
  mutate(time_diff = c(NA, diff(timestamp)), coef_diff = c(NA, diff(clustering_coefficient)), component_difference = c(NA, diff(largest_connected_component)), prop_component_difference = c(NA, diff(prop_largest_component)))

time_deltas$rounded_time = round(time_deltas$time_diff/30,2)
plot(time_deltas$rounded_time, time_deltas$prop_largest_component)

agg_time_deltas = time_deltas %>% group_by(rounded_time) %>% summarise(
                                                                   mean_coef_diff = mean(coef_diff), 
                                                                   mean_component_diff = mean(component_difference),
                                                                   mean_prop_components_diff = mean(prop_component_difference))
plot(agg_time_deltas$rounded_time, agg_time_deltas$mean_coef)
plot(agg_time_deltas$rounded_time, agg_time_deltas$mean_component)
plot(agg_time_deltas$rounded_time, agg_time_deltas$mean_prop_components)