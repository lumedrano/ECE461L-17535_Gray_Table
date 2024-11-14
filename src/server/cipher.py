

##########used for encrypting and decrypting user data before storing in DB and to compare when logging in

def encrypt(inputText, N, D):

    #reverse the string
    reversed_string = inputText[::-1]
    
    #convert string to list
    listed_string = list(reversed_string)

    #shift each char
    for i in range(len(listed_string)):
        char = ord(listed_string[i])

        if 34 <= char <= 126: #encrypt valid chars in range
            #check D flag
            if D == 1: #shift right
                char = (char + N - 34) % 93 + 34
            elif D == -1:
                char = (char - N - 34) % 93 + 34
        listed_string[i] = chr(char) #unicode to char
    return ''.join(listed_string) #return in string format




def decrypt(inputText, N, D):

    #reverse the string
    reversed_string = inputText[::-1]
    
    #convert string to list
    listed_string = list(reversed_string)

    #shift each char
    for i in range(len(listed_string)):
        char = ord(listed_string[i])

        if 34 <= char <= 126: #encrypt valid chars in range
            #check D flag
            if D == 1: # if encrypted with shift right(reverse of encryption)
                char = (char - N - 34) % 93 + 34
            elif D == -1:
                char = (char + N - 34) % 93 + 34
        listed_string[i] = chr(char) #unicode to char
    return ''.join(listed_string) #return in string format