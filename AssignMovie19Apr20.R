#Movie Recommendation Engine

library(dplyr)
library(tidyverse)
library(ggplot2)
library(scrubr)
library(reshape2)
library(scales)

setwd('/home/gabe/Documents/School 2020/Spring 2nd 8 Weeks/Data Wrangling/data/movies/ml-100k')

#Loading Tables
dat <- read.table('u.data', col.names = c("user_id", "item_id", "rating", "time"))
dat_genre <- read.table("u.genre", sep = "|", col.names = c("genre_name", "genre_num"))
dat_title <- read.csv("u.item", sep = "|", header = FALSE, col.names = c("item_id", "item_title", "release_date", "vid_release_date", "IMBD_url", 
                      "genre_unknown", "genre_action", "genre_adventure", "genre_animation", "genre_children", "genre_comdedy", "genre_crime", "genre_doc", "genre_drama", "genre_fantasy",
                      "genre_noir", "genre_horror", "genre_musical", "genre_mystery", "genre_romance", "genre_scifi", "genre_thriller", "genre_war", "genre_western"))
dat_user <- read.table("u.user", sep = "|", header = FALSE, col.names = c("user_id", "user_age", "user_gender", "user_occupation", "user_zc"))

#Convert time from seconds since 1970 to ymd
dat$time
  dat$time <- as.Date(as.POSIXct(dat$time, origin = "1970-01-01"))

#Adding title to data
dat_full <- dat
dat_full <- left_join(dat_full, dat_title, by = "item_id")

#Adding demographics to data
dat_full <- left_join(dat_full, dat_user, by =  "user_id")

##Cleaning
#Checking Null - none found
any_null <- vector("double", ncol(dat_full))
for (i in seq_along(dat_full)){
  any_null <- is.na(dat_full)  
}
any(isTRUE(any_null))
summary(any_null)

#deduplicating
#Fully duplicated rows -- none found
dup_rows <- tibble(duplicated = duplicated(dat_full), row = 1:nrow(dat_full)) %>%
  filter(duplicated == T)
count(dup_rows)


#mostly uninteresting, but some weird values I'm going to eliminate
#typically should probably investigate weird false rows, maybe fill, but in the interest of time
summary(duplicated(dat_full$item_id))
summary(duplicated(dat_full$user_id))
summary(duplicated(dat_full$rating))
summary(duplicated(dat_full$time))
summary(duplicated(dat_full$item_title))
summary(duplicated(dat_full$release_date))
summary(duplicated(dat_full$vid_release_date))
summary(duplicated(dat_full$IMBD_url))
summary(duplicated(dat_full$genre_unknown))
summary(duplicated(dat_full$user_gender))
summary(duplicated(dat_full$user_age))
summary(duplicated(dat_full$user_occupation))
summary(duplicated(dat_full$user_zc))


dat_clean <- dat_full
#item_id
dat_clean <- dat_clean %>% filter(duplicated(dat_clean$item_id) == T)
#user_id
dat_clean <- dat_clean %>% filter(duplicated(dat_clean$user_id) == T)
#rating
dat_clean <- dat_clean %>% filter(duplicated(dat_clean$rating == T))
#title
dat_clean <- dat_clean %>% filter(duplicated(dat_clean$item_title == T))

print(paste("This cleaning step removed", nrow(dat_full) - nrow(dat_clean), "rows, or about",
            round((nrow(dat_clean)/nrow(dat_full))), "% of the data"))

##Exploration
hist(dat_clean$rating,
     breaks = 5,
     xlim = c(1,5),
     ylim = c(0, 35000),
     col = "white",
     border = "black",
     las = 1,
     ylab = "Freq",
     xlab = "Ratings",
     main = "Frequency of Ratings")


ggplot(dat_clean, aes(x=rating))+geom_histogram(binwidth = 1)+facet_grid(~user_gender)+theme_bw()+stat_density()

ggplot(dat_clean, aes(rating)) +
  geom_bar(aes(y = (..count..)/ sum(..count..))) + 
  scale_y_continuous(labels = scales::percent) + 
  ylab("relative freq")

ggplot(dat_clean, aes(x= rating,  group=user_gender)) + 
  geom_bar(aes(y = ..prop.., fill = factor(..x..)), stat="count") +
  geom_text(aes( label = scales::percent(..prop..),
                 y= ..prop.. ), stat= "count", vjust = -.5) +
  labs(y = "Percent", fill="") +
  facet_grid(~user_gender) +
  scale_y_continuous(labels = scales::percent)


