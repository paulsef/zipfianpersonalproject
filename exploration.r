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
ggplot(sub1) + aes(x = sub1$registered, y = sub1$age, color = factor(sub1$gender), 
                   size = sub1$top_count1) + geom_point()

sub2 <- dcom[dcom$subscriber == 1,]
ggplot(sub2) + aes(x = sub2$registered, y = sub2$age, color = factor(sub2$gender), 
                   size = sub2$top_count1) + geom_point()
sum(is.na(sub2$gender))

dcom$reg_recent_diff = as.numeric(dcom$recent_date1 -dcom$registered, units = "days")
# what are people with NO recent tracks? nothing scrobbled ever?
recent <- dcom[(dcom$reg_recent_diff < 1000)&(dcom$reg_recent_diff > 1)&(!is.na(dcom$reg_recent_diff)),]
ggplot(recent, aes(x = reg_recent_diff)) + geom_histogram() + scale_y_sqrt()