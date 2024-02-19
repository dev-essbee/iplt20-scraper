## Web Scraper iplt20.com
___
[![GitHub issues](https://img.shields.io/github/issues/dev-SB/iplt20-scrapper)](https://github.com/dev-SB/iplt20-scrapper/issues) [![GitHub forks](https://img.shields.io/github/forks/dev-SB/iplt20-scrapper)](https://github.com/dev-SB/iplt20-scrapper/network)  [![GitHub stars](https://img.shields.io/github/stars/dev-SB/iplt20-scrapper)](https://github.com/dev-SB/iplt20-scrapper/stargazers) [![GitHub license](https://img.shields.io/github/license/dev-SB/iplt20-scrapper)](https://github.com/dev-SB/iplt20-scrapper/blob/master/LICENSE)  [![Twitter](https://img.shields.io/twitter/url/https/github.com/dev-SB/iplt20-scrapper?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fdev-SB%2Fiplt20-scrapper)

### Description
Here is a medium article explaining the project: [Web Scraping IPL statistics](https://medium.com/@dev.essbee/web-scrapping-ipl-stats-493e3344d741)

A CLI web scraping application to extract stats from https://www.iplt20.com - the official website of Indian 
Premier League.
The application allows user to extract following data sets from the website:
* Most Runs
* Most Runs (Over)
* Most Fours
* Most Fours (Innings)
* Most Sixes
* Most Sixes (Innings)
* Most Fifties
* Most Centuries
* Fastest Fifties
* Fastest Centuries
* Highest Scores
* Highest Scores (Innings)
* Best Batting Strike Rate
* Best Batting Average
* Biggest Sixes
* Most Wickets
* Most Maidens
* Most Dot Balls
* Most Dot Balls (Innings)
* Best Bowling Average
* Best Bowling Economy
* Best Bowling Economy (Innings)
* Best Bowling Strike Rate
* Best Bowling Strike Rate (Innings)
* Best Bowling Innings
* Most Runs Conceded (Innings)
* Fastest Balls
* Most Hat Tricks
* Most Four Wickets
* Player Points
* Team Ranking

The data is available for the years 2008-2019 along with some all season stats.
___
### Install Dependencies
```
pip install pandas
pip install numpy
pip install beautifulsoup4
pip install requests
pip install PyInquirer
```

### Run
Clone the repository, change directory to the downloaded repository and type following in terminal:
```
python scraper.py
```
By default the application generates csv files which are saved in the same directory as of the script.
