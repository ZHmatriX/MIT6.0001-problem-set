# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <仲逊>
# Collaborators : <17计算机科学与技术>
# Time spent    : <total time>

import math
import random
import string
from copy import deepcopy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    sc1=0
    word=word.lower()
    for char in word:
        if(char!='*'):
            sc1+=SCRABBLE_LETTER_VALUES[char]
        
    sc2=max(1,7*len(word)-3*(n-len(word)))
    
    return sc1*sc2

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    #print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
        
    hand['*'] = 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #拷贝一份手牌，word转为全小写
    hand_tem=deepcopy(hand)
    word=word.lower()
    #对于word中的每个字母，如果在手牌中，则将其数量减1
    for char in word:
        if(hand_tem.get(char,0)>0):
            hand_tem[char]=hand_tem[char]-1
            #数量减完就删除该手牌
            if(hand_tem[char]==0):
                del hand_tem[char]
    return hand_tem

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word=word.lower()
    
    #候选单词列表 如果没有*则列表只有一个word 
    #若有*则列表包含 将word中的 * 替换成5个元音字母的五个单词
    candidate_list=[]
    
    #候选手牌列表 如果没有*则列表只有hand一副手牌
    #若有*则列表包含 将hand中的 * 替换成5个元音字母的五副手牌
    hand_list=[]
    
    #每一个候选单词对应一副候选手牌
    #候选单词把word中的*替换成了什么字母，对应的候选手牌中就要加上这个字母
    
    #没有*则候选单词列表只有word，候选手牌列表只有hand
    if(word.find("*")==-1):
        candidate_list.append(word)
        hand_list.append(deepcopy(hand))
    #有*则候选单词列表包含五个单词，候选手牌列表包含五副手牌
    else:
        for vowel in VOWELS:
           candidate_list.append(word.replace("*",vowel))
           hand_tem=deepcopy(hand)
           hand_tem[vowel]=hand_tem.get(vowel,0)+1
           hand_list.append(hand_tem)
    
    is_valid=False
    #需要同时访问候选单词列表和候选手牌列表，用下标访问
    for  i in range(len(candidate_list)):
        candidate=candidate_list[i]
        #候选单词不在word_list里直接pass
        if candidate not in word_list:
            continue
        #候选单词在word_list，看看hand够不够用
        is_valid=True
        for char in candidate:
            #手牌字母不够用,置valid为false，break
            if char not in hand_list[i]:
                is_valid=False
                break
            #否则将手牌中的该字母数量减1
            else:
                hand_list[i][char]=hand_list[i][char]-1
                if hand_list[i][char]==0:
                    del hand_list[i][char]
        #valid为真，已经找到合法的单词，break
        if (is_valid):
            break
        
    return is_valid
    

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return sum(hand.values())

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    total_score=0
    handlen=calculate_handlen(hand)
    while(handlen>0):
        # 展示手牌
        print("\nCurrent Hand:",end=" ")
        display_hand(hand)
        word=input("Enter word, or \"!!\" to indicate that you are finished:")
        # 如果输入是!!则退出游戏
        if(word=="!!"):
            break   
        # 否则继续     
        else:
            # 如果单词合法
            if(is_valid_word(word, hand, word_list)):
                # 输出获得的分数，并且更新总分
                score=get_word_score(word, handlen)
                total_score+=score
                print("\"",word,"\"earned",score,"points. Total:",total_score,"points")
            # 单词不合法输出拒绝语句
            else:
                print("That is not a valid word. Please choose another word.")
            # 更新手牌
            hand=update_hand(hand, word)
        # 更新手牌长度
        handlen=calculate_handlen(hand)

    # 输出总分
    if(handlen==0):
        print("Ran out of letters.",end=" ")
    print("Total score:",total_score,"points")
    # 返回总分
    return total_score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    ans=deepcopy(hand)
    #将26英文字母转为列表
    can_choose=list(string.ascii_lowercase)
    #去除手牌中有的字母
    for char in hand.keys():
        if char in can_choose:
            can_choose.remove(char)
    #从剩下的字母中随机选一个替换手牌中的letter
    x = random.choice(can_choose)
    if(hand.get(letter, 0)>0):
        ans[x]=ans[letter]
        del ans[letter]

    return ans
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    all_hands_score=0      #每次的总分数的总和
    total_num_hands=int(input("Enter total number of hands:"))
    for num in range(total_num_hands):
        score=0
        hand=deal_hand(HAND_SIZE)
        print("\nCurrent Hand:",end=" ")
        # 展示手牌
        display_hand(hand)
        is_subs=input("Would you like to substitute a letter?")
        # 判断是否要换牌
        if(is_subs!="no"):
            subs_letter=input("Which letter would you like to replace:")
            hand=substitute_hand(hand, subs_letter)

        score=play_hand(hand, word_list)
        print("----------",end="")
        is_replay=input("Would you like to replay the hand?")
        # 判断是否重来一次 
        if(is_replay!="no"):
            # 如果是则重来一次 需要取较高分的一次(上述英文注释有要求)
            score=max(score,play_hand(hand, word_list))
            print("----------")
        # 更新总分数的总和
        all_hands_score+=score

    print("Total score over all hands:",all_hands_score)

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
