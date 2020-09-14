#Walmart Data
#Data Wrangling
#Gabe Murray
#19 Apr 20

##Set-up
library(dplyr)
library(tidyverse)
library(rvest)
library(ggplot2)
library(scrubr)
library(rpart)
library(lubridate)
library(caret)

setwd('/home/gabe/Documents/School 2020/Spring 2nd 8 Weeks/Data Wrangling/data/walmart')
dat <- read.csv('train.csv')
dat <- as_tibble(dat)

##Data Cleaning
summary(dat)
class(dat$Date)
dat$Date <- as.Date(dat$Date)
#Checking Null - none found
any_null <- vector("double", ncol(dat))
for (i in seq_along(dat)){
  any_null <- is.na(dat)  
}
any(isTRUE(any_null))
summary(any_null)

#Checking duplicates
summary(duplicated(dat$Store))#45 unique stores.. In a deeper check, would see if they are different than other stores,
#possibly remove them if they appear to differ systematically from the other stores.
#Will go ahead and remove unique stores
summary(duplicated(dat$Date))#what are the 143 unique dates?
summary(duplicated(dat$Weekly_Sales)) 
summary(duplicated(dat$IsHoliday)) #what's the two non-duplicates? store-specific holidays? Weird. Probably should remove

nrow(dat)
#Fully duplicated rows -- none found
dup_rows <- tibble(duplicated = duplicated(dat), row = 1:nrow(dat)) %>%
  filter(duplicated == T)
count(dup_rows)


##Removing strange uniques
dat_clean <- dat
#Store
dat_clean <- dat_clean %>% filter(duplicated(dat_clean$Store) == T)
#Date
dat_clean <- dat_clean %>% filter(duplicated(dat_clean$Date) == T)
#Holiday
dat_clean <- dat_clean %>% filter(duplicated(dat_clean$IsHoliday == T))
print(paste("This cleaning step removed", nrow(dat) - nrow(dat_clean), "rows."))


##Removing Outliers Weekly_Sales
boxplot(dat_clean$Weekly_Sales)
iqr <- IQR(dat_clean$Weekly_Sales)
Q <- quantile(dat_clean$Weekly_Sales, probs=c(.05, .95), na.rm = FALSE)
dat_test <- dat_clean %>% filter(dat_clean$Weekly_Sales < Q[2] & dat_clean$Weekly_Sales > Q[1])
print(paste("The outlier removal process removed", nrow(dat_clean) - nrow(dat_test), "rows, or ~", 
            round((nrow(dat_clean)/(nrow(dat_clean) - nrow(dat_test)))), "% of the data"))
dat_clean <- dat_test #May have been overkill on the removals..
boxplot(dat_clean$Weekly_Sales)

## Adding weekly_sales rank 
dat_clean <- dat_clean %>% mutate(rank = as.integer(rank((Weekly_Sales))))


## Data Exploration
#Weekly_sales
hist(dat_clean$Weekly_Sales, freq = FALSE, xlab = "Weekly Sales", main = "Distribution of Weekly Sales", col = "lightgreen")
curve(dnorm(x, mean=mean(dat$Weekly_Sales), sd=sd(dat$Weekly_Sales)), add = TRUE, lwd = 2, col = "darkblue")

hist(dat_clean$Store, freq = TRUE, xlab = "Store ID", main = "Distribution of Stores", col = "lightgreen")


##Creating Test Data
train <- dat_clean %>% filter(Date < as.Date('2012-02-24')) #~75% data
test <- dat_clean %>% filter(Date >= as.Date('2012-02-24')) #~25% data


## Model Building
lm3 <- lm(Weekly_Sales ~ IsHoliday, data = train)
lm1 <- lm(Weekly_Sales ~ IsHoliday + Store + Dept + Date, data = train)
lm2 <- lm(Weekly_Sales ~ IsHoliday + Store + Dept + Date + rank, data = train)
summary(lm1)
summary(lm2)
summary(lm3) #holidays predict a very modest increase in sales, but seems like a low p-val for n size. Could look for sales leading up to holiday, differentiate holidays
# could see an increase in revenue for dates leading up to the holidays.
print("Terrible models! Very low R^2, cannot interpret Store or Dept effect. Nothing seems predictive except rank, I'm fairly sure reduces the applicability of the second model")

##Predictive model
lm_pred1 <- predict(lm1, test)
actual_preds1 <- data.frame(cbind(actuals = test$Weekly_Sales, predicts = lm_pred1))
coorelation_accuracy1 <- cor(actual_preds1)
coorelation_accuracy1
head(actual_preds1) #Far off

lm_pred2 <- predict(lm2, test)
actual_preds2 <- data.frame(cbind(actuals = test$Weekly_Sales, predicts = lm_pred2))
coorelation_accuracy2 <- cor(actual_preds2)
coorelation_accuracy2 
head(actual_preds2)#Way closer

lm_pred3 <- predict(lm3, test)
actual_preds3 <- data.frame(cbind(actuals = test$Weekly_Sales, predicts = lm_pred3))
coorelation_accuracy3 <- cor(actual_preds3)
coorelation_accuracy3
head(actual_preds3)

#Confusion Matrix
print("As I understand, confusion matrixes are used to test the 
      occurances of true positive, true negative, false positive, and false negatives.
      I think it would work with a logistic regression but not with the 
      models I built. I may be misunderstanding the assignment.")
#confusionMatrix(lm_pred1, actual_preds1)
