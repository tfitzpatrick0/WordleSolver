import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from guess import *


# EXAMPLE GUESSES:
# DRUNK (R correct, N present, DUK incorrect)
# FIGHT (G present, FIHT incorrect)
# curl -s [words] | grep -v [dukfiht] | grep .r... | grep n | grep -v ...n. | grep g | grep -v ..g..
# running this command in terminal gives remainining list of possible answers

# Make a guess
# Retrieve info from the guess
# Filter the list of remaining words
# Choose a word from the list for next guess

ANSWERS = []


def read_answers():
    with open("answers.txt", "r") as f:
        for line in f:
            ANSWERS.append(line.strip())


def connect():
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    return driver


def main():
    read_answers()
    driver = connect()
    guess(driver, ANSWERS)


if __name__ == "__main__":
    main()
