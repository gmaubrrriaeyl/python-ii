#Gabe Murray
#Data Wrangling
#24 May 20
#Data Analysis
library(dplyr)
library(tidyverse)
library(tm)
library(stringr)
text <- readLines('/home/gabe/Documents/School 2020/Spring 2nd 8 Weeks/Data Wrangling/data/data analysis/DataAnalysis.txt')
text <- tail(text,-6)

#Exploration
colnames(test)
nchar(text[1])
nchar(text[2])
nchar(text[3])
head(text)

#Cleaning
test <- text
test <- tail(test,-6)
nchar(test[1])
test[3]
test <- str_sub(text, start = 5)
test[3]
test <- tolower(test)
test <- t(test)
test <- t(test)


# Categories
help_others = c('difference', 'child', 'kid', 'help', 'service', 'imporve', 'positive', 'trouble', 'learn')
interpersonal = c('teacher', 'educat', 'coach', 'mom', 'dad')
self = c('hour', 'off', 'enjoy', 'aptitude', 'like', 'love', 'weekend', 'dissatisf', 'summer')
prof = c('english', 'math', 'business', 'music', 'ability', 'chemistry', 'biology', 'subject')

#Model building
test$help=0

for (i in 1:nrow(test)) {
  if (help_others %in% test) {
    test$help[i] <- 1
  } else {
      test$help[i] <- 0 
      }
}

