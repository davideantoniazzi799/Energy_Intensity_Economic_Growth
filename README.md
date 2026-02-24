## Energy Intensity and Economic Growth in Major EU Economies (1995–2023)

The project aims to analyze if EU's four most populated countries (Germany, France, Italy, and Spain) 
are decoupling their economic growth from their energy consumption over the period [1995-2023].

# Research Question
*Are major EU economies decoupling economic growth from energy consumption?*

# Data Source
The project applies yearly datasets concerning GDP, Population, and Energy for each country over the observed period.
Both the GDP and the population datasets are available from Eurostat:
- The annual total population data is provided at [Population on 1 January by age and sex](https://doi.org/10.2908/DEMO_PJAN).
  No distiction of age and sex was applied.
- The annual GDP dataset is provided at [Gross domestic product (GDP) and main components (output, expenditure and income)](https://doi.org/10.2908/NAMA_10_GDP).
  - Unit of measurement: *Chain linked volumes (2010), million euro*

To elaborate Energy numbers, the total annual **Primary Energy Consumption** was assumed.
Primary energy consumption figures are taken from Our World in Data’s energy dataset, compiled from the Energy Institute and International Energy Administration.
The dataset is available at [energy-data](https://github.com/owid/energy-data?tab=readme-ov-file). To obtain the data, the available complete Energy dataset was downloaded in a CSV format.
- Unit of measurement: *terawatt-hours (TWh)* (see [full codebook](https://github.com/owid/energy-data/blob/master/owid-energy-codebook.csv))

# Methodology
The project applied Python, particularly Pandas for data manipulation and Matplotlib for visualization.
Three visualizations were produced:
- Trends of *Energy Intensity*, *Energy per capita* and *GDP per capita* for each country over the observed period
- A scatter plot depicting the relation *GDP-Energy Consumption variation rate* for each country over the observed period
- A bar chart comparing the *average elasticity* between Energy Consumption and GDP variation for each country over the observed period

All datasets were first manipulated to check the data. After, a merge of them was conducted to obtain the final dataset. 
The next step was to compute the **Energy Intensity**, defined as Energy Intensity = Total Energy Consumption/Real GDP.

Additionally, **elasticity** was computed as Elasticity = %ΔEnergy / %ΔGDP.

All the visualizations were performed eventually.

**NOTE**: to avoid the elasticity "explosion", this was set equal to None 
when a percentage variation of the GDP smaller than 0.1 compared to the previous year was registered.

# Key Findings
From the first chart it is possible to notice that:
- All the selected countries show a strong decrease of the Energy Intensity, suggesting that these economy are becoming more efficient:
  either the same amount of wealth is obtained using less energy, or more wealth is obtained with the same amount of energy.
  This suggests evidence of long-term relative decoupling between economic growth and energy consumption.
  Germany and France exhibit the strongest decline in energy intensity, suggesting a substantial structural transformation and/or efficiency improvements over the period.
  On the contrary, Spain shows a slower reduction trend which started later than the other countries, around 2005.
  
- Regarding the Energy per capita, which expresses how much energy a person consumes on average, Germany, France and Italy show a decrease but with different rates.
  France seems the country with the strongest reduction rate over the observed period, whereas Germany and Italy have a stable but more moderate decrease.
  Spain is the only country that shows a small increase of this variable over the observed period.
  It is interesting to notice the COVID-19 pandemic effect for each country, with a huge drop from 2019 to 2020 followed by an upward after 2020, except for Germany.

- The GDP per capita increased for each country over the selected period but with different rates. Germany and Spain showed the greatest rates,
  whereas Italy had a minor growth. It is possible to notice the pandemic effect here as well.

From the second chart it is possible to notice that:
- The points that stand under the red 45° line mean a decoupling year. There are two types of decoupling:
    - *relative* decoupling: both energy used and GDP growth, but GDP does at a biggest rate;
    - *absolute* decoupling: only GDP grows while the amount of energy used does not change.
  The scatter plots seem to suggest a mixture of relative and absolute decoupling years.

- **Germany** shows a good amount of *absolute* decoupling years, which reflects what the first visualization showed. There are also years with *relative* decoupling.
  Anyway, some years do not show a decoupling effect.

- Similar to Germany, **France** shows multiple *absolute* decoupling years. This country has less years with no decoupling effect than Germany.

- **Italy** shows a relative good number of *relative* decoupling years, although it is possible to notice that the GDP per capita had low numbers.

- **Spain** shows several years of *relative* decoupling, together with many years without such effect.

The average elasticity over the observed period is:
- Germany: 0.869
- France: 0.067
- Italy: 0.133
- Spain: 0.624

It is important to know that:
- Elasticity > 1 -> energy consumption grows faster than GDP
- 0 < Elasticity < 1 -> relative decoupling
- Elasticity < 0 -> absolute decoupling

# Economic Interpretation
The computed elasticity values show that each country had a *relative* decoupling effect during the selected period. 

Elasticity captures short-term responsiveness between economic activity and energy demand, but it does not necessarily reflect long-term structural decoupling.

Germany strongly reduced its energy intensity in the long period, but the short-term responsiveness between GDP and energy demand remains relatively strong.

On the other hand, France shows the lowest elasticity value, which might confirm the strong efficiency that can be noticed in the first and second char. 
France's low elasticity may also reflect its electricity mix, which relies heavily on nuclear energy.

Initially, Italy recorded the highest averaged elasticity due to the "explosion" effect that it recorded in 2013(around 1800). This was due to the almost null variation
in the GDP per capita from the previous year. This explains two points:
- The extremely high elasticity observed in 2013 for Italy is driven by near-zero GDP growth combined with a significant decline in energy consumption,
  generating a mathematically inflated ratio. This means that in this case the elasticity becomes unstable and uninterpretable.
  This is why elasticy was considered null where the GDP growth was less that 0.1;
- Extremely high elasticity values observed in certain years are driven by near-zero GDP growth rates rather than structural changes in the energy-economy relationship.

Italy showed the second lowest averaged elasticity among the selected countries. 
As just said, this value might be affected by the several years of stagnant economy that Italy experienced.

# Limitations
- The analysis does not control for structural economic changes (e.g. deindustrialization, outsourcing of energy-intensive production)
- Primary energy consumption may overstate efficiency changes due to energy mix effects
- The analysis does not decompose energy use by sector (industry, transport, residential)
- The project does not test causality between GDP growth and energy consumption
- Elasticity is sensitive to small GDP variations and short-term shocks (e.g. crises, pandemic) 

# Repository Contents
- Data folder containing:
  - annual population of the selected countries over the observed period
  - annual GDP of the selected countries over the observed period
  - energy dataset containing the primary energy consumption records

- Output folder containing:
    - the cleaned *Energy* dataset with data for the selected countries over the observed period
    - a dataset resulted from the merge of the two input and the manipulated Energy datasets
    - three visualizations: Energy Consumption and GDP Trends; GDP and Energy Consumption variations; Average Elasticity bar chart.

- Python analysis script

# Bibliography
- Hannah Ritchie, Pablo Rosado, and Max Roser (2023) - “Energy” Published online at OurWorldinData.org. Retrieved from: 'https://ourworldindata.org/energy' [Online Resource]
- Eurostat (https://ec.europa.eu/eurostat/databrowser/explore/all/all_themes?lang=en&display=list&sort=category)
