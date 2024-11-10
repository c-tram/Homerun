The purpose of this document is to provide documentation regarding the intention and usage of this software*

Homerun is a software designed to be a static prediction model focused around current trends in the MLB and provide data analytics associated.

These Trends include:
1. Playoff Chance
2. World Series Chance
3. Determine Player Growth / Regression


EXAMPLE FUNCTIONS   ->

source/gather_data  -> USE SELENIUM in order to access web pages and pull statistics from each team.

FILE gather(*selenium functions)    // take data from websites to generate a CSV for given year

FILE combine(*selenium functions)   // combine years from generated CSV. return a new CSV


source/read_data    -> USE PYTHON in order to analyze this data and generate trends as mentioned above.

Team statistics(double avg, int rbi, int hr, double risp, double era, int k, double whip, int wins, int losses, int rs, int ra, int dif, double war) //accumulation of stats for an entire team for the year. is an average of all player stats


