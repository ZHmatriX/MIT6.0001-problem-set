# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    #对于secret_word中的所有字母，只要有一个不在letters_guessed中就返回False
    #全部都在则返回True
    for char in secret_word:
        isExist=False
        for letter in letters_guessed:
            if(letter==char):
                isExist=True
                break
        if(isExist==False):
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
 
    ans=""
    #依次判断secret_word中的字母是否被猜到
    #是则将字母加入ans，否则将“_ ”加入ans
    for char in secret_word:
        if(char in letters_guessed):
            ans+=char
        else:
            ans+="_ "
    return ans



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    #将26英文字母转为列表
    ans=list(string.ascii_lowercase)
    #去除被猜到的字母
    for char in letters_guessed:
        if char in ans:
            ans.remove(char)
    #返回ans中元素组成的字符串
    return "".join(ans)
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    secret_word="tact"
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is ",len(secret_word)," letters long.")
    
    warning_left=3        #剩余的warning次数
    times_left=6          #剩余可以猜的次数
    letters_guessed=""    #已经猜过的字母
    is_win=False          #是否赢得比赛
    print("You have ",warning_left," warnings left.")
    while(times_left>0):
        #更新可使用的字母表
        available_letters=get_available_letters(letters_guessed)
        #更新需要显示的已猜中字母 例如“a_ b_”
        guessed_print=get_guessed_word(secret_word,letters_guessed)
        
        print("-------------")
        print("You have ",times_left," guesses left.")
        print("Available letters: "+available_letters)
        letter=input("Please guess a letter: ").lower()
        
        #如果输入不是字母或者超过一个字母，warning
        if (not letter.isalpha() or len(letter)!=1):
            #若剩余warning大于0，扣warning，否则扣次数
            if(warning_left>0):
                warning_left=warning_left-1
                print("Oops! That is not a valid letter. You have", warning_left, "warnings left:")
            else:
                times_left-=1
                print("Oops! That is not a valid letter. You have no warnings left")
                print("so you lose one guess:",end="")
            print(guessed_print)
            
        #如果输入字母不在可选字母表内，warning
        elif letter not in available_letters:
             #若剩余warning大于0，扣warning，否则扣次数
            if(warning_left>0):
                warning_left=warning_left-1
                print("Oops! You've already guessed that letter. You have",warning_left,"warnings left:")
            else:
                times_left-=1
                print("Oops! You've already guessed that letter. You have no warnings left")
                print("so you lose one guess:",end="")
            print(guessed_print)
            
        #如果猜中，剩余次数不减，猜的字母加入letters_guessed
        elif letter in secret_word:
            letters_guessed+=letter
            guessed_print=get_guessed_word(secret_word,letters_guessed)
            print("Good guess:"+guessed_print)
            
        #未猜中，是元音字母剩余次数减2，猜的字母加入letters_guessed
        elif letter in ['a','e','i','o','u']:
            times_left-=2
            letters_guessed+=letter
            print("Oops! That letter is not in my word:"+guessed_print)
        
        #未猜中，不是元音字母剩余次数减1，猜的字母加入letters_guessed   
        else:
            times_left-=1
            letters_guessed+=letter
            print("Oops! That letter is not in my word:"+guessed_print)   
        #若已经猜中所有字母，将is_win置为True，直接break
        if(is_word_guessed(secret_word,letters_guessed)):
            is_win=True
            break
    
    #赢则输出分数，否则输出该secret word
    if(is_win):
        print("Congratulations, you won!")
        print("Your total score for this game is:",times_left*(len(set(secret_word))))
    else:
        print("Sorry, you ran out of guesses. The word was "+secret_word+".")




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    #去除my_word中所有空格
    my_word=my_word.replace(" ","")
    #长度不同返回false
    if(len(my_word)!=len(other_word)):
        return False
    
    #为了方便下标对应，使用C式语言的下标循环遍历
    #在my_word[i]=='_'时，将other_word[i]以及其他所有等于other_word[i]的字符替换为'_'
    for index in range(0,len(my_word)):
        if(my_word[index]=="_"):
            other_word=other_word.replace(other_word[index],"_")
     #处理完毕后只需比较两字符串是否相等即可
    if(my_word==other_word):
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    #对于wordlist中的每个单词，若与my_word匹配，则输出
    is_exist=False
    for word in wordlist:
        if(match_with_gaps(my_word, word)):
            is_exist=True
            print(word,end=' ')
    if(is_exist):
        print()
    else:
        print("No matches found")

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    #secret_word="tact"
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is ",len(secret_word)," letters long.")
    
    warning_left=3        #剩余的warning次数
    times_left=6          #剩余可以猜的次数
    letters_guessed=""    #已经猜过的字母
    is_win=False          #是否赢得比赛
    print("You have ",warning_left," warnings left.")
    while(times_left>0):
        #更新可使用的字母表
        available_letters=get_available_letters(letters_guessed)
        #更新需要显示的已猜中字母 例如“a_ b_”
        guessed_print=get_guessed_word(secret_word,letters_guessed)
        
        print("-------------")
        print("You have ",times_left," guesses left.")
        print("Available letters: "+available_letters)
        letter=input("Please guess a letter: ").lower()
        
        #如果输入是*,输出所有匹配
        if(letter=="*"):
            print("Possible word matches are:")
            show_possible_matches(guessed_print)
            
        #如果输入不是字母，不是*或者超过一个字母，warning
        elif (not letter.isalpha() or len(letter)!=1):
            #若剩余warning大于0，扣warning，否则扣次数
            if(warning_left>0):
                warning_left=warning_left-1
                print("Oops! That is not a valid letter. You have", warning_left, "warnings left:")
            else:
                times_left-=1
                print("Oops! That is not a valid letter. You have no warnings left")
                print("so you lose one guess:",end="")
            print(guessed_print)
            
        #如果输入字母不在可选字母表内，warning
        elif letter not in available_letters:
             #若剩余warning大于0，扣warning，否则扣次数
            if(warning_left>0):
                warning_left=warning_left-1
                print("Oops! You've already guessed that letter. You have",warning_left,"warnings left:")
            else:
                times_left-=1
                print("Oops! You've already guessed that letter. You have no warnings left")
                print("so you lose one guess:",end="")
            print(guessed_print)
            
        #如果猜中，剩余次数不减，猜的字母加入letters_guessed
        elif letter in secret_word:
            letters_guessed+=letter
            guessed_print=get_guessed_word(secret_word,letters_guessed)
            print("Good guess:"+guessed_print)
            
        #未猜中，是元音字母剩余次数减2，猜的字母加入letters_guessed
        elif letter in ['a','e','i','o','u']:
            times_left-=2
            letters_guessed+=letter
            print("Oops! That letter is not in my word:"+guessed_print)
        
        #未猜中，不是元音字母剩余次数减1，猜的字母加入letters_guessed   
        else:
            times_left-=1
            letters_guessed+=letter
            print("Oops! That letter is not in my word:"+guessed_print)
            
        #若已经猜中所有字母，将is_win置为True，直接break
        if(is_word_guessed(secret_word,letters_guessed)):
            is_win=True
            break
    
    #赢则输出分数，否则输出该secret word
    if(is_win):
        print("Congratulations, you won!")
        print("Your total score for this game is:",times_left*(len(set(secret_word))))
    else:
        print("Sorry, you ran out of guesses. The word was "+secret_word+".")





# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
