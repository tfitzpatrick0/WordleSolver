import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# EXAMPLE GUESSES:
# DRUNK (R correct, N present, DUK incorrect)
# FIGHT (G present, FIHT incorrect)
# curl -s [words] | grep -v [dukfiht] | grep .r... | grep n | grep -v ...n. | grep g | grep -v ..g..
# running this command in terminal gives remainining list of possible answers

# Make a guess
# Retrieve info from the guess
# Filter the list of remaining words
# Choose a word from the list for next guess


def connect():
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    return driver


def main():
    driver = connect()

    game = driver.find_element_by_tag_name("body")
    game.click()
    time.sleep(1)
    game.send_keys("crate")
    game.send_keys(Keys.ENTER)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
