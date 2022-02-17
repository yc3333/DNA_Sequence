import math
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import I 

def lcstr(X, Y):
    m = len(X)
    n = len(Y)

    L = [[0 for k in range(n+1)] for l in range(m+1)]
    result = 0
    for i in range(m + 1):
        for j in range(n + 1):
            if (i == 0 or j == 0):
                L[i][j] = 0
            elif (X[i-1] == Y[j-1]):
                L[i][j] = L[i-1][j-1] + 1
                result = max(result, L[i][j])
            else:
                L[i][j] = 0
    return result

def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)
  
    # declaring the array for storing the dp values
    L = [[None]*(n + 1) for i in range(m + 1)]
  
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
  
    return L[m][n]

def editDist(X, Y):
    m = len(X)
    n = len(Y)

    L = [[0 for x in range(n + 1)] for x in range(m + 1)]
  
    for i in range(m + 1):
        for j in range(n + 1):
  
            if i == 0:
                L[i][j] = j    
  
            elif j == 0:
                L[i][j] = i   
  
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]
  
            else:
                L[i][j] = 1 + min(L[i][j-1],        # Insert
                                   L[i-1][j],        # Remove
                                   L[i-1][j-1])    # Replace
    return L[m][n]

gap_penalty = -1
match_award = 1
mismatch_penalty = -1

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    else:
        return mismatch_penalty

def needleman_wunsch(X, Y):
    
    n = len(X)
    m = len(Y)  
    
    L = [[0 for x in range(n + 1)] for x in range(m + 1)]
   
    for i in range(0, m + 1):
        L[i][0] = gap_penalty * i
    
    for j in range(0, n + 1):
        L[0][j] = gap_penalty * j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = L[i - 1][j - 1] + match_score(X[j-1], Y[i-1])
            delete = L[i - 1][j] + gap_penalty
            insert = L[i][j - 1] + gap_penalty
            L[i][j] = max(match, delete, insert)

    return L[m][n]

def main():
    layout = [[sg.Text('Please enter DNA files:', font=("Times New Roman", 20))],
            [sg.Text('DNA query', size=(15, 2),font=("Times New Roman", 20)), sg.Input(size=(50,2),font=("Times New Roman", 15)), sg.FileBrowse(size=(6,2))],
            [sg.Text('DNA sequences', size=(15, 2),font=("Times New Roman", 20)), sg.Input(size=(50,2),font=("Times New Roman", 15)), sg.FileBrowse(size=(6,2))],
            [sg.Submit(size=(6,2)), sg.Cancel(size=(6,2))]]

    window = sg.Window('DNA Sequence Matching Program', layout, size=(800,250))

    event, values = window.read()
    window.close()

    # get query DNA
    f = open(values[0], "r")
    DNA_search = f.read()
    f.close()

    # get sequence DNAs
    f = open(values[1], "r")
    DNA_seq = f.read()
    DNA_seq = DNA_seq.split(">")[1:]
    DNA_name = []
    DNA_list = []
    for DNA in DNA_seq:
        split = DNA.split("\n")
        DNA_name.append(split[0])
        split = split[1:]
        seq = ""
        for item in split:
            seq += item
        DNA_list.append(seq)

    layout1 = [[sg.Text("Query file: "+values[0], font=("Times New Roman", 15))],
            [sg.Text("Sequence file: "+values[1], font=("Times New Roman", 15))],
            [sg.Text("Choose what algorithm you want to use:", font=("Times New Roman", 20))],
            [sg.Button("Longest Common Substring", k='LCstr', size=(30,2)), sg.Button("Longest Common Subsequence", k='LCS', size=(30,2)), sg.Button("Edit distance", k='ED', size=(30,2))],
            [sg.Button("needleman-wunsch algorithm", k='nw', size=(30,2)), sg.Button("Our Own Design", k='own', size=(30,2))],
            [sg.Output(size=(90,10), k='-OUTPUT-',font=("Times New Roman", 15))],
            [sg.Button("Clear", size=(6,2)),sg.Button("Exit", size=(6,2))]]

    window1 = sg.Window("Result", layout1)

    while True:
        event1, values1 = window1.read()
        if event1 == 'Exit' or event1 == sg.WIN_CLOSED:
            break
        elif event1 == "LCS":
            # find longest common subseqeunce best result
            LCS_result = 0
            index = -1
            for i in range(10):
                result = lcs(DNA_search, DNA_list[i])
                if result > LCS_result:
                    LCS_result = result
                    index = i
            print("Longest common subsequence best result: " + DNA_name[index])
        elif event1 == 'LCstr':
            LCStr_result = 0
            index = -1
            for i in range(10):
                result = lcstr(DNA_search, DNA_list[i])
                if result > LCStr_result:
                    LCStr_result = result
                    index = i
            print("Longest common substring best result: " + DNA_name[index])
        elif event1 == 'ED':
            ED_result = 5000
            index = -1
            for i in range(10):
                result = editDist(DNA_search, DNA_list[i])
                if result < ED_result:
                    ED_result = result
                    index = i
            print("Edit distance best result: " + DNA_name[index])
        elif event1 == 'nw':
            nw_result = -5000
            index = -1
            for i in range(10):
                result = needleman_wunsch(DNA_search, DNA_list[i])
                if result > nw_result:
                    nw_result = result
                    index = i
            print("needleman wunsch algorithm best result: " + DNA_name[index])
        elif event1 == 'own':
            own_result = -5000
            index = -1
            for i in range(10):
                result1 = lcs(DNA_search, DNA_list[i]) / math.log(abs((len(DNA_search) - len(DNA_list[i]))),2)
                result2 = editDist(DNA_search, DNA_list[i]) / math.log(abs((len(DNA_search) - len(DNA_list[i]))),2)
                result = result1 / result2
                if result > own_result:
                    own_result = result
                    index = i
            print("own design best result: " + DNA_name[index])
        elif event1 == "Clear":
            window1['-OUTPUT-'].update('')
            
    window1.close()




if __name__ == "__main__":
    main()
