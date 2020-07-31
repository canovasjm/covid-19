# required libraries ------------------------------------------------------
library(tidyverse)

# read data
df <- read_csv(file = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=722f3143b586a83f")

# transform to tidy data
df1 <- df %>% 
  filter(country_region_code == "AR") %>% 
  select(country_region, 
         sub_region_1, 
         date, 
         retail_and_recreation_percent_change_from_baseline, 
         grocery_and_pharmacy_percent_change_from_baseline,
         parks_percent_change_from_baseline, 
         transit_stations_percent_change_from_baseline, 
         workplaces_percent_change_from_baseline, 
         residential_percent_change_from_baseline) %>% 
  pivot_longer(-c(country_region, sub_region_1, date), names_to = "type", values_to = "values") %>% 
  mutate(sub_region_1 = sub("Buenos Aires$", "CABA", sub_region_1)) %>% 
  mutate(sub_region_1 = sub("* Province", "", sub_region_1)) %>%
  mutate(sub_region_1 = replace_na(sub_region_1, "Todas las provincias")) %>% 
  mutate(type = sub("_percent_change_from_baseline$", "", type))

# write data
write_csv(df, path = paste0("data/google_mobility_report_", Sys.Date(), ".csv"))
write_csv(df1, path = "data/google_mobility_report.csv")
