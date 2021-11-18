# NFL_Gamba_And_Power_Rankings

## The Model
This project creates Elo power rankings system for every team in the NFL using data dating back to 1970. The algorithm scans odds from Vegas (Currently read of spreadsheet format) and compares them to the elo ranking’s predictions. The use of 'odds' is neccessary for a more complete picture of the accuracy of the model. For example, predicting a NFL team to beat a high school team is hardly a feat, predictions are most valuable when the outcome is unclear. This model factors in the NFL Draft by regressing teams towords the mean after every season proportionaly to their standings in order to mimick the advantage of early draft picks. The final weights for the model where found by regressive search throughthe Elo Model's learning parameters (*MAX_GAIN*, *SEASON_ADJ*, *DELTA*) and the optimization of the betting model's variables (*mu* and *max_edge*).

## Results
This model demonstrates predictive capabilities in a backtest from the 2020 season, however the availbility and changing nature of sports betting odds limits curretn back testing capabilities.

### Betting Stats

![image](https://user-images.githubusercontent.com/44657125/142319784-eaba6508-eca7-4af5-97c9-c1961e0a66d9.png)

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
