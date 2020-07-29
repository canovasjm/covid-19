#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:15:21 2020

@author: jm
"""

#%% required libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#%% read data
#df_original = pd.read_csv('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=5805f0ab2859cf87', encoding = 'utf-8')
df_original = pd.read_csv('data/google_mobility_report_2020-07-25.csv', encoding = ('utf-8'))
df = df_original.copy()

# check columns
df.columns

# see head of data frame
df.head()

#%% filter data for Argentina only
df = df[df['country_region'] == 'Argentina']

# check resulting data
df.info()

# check NA
df.isna().any()
df.isna().sum().plot(kind = 'bar')

# drop columns with many NA
df = df.drop(columns = ['country_region_code', 'sub_region_2', 'iso_3166_2_code', 'census_fips_code'])

# rename columns
df.rename(columns = {'country_region': 'pais',
                     'sub_region_1': 'provincia',
                     'date': 'fecha',
                     'retail_and_recreation_percent_change_from_baseline': 'retail_and_recreation', 
                     'grocery_and_pharmacy_percent_change_from_baseline': 'grocery_and_pharmacy',
                     'parks_percent_change_from_baseline': 'parks',
                     'transit_stations_percent_change_from_baseline': 'transit_stations',
                     'workplaces_percent_change_from_baseline': 'workplaces',
                     'residential_percent_change_from_baseline': 'residential'}, 
          inplace = True)


# drop row where 'provincia' is NA
df = df.dropna(subset = ['provincia'])

# check NA
df.isna().sum().plot(kind = 'bar')



#%% set index to plot the data
df['fecha'] = pd.to_datetime(df['fecha'])
df.set_index('fecha', inplace = True)

# check index
print(df.index)


#%% subsets
bsas = df[df['provincia'] == 'Buenos Aires Province']
caba = df[df['provincia'] == 'Buenos Aires']


#%% plot for CABA
plt.rcParams["figure.dpi"] = 1200
plt.figure(figsize = (10, 10))
fig, ax = plt.subplots()

# plot data
ax.plot(caba.index, caba['workplaces'], color = 'darkred', label = 'Workplaces')
ax.plot(caba.index, caba['retail_and_recreation'], color = 'darkblue', label = 'Retail and recreation')

# color the area of lockdown phase 1
p1 = caba['2020-07-01':'2020-07-17'].index
ax.fill_between(p1, -90, -30, facecolor = 'lightsteelblue', alpha = 0.3, label = 'Fase 1') 

# annotate carnaval
ax.annotate('Carnaval', xy = [pd.Timestamp('2020-02-24'), -71], 
            xytext = [pd.Timestamp('2020-03-25'), 10], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# annotate dia del trabajador
ax.annotate('Día del \ntrabajador', xy = [pd.Timestamp('2020-05-01'), -87], 
            xytext = [pd.Timestamp('2020-03-28'), -50], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# annotate dia de la Revolucion de Mayo
ax.annotate('Día de la \nRevolución de Mayo', xy = [pd.Timestamp('2020-05-25'), -84], 
            xytext = [pd.Timestamp('2020-04-01'), -30], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'}, 
            fontsize = 8)

# annotate paso a la inmortalidad Gral. Güemes
ax.annotate('Paso a la inmortalidad \nGral. Güemes', xy = [pd.Timestamp('2020-06-15'), -80], 
            xytext = [pd.Timestamp('2020-04-15'), -15], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# annotate paso a la inmortalidad Gral. Belgrano
ax.annotate('Paso a la \ninmortalidad \nGral. Belgrano', xy = [pd.Timestamp('2020-06-20'), -55], 
            xytext = [pd.Timestamp('2020-05-23'), -28], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# annotate dia de la independencia
ax.annotate('Día de la \nindependencia', xy = [pd.Timestamp('2020-07-09'), -80], 
            xytext = [pd.Timestamp('2020-06-15'), -10], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# set axis names
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 7))
plt.xticks(fontsize = 5, rotation = 90)
ax.set_xlabel('Fecha', size = 8)
ax.set_ylabel('% de cambio respecto a la línea base', size = 8)
ax.set_title('Ciudad Autónoma de Buenos Aires')

# set caption
caption = "@canovasjm \nFuente: Google LLC 'Google COVID-19 Community Mobility Reports' \nhttps://www.google.com/covid19/mobility/ \nConsultado: 2020-07-25"
plt.figtext(0.9, -0.05, caption, wrap = False, horizontalalignment = 'right', fontsize = 6)

# set legend
plt.legend(prop = {'size': 6})

# show plot
plt.show()

# save plot
fig.set_size_inches([10, 7])
fig.savefig('python-plot/caba-fase-uno.png', dpi = fig.dpi, bbox_inches = 'tight')


#%% plot for Buenos Aires
plt.rcParams["figure.dpi"] = 1200
plt.figure(figsize = (10, 10))
fig, ax = plt.subplots()

# plot data
ax.plot(bsas.index, bsas['workplaces'], color = 'darkred', label = 'Workplaces')
ax.plot(bsas.index, bsas['retail_and_recreation'], color = 'darkblue', label = 'Retail and recreation')

# color the area of lockdown phase 1
p1 = bsas['2020-07-01':'2020-07-17'].index
ax.fill_between(p1, -85, -22, facecolor = 'lightsteelblue', alpha = 0.3, label = 'Fase 1') 

# annotate carnaval
ax.annotate('Carnaval', xy = [pd.Timestamp('2020-02-24'), -54], 
            xytext = [pd.Timestamp('2020-03-25'), 10], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# annotate dia del trabajador
ax.annotate('Día del \ntrabajador', xy = [pd.Timestamp('2020-05-01'), -76], 
            xytext = [pd.Timestamp('2020-03-28'), -47], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# annotate dia de la Revolucion de Mayo
ax.annotate('Día de la \nRevolución de Mayo', xy = [pd.Timestamp('2020-05-25'), -70], 
            xytext = [pd.Timestamp('2020-04-01'), -33], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'}, 
            fontsize = 8)

# annotate paso a la inmortalidad Gral. Güemes
ax.annotate('Paso a la inmortalidad \nGral. Güemes', xy = [pd.Timestamp('2020-06-15'), -64], 
            xytext = [pd.Timestamp('2020-04-01'), -17], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# annotate paso a la inmortalidad Gral. Belgrano
ax.annotate('Paso a la \ninmortalidad \nGral. Belgrano', xy = [pd.Timestamp('2020-06-20'), -32], 
            xytext = [pd.Timestamp('2020-05-20'), -20], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# annotate dia de la independencia
ax.annotate('Día de la \nindependencia', xy = [pd.Timestamp('2020-07-09'), -63], 
            xytext = [pd.Timestamp('2020-06-17'), -12], 
            arrowprops = {'arrowstyle' : '->', 'color' : 'gray'},
            fontsize = 8)

# set axis names
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 7))
plt.xticks(fontsize = 5, rotation = 90)
ax.set_xlabel('Fecha', size = 8)
ax.set_ylabel('% de cambio respecto a la línea base', size = 8)
ax.set_title('Provincia de Buenos Aires')

# set caption
caption = "@canovasjm \nFuente: Google LLC 'Google COVID-19 Community Mobility Reports' \nhttps://www.google.com/covid19/mobility/ \nConsultado: 2020-07-25"
plt.figtext(0.9, -0.05, caption, wrap = False, horizontalalignment = 'right', fontsize = 6)

# set legend
plt.legend(prop = {'size': 6})

# show plot
plt.show()

# save plot
fig.set_size_inches([10, 7])
fig.savefig('python-plot/bsas-fase-uno.png', dpi = fig.dpi, bbox_inches = 'tight')
