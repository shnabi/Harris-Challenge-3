setwd("C:/Users/Shehryar/Documents/GitHub/shnabi/python-master")

library(ipumsr)
library(tidyverse)

## LODING AN IPUMS DATASET ## 

ddi <- read_ipums_ddi("usa_00012.xml")
data <- read_ipums_micro(ddi)

## EXPORTING AS A CSV ## 

write.csv(data, "C:/Users/Shehryar/Documents/GitHub/shnabi/python-master/counties_data.csv")
