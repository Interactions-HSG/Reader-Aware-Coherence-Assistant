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
        if res:return res.span() #if you find the number, where the position
        return False #no result find
    elif output_format == '3positions_list': # to test if it is a list of given value
        pass #require the valiation 1)ask py to transact the result to list - try accept block 2)go through the list loop each element
    #of the list - reliable the measuring validation, to ease the coloring to change the representation



def main():
    print("main function")
#saperate the main and the loading
if __name__ == '__main__': main() 
