import re
import numpy as np


# PART 1: Processing game strings
# These functions, leading up to format_game, are designed to process 

def remove_braces(s):
    '''
    Removes any segments of the string s that are in braces.  For example,
    'This {is a} message { }' becomes 'This  message '.
    '''
    is_brace = 0
    output = ''
    for i in range(len(s)):
        if s[i]=='{':
            is_brace = 1
        if is_brace == 0:
            output += s[i]
            continue
        else:
            if s[i] == '}':
                is_brace=0
                continue
    
    return output




#Get rid of the move numbers
def remove_numbers(s):
    return re.sub( '\d+\.+' , '', s).lstrip()



#Remove the ending 0-1, 1-0, or 1/2-1/2 from the string
def remove_ending(s):
    if (s[-3:]=='0-1') or (s[-3:]=='1-0'):
        return s[:-3].rstrip()
    elif s[-7:]=='1/2-1/2':
        return s[:-7].rstrip()



#Remove any question marks and exclamation marks
def remove_marks(s):
    return re.sub('(\?|\!)+', '', s)


#Turn any spaces into single spaces
def format_spaces(s):
    return re.sub('\s+', ' ', s)


#Function to format the 'AN' column into a string that the "chess" library can process
def format_game(s):
    '''
    Function to format the 'AN' column into a string that the "chess" library can process.
    Just split the string on its spaces to get the sequence of moves.
    '''
    return format_spaces(remove_marks(remove_ending(remove_numbers(remove_braces(s)))))










# PART 2: Elo and Glicko Scores


def elo_expectation(p1_rating, p2_rating):
    '''
    Inputs: The ratings of the two players (assuming the Lichess.org ratings scale)
    Output: The predicted probability (from the Elo model) that player 1 wins
            if players 1 and 2 were to play each other
    '''
    return 1/(1+10**(-(p1_rating - p2_rating)/400))



#Constant used for Glicko scoring
q = np.log(10)/400


#Function used for Glicko scoring
def g(x):
    return 1/(1+3 * (x**2) * (q**2)/((np.pi)**2) )**.5



def glicko_expectation(p1_rating, p2_rating, p1_RD, p2_RD):
    '''
    Inputs: The ratings and "ratings deviations" of the two players (assuming the Lichess.org ratings scale)
    Output: The predicted probability (from the Glicko1 model) that player 1 wins
            if players 1 and 2 were to play each other
    '''
    return 1/(1+10**(-(p1_rating - p2_rating)/400 * g((p1_RD**2 + p2_RD**2)**.5) ) ) 