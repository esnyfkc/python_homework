def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())
        display = "".join(char if char.lower() in guesses else "_" for char in secret_word)
        print(display)
        return all(char.lower() in guesses for char in secret_word)

    return hangman_closure

if __name__ == "__main__":
    secret_word = input("Enter the secret word: ")
    guess_word = make_hangman(secret_word)

    solved = False
    while not solved:
        letter = input("guess a letter: ")
        solved = guess_word(letter)
    print("You guessed it! The word was: ", secret_word)



