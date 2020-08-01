# COVID-19 reporte de movilidad de Google para Argentina  
Este repositorio contiene código para explorar el data set _"COVID-19 Google mobility report"_ para Argentina.   
Fuente de los datos [aquí](https://www.google.com/covid19/mobility/index.html?hl=en).  

* `app.R`: es el archivo para generar una shiny app y explorar los datos de forma interactiva. Puede ver la shiny app [aquí](https://canovasjm.shinyapps.io/covid-19-argentina/)  
* `read_data.R`: es un script para bajar, procesar y guardar los datos en la carpeta `/data`  


# COVID-19 Google mobility report for Argentina  
This repository contains code with work done on _"COVID-19 Google mobility report"_ data set for Argentina.   
Orginal data source [here](https://www.google.com/covid19/mobility/index.html?hl=en).  

* `app.R`: is the shiny app file to explore the data interactively. You can see the shiny app [here](https://canovasjm.shinyapps.io/covid-19-argentina/)    
* `read_data.R`: is a script to download, process and save the data to the folder `/data`

# UPDATE 2020-08-01  
The original _"COVID-19 Google mobility report"_ provided one value per day of _percent change from baseline_ for each of the series. On Tuesday 2020-07-28 I detected that Google was provinding several values instead. 

I had a backup file with the old methodology including data up to 2020-07-21. For the days after 2020-07-21, I modified the script that process the data in order to compute the median _percent change from baseline_ for each day. 

Also, now the shiny app reads the processed data from GitHub.
