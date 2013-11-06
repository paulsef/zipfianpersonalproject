setwd("~/Zipfian/personal_project")
library(ggplot2)

df1 <- read.table('./ssvout/0.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
df2 <- read.table('./ssvout/15000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
           comment.char = "", quote = "")
df3 <- read.table('./ssvout/20000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
#df4 <- read.table('./ssvout/25000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
#                  comment.char = "", quote = "")
df5 <- read.table('./ssvout/10000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
dcom <- rbind(df1,df2,df3,df5)
rm(df1,df2,df3,df5)
print(sum(dcom$subscriber == 1))

dcom$registered <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$registered
dcom$recent_date1 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date1
dcom$recent_date2 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date2
dcom$recent_date3 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date3
dcom$recent_date4 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date4
dcom$recent_date5 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date5

sub1 <- dcom[dcom$playcount > 1,]
ggplot(sub1) + aes(x = sub1$registered, y = sub1$playcount, color = factor(sub1$subscriber)) + 
  geom_point() + scale_y_log10()#+ scale_colour_hue(l=100, c=100)
ggplot(sub1) + aes(x = sub1$registered, y = sub1$playcount, color = factor(sub1$subscriber), 
                   size = sub1$age) + geom_point() + scale_y_log10()

subscriber <- dcom[dcom$subscriber == 1,]
user <- dcom[dcom$subscriber == 0,]
ggplot(subsciber) + aes(x = subsciber$registered, y = subsciber$age, color = factor(subsciber$gender), 
                   size = subsciber$top_count1) + geom_point()



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