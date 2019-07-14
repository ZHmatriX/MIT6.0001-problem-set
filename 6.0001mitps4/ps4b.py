# Problem Set 4B
# Name: <仲逊>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text=text
        self.valid_words=load_words("words.txt")

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lowercase=string.ascii_lowercase
        uppercase=string.ascii_uppercase
        ans={}
        #将每个字母移位通过将他们的ASCII码加上对应数值实现,超出a-z范围注意取模
        #ASCII->Char用chr函数  Char->ASCII用ord函数
        for i in range(26):
            ans[lowercase[i]]=chr(97+(ord(lowercase[i])-97+shift)%26)
            ans[uppercase[i]]=chr(65+(ord(uppercase[i])-65+shift)%26)
            
        return ans

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        #string不可变 先转list
        shifted_meg=list(self.message_text)
        shift_map=self.build_shift_dict(shift)
        
        #对于shift_dict存在键的字符char,将其改为对应值,否则保持不变,即还是char
        for i in range(len(shifted_meg)):
            shifted_meg[i]=shift_map.get(shifted_meg[i],shifted_meg[i])
        
        return "".join(shifted_meg)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        super().__init__(text)
        self.shift=shift
        #调用父类函数建立加密映射表和密文
        self.encryption_dict=self.build_shift_dict(shift)
        self.message_text_encrypted=self.apply_shift(shift)
        
    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift=shift


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_shift=0      #最优位移
        best_valid_num=0  #最优合法单词数
        #对于0-26每个shift值
        for shift in range(26):
            valid_num=0
            #得到shift后的语句
            shifted_meg=self.apply_shift(shift)
            #将语句分割为单词
            word_list=[msg for msg in shifted_meg.split(' ')]
            #如果单词合法则valid_num++
            for word in word_list:
                if is_word(self.valid_words,word):
                    valid_num+=1
            #如果这个shift的表现比之前的好，更新最优位移和最优合法单词数      
            if valid_num>best_valid_num:
                best_valid_num=valid_num
                best_shift=shift
                
        #返回最优位移和解码后的语句
        return best_shift,self.apply_shift(best_shift)

if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #test case(PlaintextMessage)1
    plaintext = PlaintextMessage('convolutional neural network', 4)
    print('Expected Output: gsrzspyxmsrep riyvep rixasvo')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    
    #test case (CiphertextMessage)1
    ciphertext = CiphertextMessage('gsrzspyxmsrep riyvep rixasvo')
    print('Expected Output:', (22, 'convolutional neural network'))
    print('Actual Output:', ciphertext.decrypt_message())
    
    #test case (PlaintextMessage)2
    plaintext = PlaintextMessage('I\'m the bone of my sword, unlimited blade works',12)
    print('Expected Output: U\'y ftq nazq ar yk eiadp, gzxuyufqp nxmpq iadwe')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    
    #test case (CiphertextMessage)2
    ciphertext = CiphertextMessage('U\'y ftq nazq ar yk eiadp, gzxuyufqp nxmpq iadwe')
    print('Expected Output:', (14, 'I\'m the bone of my sword, unlimited blade works'))
    print('Actual Output:', ciphertext.decrypt_message())
    
    #best shift value and unencrypted story
    cipherstory = CiphertextMessage(get_story_string())
    print("best shift: ",cipherstory.decrypt_message()[0])
    print("unencrypted story:\n",cipherstory.decrypt_message()[1])
    
    
