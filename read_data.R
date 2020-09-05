# required libraries ------------------------------------------------------
library(tidyverse)

# read data ---------------------------------------------------------------
# read and filter data from may
df_may <- read_csv("data/google_mobility_report_2020-07-25.csv") %>% 
  filter(country_region_code == 'AR') %>% 
  arrange(sub_region_1, date)

# filter data to update
df_new_raw <- read_csv(file = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=722f3143b586a83f")
df_new <- df_new_raw %>% 
  filter(country_region_code == 'AR' & date > '2020-07-21' ) %>% 
  arrange(sub_region_1, date)

# filter data to save in GitHub as backup
df_to_bkp <- df_new_raw %>% 
  filter(country_region_code == 'AR')

# process data ------------------------------------------------------------
# group by and aggregate df_new to create df_new
df_new <- df_new %>%
  group_by(country_region_code, country_region, sub_region_1, date) %>%
  summarise(across(ends_with("baseline"), ~median(.x, na.rm = TRUE)))

# row bind data sets
df_updated <- bind_rows(df_may, df_new, .id = 'id')

# transform to tidy data
df <- df_updated %>% 
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
  mutate(
    sub_region_1 = sub("Buenos Aires$", "CABA", sub_region_1), 
    sub_region_1 = sub("* Province", "", sub_region_1),
    sub_region_1 = replace_na(sub_region_1, "Todas las provincias"),
    type = sub("_percent_change_from_baseline$", "", type)
    )

# write data --------------------------------------------------------------
write_csv(df_to_bkp, path = paste0("data/google_mobility_report_", Sys.Date(), ".csv"))
write_csv(df, path = "data/google_mobility_report.csv")
