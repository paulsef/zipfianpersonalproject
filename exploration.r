setwd("/Users/paul/Zipfian/personal_project")
source('dfs.r')
library(ggplot2)
library(reshape2)
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

dcom$reg_recent_diff <- as.numeric(dcom$recent_date1 -dcom$registered, units = "days")
# diff <- data.frame(as.numeric(dcom$recent_date1 - dcom$recent_date2, units = "hours"), 
#   as.numeric(dcom$recent_date2 - dcom$recent_date3, units = "hours"),
#   as.numeric(dcom$recent_date3 - dcom$recent_date4, units = "hours"), 
#   as.numeric(dcom$recent_date4 - dcom$recent_date5, units = "hours"), row.names = c('d1','d2','d3','d3'))
# dcom$avg_diff <- transform(dcom, avg_diff)
# dcom$avg_diff <- mean(diff)
ggplot(subscriber, aes(x = reg_recent_diff)) + geom_histogram() #+ scale_y_sqrt()

subscriber <- dcom[dcom$subscriber == 1,]
user <- dcom[dcom$subscriber == 0,]
#recent <- dcom[(dcom$reg_recent_diff < 1000)&(dcom$reg_recent_diff > 1)&(!is.na(dcom$reg_recent_diff)),]
ggplot(subscriber, aes(x = reg_recent_diff)) + geom_histogram() + scale_y_sqrt()
ggplot(user, aes(x = reg_recent_diff)) + geom_histogram() + scale_y_sqrt()

ggplot(subscriber, aes(x = avg_diff)) + geom_histogram()
ggplot(user, aes(x = avg_diff)) + geom_histogram()

melted <- melt(data=dcom[,c('friend_sub', 'subscriber')], id.vars='subscriber',value.name='friend_sub', )
ggplot(dcom) + aes(x = dcom$friend_count, y= dcom$friend_sub, color = dcom$subscriber) +
  geom_jitter() + scale_x_log10() + scale_y_log10()#geom_point(position = jitter) 


final <- read.table('final_test.csv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
subs <- final[final$probs > .60,]
sorted <- subs[order(subs$probs, decreasing = TRUE) , ]

f <- final[(final$rock > .1 | final$indie > .1 | final$electronic > .1 |
            final$folk > .1 | final$jazz > .1),c('playcount','probs', 'hour_registered','top_genres')]
f$modded <- f$top_genres
change <- function(x){if (!(x %in% c('rock', 'indie', 'electronic')) 'other' else x}
f$modded <- sapply(f$top_genre, change)
f <- sorted[((sorted$top_genres == 'rock' | sorted$top_genres == 'indie' | sorted$top_genres == 'electronic')&
              (sorted$avg_diff_hours <1000)), c('playcount','probs', 'avg_diff_hours','top_genres')]
melted <- melt(data=f, id.vars=c('playcount', 'probs', 'use_diff_days'))

ggplot(f) + aes(x = f$avg_diff_hours, y = f$playcount, size = f$probs, color = f$top_genres) + geom_jitter() +
  scale_x_log10()

ggplot(final) + aes(x = final$avg_diff_hours, y = final$playcount, size = final$probs, color = factor(final$subscriber)) + geom_jitter() +
  scale_x_log10()
ggplot(final) + aes(x = final$use_diff_days, y = final$playcount, size = final$probs, color = factor(final$subscriber)) + geom_jitter() 
ggplot(final) + aes(x = final$playcount, y = final$age, size = final$probs, color = factor(final$subscriber)) + geom_jitter() +
  scale_x_log10()
ggplot(final) + aes(x = final$hour_registered, y = final$probs, color = factor(final$subscriber)) + 
  geom_point()#,  size = final$probs,) + geom_jitter() #+
  #scale_x_log10()
  
counts <- as.data.frame(table(dcom$subscriber))
counts$Var1 <- c('User', 'Subscriber')
count_plot <- ggplot(counts) + aes(x = counts$Var1, y=counts$Freq) + geom_bar(stat = 'identity', fill = 'white') + 
  theme(plot.background = element_rect(fill='#D20039'), panel.background = element_rect(fill='#D20039'),
        axis.text=element_text(colour="white"), axis.title.y = element_text(color = 'white'), panel.border = theme_blank()) + 
  xlab('') + ylab('Frequency')
ggsave(filename='./presentation/uservsubs.jpg',plot=count_plot)
dev.off()

playcount_hist <- ggplot(dcom) + aes(x = dcom$playcount) + geom_histogram(fill = 'white') + scale_y_sqrt() + scale_x_sqrt() + 
  theme(plot.background = element_rect(fill='#D20039'), 
        panel.border = element_blank(),
        panel.background = element_rect(fill='#D20039'),
        axis.text=element_text(colour="white"), 
        axis.title = element_text(color = 'white', face = 'bold',size=20), 
        panel.grid.major = element_blank(),  
        panel.grid.minor = element_blank()) + 
  xlab('Playcount') + ylab('Frequency')
playcount_hist
ggsave(filename= './presentation/playcount_hist.jpeg', plot=playcount_hist)
dev.off()

regvplaycount <- ggplot(final) + aes(x = final$use_diff_days, y = final$playcount, size = final$probs, color = factor(final$subscriber)) +
  geom_jitter() + theme(plot.background = element_rect(fill='#D20039'), 
                        panel.background = element_rect(fill='#D20039'),
                        panel.border = element_blank(),
                        axis.text=element_text(colour="white"), 
                        axis.title = element_text(color = "white"),
                        legend.background = element_rect(fill = '#D20039'),
                        legend.key = element_rect(fill = '#D20039', color = '#D20039'),
                        legend.text = element_text(color = 'white'),
                        legend.title = element_blank()) +
  scale_color_manual(values = c('black', 'white')) + 
  xlab('Difference between Date Registered and Last Used (log(days))') + 
  ylab('Playcount')
regvplaycount
ggsave(filename = './presentation/regvplaycount.jpeg',regvplaycount)
dev.off()

  