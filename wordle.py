import random
from rich import print
from rich.console import Console
import requests

# Validates an input is a real word
def wordExists(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    return response.status_code == 200

# Receives an input, evaluates correctness, prints result
def makeGuess(solution):
    # reveive guess
    guess = [*(input().upper())]

    # validate guess
    if len(guess) != 5:
        print("Guesses must be 5 letters")
        return False
    
    if wordExists(''.join(guess)) == False:
        print("Sorry, that is not a real word")
        return False

    # evaluate guess
    result = ""
    for i in range(len(solution)):
        if guess[i] == solution[i]:
            result += f"[green]{guess[i]}[/green] "
        elif guess[i] in solution:
            result += f"[yellow]{guess[i]}[/yellow] "
        else:
            result += f"{guess[i]} "
    
    # display response
    print(result.strip())

    # evaluate winning status
    return guess == solution 

    



# Main

# load word list
wordsFile = open("words.txt", "r")
data = wordsFile.read()
wordList = data.replace('\n', ' ').split(' ')

# select solution
solution = [*(random.choice(wordList))]

# set up console
console = Console()
console.clear()
console.bell()
print("Welcome to Wordle! Make your first guess:")
success = False

# run game
for i in range(6):
    success = makeGuess(solution)
    if success:
        break

# end game
if success:
    print("You Win! :thumbsup:")
else:
    print(f"Sorry, you lose :tired_face: The solution was {''.join(solution)}")




