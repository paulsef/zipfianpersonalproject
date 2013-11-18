setwd("~/Zipfian/personal_project")
library(ggplot2)

df1 <- read.table('./ssvout/0.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
df2 <- read.table('./ssvout/5000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
df3 <- read.table('./ssvout/10000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
df4 <- read.table('./ssvout/15000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
df5 <- read.table('./ssvout/20000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
df6 <- read.table('./ssvout/25000.ssv', header = TRUE, sep = ',', as.is = TRUE, na.strings = "None",
                  comment.char = "", quote = "")
print(c(sum(df1$subscriber == 1),sum(df2$subscriber == 1),sum(df3$subscriber == 1),sum(df4$subscriber == 1)))
dcom <- rbind(df1,df2,df3, df4, df5, df6)
rm(df1,df2,df3,df4, df5, df6)
print(sum(dcom$subscriber == 1))

dcom$registered <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$registered
dcom$recent_date1 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date1
dcom$recent_date2 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date2
dcom$recent_date3 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date3
dcom$recent_date4 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date4
dcom$recent_date5 <- strptime("1970-01-01", "%Y-%m-%d", tz="UTC") + dcom$recent_date5


