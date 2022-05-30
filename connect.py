import time
from selenium import webdriver

# open the website https://www.nytimes.com/games/wordle/index.html
# find the text input box
# enter the word "hello"
# click the submit button


def connect():
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    input_box = driver.find_element_by_id("word")
    input_box.send_keys("hello")
    submit_button = driver.find_element_by_id("submit")
    submit_button.click()


def main():
    connect()


if __name__ == "__main__":
    main()
