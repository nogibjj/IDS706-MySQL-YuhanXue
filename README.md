# IDS706-MySQL-YuhanXue

![format workflow](https://github.com/nogibjj/IDS706-MySQL-YuhanXue/actions/workflows/cicd.yml/badge.svg)

This project 6 contains Python scripts/functions that performs a complex query on MySQL. 

## Formatting and Erorrs
Please run `make all` to ensure all codes are well-formatted and free of errors.

## Running Scripts
To run the `main.py`, issue the following command:
```
python3 main.py
```

This script performs the following:
1. Create a database named "beers".
2. Create tables with schemas.
2. Load data from "drinker.csv", "frequents.csv", "serves.csv" to corresponding tables.
3. Perform a complex query and print result.

## Database and Complex Query
The database is a partial database instance from the famous beers instance:
  - drinker: name, address. This table contains name of each drinker and their addresses.
  - frequents: drinker, bar, times_a_week. This table indicates the bar each drinker visits, and how many times the drinker visits the bar each week.
  - serves: bar, beer, price. This table indicates which bar serves which beer at what price.

The complex query is to find drinkers who frequent bars that serve Amstel more than 2 times a week. It returns two columns: drinker, times.
```sql
SELECT d.name, SUM(f.times_a_week) AS times
FROM drinker d INNER JOIN frequents f ON d.name = f.drinker INNER JOIN serves s on f.bar = s.bar
WHERE s.beer = 'Amstel'
GROUP BY d.name
HAVING SUM(f.times_a_week) > 2
ORDER BY times;
```

On the database instance included under `/data`, the above query returns the following results:<br>
Ben, 4 <br>
Dan, 8

