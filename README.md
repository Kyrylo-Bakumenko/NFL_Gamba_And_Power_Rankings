# NFL_Gamba_And_Power_Rankings
Elo Based Rankings System for the NFL. Risk Aware Wager Algorithm.

## The Model
This project creates Elo power rankings system for every team in the NFL using data dating back to 1970. The algorithm scans odds from Vegas (Currently read of spreadsheet format) and compares them to the elo ranking’s predictions. The use of 'odds' is neccessary for a more complete picture of the accuracy of the model. For example, predicting a NFL team to beat a high school team is hardly a feat, predictions are most valuable when the outcome is unclear. This model factors in the NFL Draft by regressing teams towords the mean after every season proportionaly to their standings in order to mimick the advantage of early draft picks. The final weights for the model where found by regressive search through the Elo Model's learning parameters (*MAX_GAIN*, *SEASON_ADJ*, *DELTA*) as well as optimizing the betting model's variables (*mu* and *max_edge*). This search was accelerated by the use of Numba.

## Results
This model demonstrates predictive capabilities in a backtest from the 2020 season, however the availbility and changing nature of sports betting odds limits curretn back testing capabilities. This model also allows us to quantify team performance over their existence and visualize it, either as they compare to the rest of the league or relative to themself in the past.

### Elo Insights
20 Years Model's Teams Visualized

![image](https://user-images.githubusercontent.com/44657125/142329535-9ae4052f-7f14-41ab-baa5-97ba434308b9.png)

New York Jets Isolated

![image](https://user-images.githubusercontent.com/44657125/142330777-be886f8d-8191-4a70-880a-0da634958c79.png)

### Betting Performance
Stats, season starts with $1

![Screenshot (948)](https://user-images.githubusercontent.com/44657125/142328056-451050bc-09be-44a1-8398-f738121ba6c8.png)

Profit by Time

![image](https://user-images.githubusercontent.com/44657125/142322862-232fb0ee-ef93-4b25-9d9c-8aaaa3109f08.png)

Distribution of Wins and Loses

![image](https://user-images.githubusercontent.com/44657125/142323039-65a3c0cb-8b31-436f-9d36-be6963fc2773.png)


### Optimization Search Snapshots
3D plot

![image](https://user-images.githubusercontent.com/44657125/142321595-c628f045-1a2e-4baf-9d9a-43ce1266ba07.png)

2D Slice

![image](https://user-images.githubusercontent.com/44657125/142322143-e647bd84-0199-4d65-a852-6a9c001286d8.png)


## Areas for Further Development
This project uses webscraping for data gathering for the Elo Model, however there has not yet been an implmentation for on deman historical betting data. Another constant impediement for accurate results is injury in the NFL as the model remains oblivoious to these crucial changes within teams.
Furthermore there are two main shortcomings of an Elo approach:

### 1. Elo is Score Indiscriminant
This means that the Elo model cannot differentiate between a blowout win and a narrow victory: each are weighed equally.

### 2. Teams Consist of Many Players
The elo ranking applies to the team as a whole. This makes it impossible to account for player transfers and trades as well as injuries as the indivdual impact of the player is not known.

## Looking Ahead
In the future I will add web-scraping for adding betting data. This will allow me to perform backtesting across a wider range of years.
Additionaly I plan to innovate on a more inclusive multivariable model using Trust Regions or attaching an indivdualised score to each active player on an NFL team. This will allow me more accurately asses the impact of injuries, trades, and other line-up changes.
