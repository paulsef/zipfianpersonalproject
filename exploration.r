setwd("/Users/paul/Zipfian/personal_project")
source('dfs.r')
library(ggplot2)
dcom <- dcom[complete.cases(dcom[,10:41]),]
sub1 <- dcom[dcom$playcount > 1,]
ggplot(sub1) + aes(x = sub1$registered, y = sub1$playcount, color = factor(sub1$subscriber)) + 
  geom_point() + scale_y_log10()#+ scale_colour_hue(l=100, c=100)
ggplot(sub1) + aes(x = sub1$registered, y = sub1$playcount, color = factor(sub1$subscriber), 
                   size = sub1$age) + geom_point() + scale_y_log10()

subscriber <- dcom[dcom$subscriber == 1,]
user <- dcom[dcom$subscriber == 0,]
ggplot(subscriber) + aes(x = subscriber$registered, y = subscriber$age, color = factor(subscriber$gender), 
                   size = subscriber$top_count1) + geom_point()



t_sub <- as.data.frame(table(subscriber$tag1))
t_use <- as.data.frame(table(user$tag1))
subscriber_tags <- t_sub[order(t_sub$Freq, decreasing = TRUE),'Var1']
user_tags <-  t_use[order(t_use$Freq, decreasing = TRUE),'Var1']

cp <- dcom
cp$tag1 <- factor(dcom$tag1,levels = t[order(t$Freq, decreasing = TRUE),'Var1'])

# histogram of active users
dcom$reg_recent_diff = as.numeric(dcom$recent_date1 -dcom$registered, units = "days")
# what are people with NO recent tracks? nothing scrobbled ever?
recent <- dcom[(dcom$reg_recent_diff < 1000)&(dcom$reg_recent_diff > 1)&(!is.na(dcom$reg_recent_diff)),]
ggplot(recent, aes(x = reg_recent_diff)) + geom_histogram() + scale_y_sqrt()

# histrogram of playcounts
ggplot(subscriber, aes(x = playcount + 1)) + geom_histogram() + scale_x_log10()
ggplot(user, aes(x = playcount + 1)) + geom_histogram() + scale_x_log10()

model <- dcom[dcom$playcount > 2,c('playcount', 'subscriber') ]
#model$tag1 <- factor(model$tag1)
m <- glm(subscriber ~ playcount, data = model, family = 'binomial')

sub_agg <- aggregate(top_count1 ~ tag1, data = subscriber, FUN = mean)
use_agg <- aggregate(top_count1 ~ tag1, data = user, FUN = mean)
melted_agg <- melt(merge(sub_agg, use_agg, by = 'tag1', all = TRUE), id= 'tag1')
melted_agg[is.na(melted_agg)] <- 0
ggplot(melted_agg) + aes(x = melted_agg$tag1, y = melted_agg$value, fill = melted_agg$variable) + 
  geom_bar(stat='identity',position = 'dodge') + theme(axis.text.x = element_text(angle = 90, hjust = 1))

dcom$month_registered <- strftime(dcom$registered, format = '%H')
subscriber <- dcom[dcom$subscriber == 1,]
user <- dcom[dcom$subscriber == 0,]
ggplot(subscriber,aes(x = month_registered)) + geom_histogram()
ggplot(user,aes(x = month_registered)) + geom_histogram()

# dcom$reg_recent_diff <- as.numeric(dcom$recent_date1 -dcom$registered, units = "days")
# diff <- data.frame(as.numeric(dcom$recent_date1 - dcom$recent_date2, units = "hours"), 
#   as.numeric(dcom$recent_date2 - dcom$recent_date3, units = "hours"),
#   as.numeric(dcom$recent_date3 - dcom$recent_date4, units = "hours"), 
#   as.numeric(dcom$recent_date4 - dcom$recent_date5, units = "hours"), row.names = c('d1','d2','d3','d3'))
# dcom$avg_diff <- transform(dcom, avg_diff)
# dcom$avg_diff <- mean(diff)

subscriber <- dcom[dcom$subscriber == 1,]
user <- dcom[dcom$subscriber == 0,]
#recent <- dcom[(dcom$reg_recent_diff < 1000)&(dcom$reg_recent_diff > 1)&(!is.na(dcom$reg_recent_diff)),]
ggplot(subscriber, aes(x = reg_recent_diff)) + geom_histogram() + scale_y_sqrt()
ggplot(user, aes(x = reg_recent_diff)) + geom_histogram() + scale_y_sqrt()

ggplot(subscriber, aes(x = avg_diff)) + geom_histogram()
ggplot(user, aes(x = avg_diff)) + geom_histogram()

ggplot(dcom) + aes(x = rownames(dcom), y= dcom$top_count4, color = dcom$subscriber) +
  geom_point() + scale_y_log10()
