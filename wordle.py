import random
from rich.console import Console
import requests
import re
# Constants
NUMBERWORDS = ["[green]first[/green]", "[green]second[/green]", "[green]third[/green]",
               "[yellow]fourth[/yellow]","[yellow]fifth[/yellow]","[red]final[/red]"]

# Globals
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O",  "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
solution = ""
console = Console()

# Validates an input is a real word
def wordExists(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    return response.status_code == 200

# Finds letter in alphabet and sets formatting
def formatLetter(letter, formatting):
    idx = [i for i, item in enumerate(alphabet) if re.search(f"(^\[.+\]{letter}\[.+\]$)|(^{letter}$)", item)]
    print(idx)
    alphabet[idx[0]] = f"[{formatting}]{letter}[/{formatting}]"

# Receives an input, evaluates correctness, prints result
def makeGuess():
    # reveive guess
    guess = [*(input().upper())]
    result = {
        "guess": guess,
        "displayTxt": "",
        "success": False
    }

    if ''.join(guess) == 'EXIT':
        exit()

    # validate guess
    if len(guess) != 5:
        result.update({"displayTxt": f"[red]{' '.join(guess)}[/red] :x: not 5 letters"})
    elif wordExists(''.join(guess)) == False:
        result.update({"displayTxt": f"[red]{' '.join(guess)}[/red] :x: not a word"})
    # evaluate guess
    else:
        displayTxt = ""
        solutionCopy = solution.copy()

        for i in range(len(solution)):
            if guess[i] == solution[i]:
                displayTxt += f"[green]{guess[i]}[/green] "
                solutionCopy[i] = " "
                formatLetter(guess[i], "green")
            elif guess[i] in solutionCopy:
                displayTxt += f"[yellow]{guess[i]}[/yellow] "
                solutionCopy[solutionCopy.index(guess[i])] = " "
                formatLetter(guess[i], "yellow")

                
            else:
                displayTxt += f"{guess[i]} "
                try:
                    alphabet.remove(guess[i])
                except ValueError:
                    pass

        result.update({"displayTxt": displayTxt.strip(), "success": guess == solution})
        
    return result

# Prints the game so far
def showBoard(data):
    console.clear()
    for entry in data:
        console.print(entry["displayTxt"])


    



# Main

# load word list
wordsFile = open("words.txt", "r")
data = wordsFile.read()
wordList = data.replace('\n', ' ').split(' ')

# select solution
solution = [*(random.choice(wordList))]

# run game
gameResults = ["placeholder for turn", "placeholder for letters", {"displayTxt": ""}]
for i in range(6):
    gameResults[0] = {"displayTxt": f"Welcome to Wordle! Make your [bold]{NUMBERWORDS[i]}[/bold] guess:"}
    gameResults[1] = {"displayTxt": f"Available Letters: ({' '.join(alphabet)})"}
    showBoard(gameResults)
    result = makeGuess()
    gameResults.append(result)
    if result["success"]:
        break
        

# end game
if gameResults[-1]["success"]:
    gameResults.append({"displayTxt": "You Win! :thumbsup:"})
else:
    gameResults.append({"displayTxt": f"Sorry, you lose :tired_face: The solution was {''.join(solution)}"})

showBoard(gameResults)




