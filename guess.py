import time
import random
import re
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# EXAMPLE GUESSES:
# DRUNK (R correct, N present, DUK incorrect)
# FIGHT (G present, FIHT incorrect)
# curl -s [words] | grep -v [dukfiht] | grep .r... | grep n | grep -v ...n. | grep g | grep -v ..g..
# running this command in terminal gives remainining list of possible answers

def guess(driver, answers):
  # Make a guess
  # Retrieve info from the guess
  # Filter the list of remaining words
  # Choose a word from the list for next guess
  info = {"absent": "", "correct": {}, "present": {}, "duplicates": {}}
  for i in range(6):
    # pick random element from answers
    guess = random.choice(answers)
    # if i == 0:
    #   guess = "shoos"
    try_guess(driver, guess)
    info = update_info(driver, info, guess)
    regex_list = set_regex(info)
    print(regex_list)
    answers = update_answers(answers, regex_list)


def try_guess(driver, guess):
  game = driver.find_element_by_tag_name("body")
  game.click()
  time.sleep(1)
  game.send_keys(guess)
  game.send_keys(Keys.ENTER)
  time.sleep(5)


def update_info(driver, info, guess):
  wrapper = driver.find_element_by_tag_name("game-app")
  game = driver.execute_script(
    "return arguments[0].shadowRoot.getElementById('game')", wrapper
  )

  game_row = game.find_element_by_css_selector("game-row[letters='" + guess + "']")
  game_row_HTML = BeautifulSoup(
    driver.execute_script("return arguments[0].shadowRoot.innerHTML", game_row),
    features="html.parser",
  )

  keyboard = game.find_element_by_css_selector("game-keyboard")
  keyboard_HTML = BeautifulSoup(
    driver.execute_script("return arguments[0].shadowRoot.innerHTML", keyboard),
    features="html.parser",
  )

  for position, tile in enumerate(game_row_HTML.findAll("game-tile")):
    letter = tile.attrs["letter"]
    status = tile.attrs["evaluation"]

    if status == "absent":
      key = keyboard_HTML.find("button", {"data-key": letter})
      if key.attrs["data-state"] == "absent" and letter not in info["absent"]:
        info["absent"] += letter

      # handling duplicate letters
      elif key.attrs["data-state"] == "present":
        if letter in info["present"]:
          info["present"][letter].append(position)
        else:
          info["present"][letter] = [position]
      elif key.attrs["data-state"] == "correct":
        if position not in info["correct"]:
          info["duplicates"][letter] = [position]

    if status == "correct":
      info["correct"][position] = letter
      if letter in info["present"]:
        del info["present"][letter]

    if status == "present" and letter not in info["correct"].values():
      if letter in info["present"]:
        info["present"][letter].append(position)
      else:
        info["present"][letter] = [position]

    print(info)

  return info


def set_regex(info):
  regex_list = []
  if len(info["absent"]) > 0:
    regex_list.append(re.compile("^[^" + info["absent"] + "]*$"))

  for position, letter in info["correct"].items():
    regex = ""
    for i in range(5):
      if i == position:
        regex += "[" + letter + "]"
      else:
        regex += "."
    regex_list.append(re.compile(regex))

  for letter, positions in info["present"].items():
    regex_list.append(re.compile("^.*" + letter + ".*$"))

    for position in positions:
      regex = ""
      for i in range(5):
        if i == position:
          regex += "[^" + letter + "]"
        else:
          regex += "."
      regex_list.append(re.compile(regex))
  
  for letter, positions in info["duplicates"].items():
    for position in positions:
      regex = ""
      for i in range(5):
        if i == position:
          regex += "[^" + letter + "]"
        else:
          regex += "."
      regex_list.append(re.compile(regex))

  return regex_list


def update_answers(answers, regex_list):
  # Filter the list of remaining words
  new_answers = []
  for answer in answers:
    if check_answer(answer, regex_list):
      new_answers.append(answer)

  return new_answers


def check_answer(answer, regex_list):
  for regex in regex_list:
    if not regex.match(answer):
      return False
  return True
