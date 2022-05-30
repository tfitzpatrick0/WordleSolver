import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# open the website https://www.nytimes.com/games/wordle/index.html
# find the text input box
# enter the word "hello"
# click the submit button


def connect():
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://www.nytimes.com/games/wordle/index.html")

    game = driver.find_element_by_tag_name("body")
    game.click()
    time.sleep(1)
    game.send_keys("crate")
    game.send_keys(Keys.ENTER)
    time.sleep(5)


def main():
    connect()


if __name__ == "__main__":
    main()
