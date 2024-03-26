#different functions that use the text input
#and apply the critera(format,limit) of the ai response, see whether it passes or not
import re

def validate(text,output_format,params={}):
    bStrict = True #by default
    if 'strict'in params.keys():bStrict = params['strict']
    if output_format == 'number':
        temp = "(^\d+$)" #strict criteria
        if not bStrict:temp = "(\d+)" #define loose criteria check if at least one number is in the text

        res =re.search(temp,text)
        if res:return res.span() #if you find the number, where the position, and the size of the str
        return False #no result find
    elif output_format == 'list_of_numbers': # to test if it is a list numbers (floats or integers)
        # 1. Define the template regexp for the list -> https://regex101.com/  and test [1.3,2,5.4]
        if bStrict: # the diff bt the strict and loose is the template
            temp = "^(\d+\.?\d*)?(\s*\,\s*(\d+\.?\d*))*$"
        else:
            temp = "\s*(\d+\.?\d*)?(\s*\,\s*(\d+\.?\d*))*\s*" 
        
        # 2. Find an occurence of the list
        res = re.search(temp,text)
        if res:return res.span()
        return False
    elif output_format == 'list_of_numbers_in_range':
        aRange = params['aRange']
        fctToNumber = int
        if 'fctToNumber' in params: fctToNumber = params['fctToNumber']

        # 1. Validate the occurence of a list of numbers in the text
        valid = validate(text, 'list_of_numbers', params)
        if not valid: return False
        if valid[1] - valid[0] <= 1: return []
        
        # 2. Extract the list of numbers as a substring of the text -> in python strings are arrays
        sListOfNumbers = text[valid[0]:valid[1]+1] #the begining and the end; we should have sth that can be transfromed into a list
        # print(sListOfNumbers)

        # 3. Transform the substring into a list 
        # '[1, 2.3, 5.4]' -> '1, 2.3, 5.4'
        # split(): breaks a string  into elements
        listOfStringValues = ((sListOfNumbers.replace(" ", "")).split(",")) # ['1', '2.3', '5.4'] -> [1, 2.3, 5.4]
        try:
            listOfNumbers = [fctToNumber(value) for value in listOfStringValues]
        except ValueError:
            return []
        # print(listOfNumbers)

        # 4. Check if each element of the list belong to the given range
        # all() : tests if all elements of a list are True
        # map() : maps a function onto each element of a list
        # lambda: anonymous function
        # 4.1 Create a function to test if a value is in a given range
        fctRestRange = lambda value: value in aRange
        # 4.2 Map the (lambda) function to each value of the list of numbers
        bTestedRange = map(fctRestRange, listOfNumbers)
        # for b in bTestedRange: print(b)


        if all(bTestedRange): return listOfNumbers
        return False
    #of the list - reliable the measuring validation, to ease the coloring to change the representation



def main():
    print("main function")
#saperate the main and the loading
if __name__ == '__main__': main() 
