"""
The script contains the following sections:
-  Import of Panda and Matplotlib libraries
1) Import and analysis of the GDP dataset (some lines are commented to avoid their print on every run)
2) Import and analysis of the Energy dataset (some lines are commented to avoid their print on every run)
    with an export of the final filtered dataset
3) Import and analysis of the GDP dataset (some lines are commented to avoid their print on every run)
4) Merge of GDP, ENERGY AND POPULATION datasets to obtain a final merged dataset,
    based on column 'Country' and 'Year' 
5) Computation of Energy Intensity defined as Energy Intensity=Total Energy Consumption/Real GDP + 
    GDP per capita computation + export of the dataset + pivot table based on the exported dataset
6) Trend Energy Intensity + Energy per capita + GDP per capita for each country
7) Computing GDP and energy consumption from the previous year for each country + scatter plot for each country
8) Computing Elasticity + its mean over the observed period for each country + bar chart of the average elasticity

- NOTE: the graph representing the Energy per capita(point 6) has Megawatt-hours per Euro (MWh/€) as 
        unit of measurement. The primary energy consumption in the original Energy dataset uses Terawatt-hours.
        Mathematically, Terawatt-hours per million Euro (TWh/M€) is equal to Megawatt-hours per Euro (MWh/€).

- NOTE 2: to avoid the elasticity to explode, it was set equal to None where the GDP % variation compared
        to the previous year was less than 0.1
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1) GDP DATASET IMPORT AND DATA CHECK
df_gdp = pd.read_csv("Data/GDP_GE_FR_IT_SP.csv",
                     sep = ",",
                     usecols= ["Unit of measure", "National accounts indicator (ESA 2010)", 
                          "geo", "Geopolitical entity (reporting)", "TIME_PERIOD", "OBS_VALUE"])

df_gdp.rename(columns={"Unit of measure": "Unit", 
                   "National accounts indicator (ESA 2010)":"Indicator",
                   "Geopolitical entity (reporting)":"Country",
                   "TIME_PERIOD":"Year",
                   "OBS_VALUE":"GDP_VALUE"}, 
                   inplace=True)

#df_gdp.info()
#print(df_gdp.head(5))

# Missing values
#print("Missing values in the GDP dataset:")
#print(df_gdp.isna().sum()) #0 missing values

df_gdp = df_gdp.sort_values('Year')


#2) PRIMARY ENERGY CONSUMPTION DATASET IMPORT AND DATA CHECK
df_energy = pd.read_csv("Data/owid-energy-data.csv",
                        sep=",",
                        usecols ={"country", "year", "iso_code", "primary_energy_consumption"})

df_energy.rename(columns={"country":"Country","year":"Year"}, inplace=True)

#df_energy.info()
#print(df_energy.head(5))

# Country and year filter
df_energy_filtered = df_energy[df_energy['Country'].isin(["Germany", "France", "Italy", "Spain"])]
df_energy_final = df_energy_filtered[df_energy_filtered['Year'].between(1995, 2023)]

#df_energy_final.info()
#print(df_energy_final.head(5))

# Missing values
#print("Missing values in the final energy dataset:")
#print(df_energy_final.isna().sum()) #0 missing values

df_energy_final = df_energy_final.sort_values('Year')

# Exporting df_energy_final
df_energy_final.to_csv("Output/Energy_GE_FR_IT_SP.csv")


#3) POPULATION DATASET IMPORT AND DATA CHECK
df_pop = pd.read_csv("Data/Pop_GE_FR_IT_SP.csv",
                 sep = ",",
                 usecols=["Unit of measure", "Age class", "Sex", "geo", 
                          "Geopolitical entity (reporting)", "TIME_PERIOD", "OBS_VALUE"])

df_pop.rename(columns={"Unit of measure": "Unit", 
                   "Geopolitical entity (reporting)":"Country",
                   "TIME_PERIOD":"Year",
                   "OBS_VALUE":"POP_VALUE"}, 
                   inplace=True)

#print(df_pop.info())
#print(df_pop.head(5))

# Missing values
#print("Missing values in the population dataset:")
#print(df_pop.isna().sum()) #no missing values


# 4) MERGING GDP, ENERGY AND POPULATION DATASETS
df_gdp_energy = pd.merge(df_gdp, df_energy_final, 
                      on=['Country', 'Year'], 
                      how="inner", 
                      suffixes=('_gdp', '_energy'))

df_final_merged = pd.merge(df_gdp_energy, df_pop, 
                      on=['Country', 'Year'], 
                      how="inner", 
                      suffixes=('_2', '_pop'))

df_final_merged = df_final_merged.drop(['iso_code', 'geo_pop'], axis=1)
df_final_merged = df_final_merged[['geo_2', 
                                   'Country', 
                                   'Year', 
                                   'GDP_VALUE', 
                                   'Indicator', 
                                   'Unit_2', 
                                   'primary_energy_consumption', 
                                   'POP_VALUE', 
                                   'Unit_pop', 
                                   'Age class', 
                                   'Sex']]


# 5) COMPUTING Energy Intensity DEFINED AS Energy Intensity=Total Energy Consumption/Real GDP + (per capita) 
df_final_merged["GDP_capita"] = df_final_merged["GDP_VALUE"]/df_final_merged["POP_VALUE"]
df_final_merged["Energy_Intensity"] = df_final_merged["primary_energy_consumption"]/df_final_merged["GDP_VALUE"]
df_final_merged["Energy_per_capita"] = df_final_merged["primary_energy_consumption"]/df_final_merged["POP_VALUE"]

# Exporting df_GHG_pop
df_final_merged.to_csv("Output/final_data_GE_FR_IT_SP.csv")

# Pivot tables
pt_energy_intensity = df_final_merged.pivot(index='Year', 
                                    columns='Country', 
                                    values='Energy_Intensity')

pt_energy_capita = df_final_merged.pivot(index='Year', 
                                    columns='Country', 
                                    values='Energy_per_capita')

pt_gdp_capita = df_final_merged.pivot(index='Year', 
                                    columns='Country', 
                                    values='GDP_capita')

# 6) Trend Energy Intensity + Energy per capita: graphic
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

ax1 = pt_energy_intensity.plot(ax=axs[0,0], legend=False, title='Energy Intensity', grid=True)
ax2 = pt_energy_capita.plot(ax=axs[0,1], legend=False, title='Energy per capita', grid=True)
ax3 = pt_gdp_capita.plot(ax=axs[1,0], legend=False, title='GDP per capita', grid=True)
ax4 = axs[1,1].axis('off')

ax1.set_ylabel("MWh/€")
ax2.set_ylabel("TWh/person")
ax3.set_ylabel("€/inhabitant")

# Collect all handles and labels
handles, labels = axs[0,0].get_legend_handles_labels()
# Create the single figure legend
# Use fig.legend() to place the legend at the figure level
axs[1,1].legend(handles, labels, loc='center', fontsize='large')

fig.suptitle("Energy and GDP Trends [1995-2023]", fontsize=16, y=0.99)
plt.tight_layout()
plt.savefig("Output/Energy_Intensity_percapita_GE_FR_IT_SP.png")
plt.show()

# 7) Scatter plot: GDP growth rate - Energy consumption growth rate for each country

# Computing GDP and energy consumption from the previous year for each country
df_sorted = df_final_merged.sort_values(by=['Country', 'Year'])

df_sorted["GDP_Variation"] = df_sorted.groupby("Country")["GDP_VALUE"].diff()
df_sorted["GDP_Variation_%"] = df_sorted.groupby("Country")["GDP_VALUE"].pct_change() * 100

df_sorted["Energy_Variation"] = df_sorted.groupby("Country")["primary_energy_consumption"].diff()
df_sorted["Energy_Variation_%"] = df_sorted.groupby("Country")["primary_energy_consumption"].pct_change() * 100

# Scatter plot
fig_2, axs_2 = plt.subplots(2, 2, figsize=(10, 8))

scatt1= df_sorted[df_sorted['Country'] == 'Germany'].plot.scatter(x="GDP_Variation_%", 
                                                                  y="Energy_Variation_%", 
                                                                  ax=axs_2[0,0], 
                                                                  legend=False, 
                                                                  title='Germany', 
                                                                  grid=True,
                                                                  color='k')
scatt2= df_sorted[df_sorted['Country'] == 'France'].plot.scatter(x="GDP_Variation_%", 
                                                                  y="Energy_Variation_%", 
                                                                  ax=axs_2[0,1], 
                                                                  legend=False, 
                                                                  title='France', 
                                                                  grid=True,
                                                                  color='b')
scatt3= df_sorted[df_sorted['Country'] == 'Italy'].plot.scatter(x="GDP_Variation_%", 
                                                                  y="Energy_Variation_%", 
                                                                  ax=axs_2[1,0], 
                                                                  legend=False, 
                                                                  title='Italy', 
                                                                  grid=True,
                                                                  color='g')
scatt4= df_sorted[df_sorted['Country'] == 'Spain'].plot.scatter(x="GDP_Variation_%", 
                                                                  y="Energy_Variation_%", 
                                                                  ax=axs_2[1,1], 
                                                                  legend=False, 
                                                                  title='Spain', 
                                                                  grid=True,
                                                                  color='y')

scatt1.set_xlabel("GDP Variation[%]")
scatt1.set_ylabel("Energy Variation[%]")
scatt1.axline(xy1=(0, 0), slope=1, color='red', linestyle='--', linewidth=2)

scatt2.set_xlabel("GDP Variation[%]")
scatt2.set_ylabel("Energy Variation[%]")
scatt2.axline(xy1=(0, 0), slope=1, color='red', linestyle='--', linewidth=2)

scatt3.set_xlabel("GDP Variation[%]")
scatt3.set_ylabel("Energy Variation[%]")
scatt3.axline(xy1=(0, 0), slope=1, color='red', linestyle='--', linewidth=2)

scatt4.set_xlabel("GDP Variation[%]")
scatt4.set_ylabel("Energy Variation[%]")
scatt4.axline(xy1=(0, 0), slope=1, color='red', linestyle='--', linewidth=2)

fig_2.suptitle("GDP and Energy Variation [1995-2023]", fontsize=16, y=0.98)
plt.tight_layout()
plt.savefig("Output/Decoupling_scatter_GE_FR_IT_SP.png")
plt.show()

# 8) Computing Elasticity=%ΔEnergy/%ΔGDP + bar chart for each country
df_sorted["Elasticity"] = df_sorted["Energy_Variation_%"]/df_sorted["GDP_Variation_%"]
print(df_sorted[["GDP_Variation_%", "Energy_Variation_%", "Elasticity"]].loc[df_sorted['Country'] == 'Italy'])

#To set Elasticity equal to None where GDP_Variation_% = 0.1, so it does not "explode"
df_sorted.loc[abs(df_sorted["GDP_Variation_%"]) < 0.1, "Elasticity"] = None

elasticity_mean = df_sorted.groupby("Country")["Elasticity"].mean()
print(elasticity_mean)
# If
# Elasticity > 1 = energy growths more than GDP (no decoupling)
# 0 < Elasticity < 1 = energy growths less then PIL (relative decoupling)
# Elasticity = 0 = GDP growth but the energy does not change
# Elasticity < 0 → GDP growth while energy decreases (absolute decoupling)

# All the selected countries had relative decoupling over the observed period

ax_bar = elasticity_mean.plot(kind='bar', 
                         ylabel='Elasticity coefficient',
                         title = 'Average Elasticity [1995-2023]')

plt.tight_layout()
plt.savefig("Output/Avg_Elasticity_Char_GE_FR_IT_SP.png")
plt.show()