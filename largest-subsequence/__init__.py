'''
Simple O(n) solution to largest subarray of integers.

@input an array of integers
'''
def largestSubSequence(input):
    if not input :
        raise Error("empty input!")
    
    largestSum = input[0]
    bestStartPos = bestEndPos = runningStartPos = sum = 0
    
    for x in range(len(input)) :
         sum += input[x]
         if sum > largestSum :
             largestSum = sum
             bestStartPos = runningStartPos
             bestEndPos = x
         elif sum <= 0 :
             runningStartPos = x+1
             sum = 0
         
    print "Largest Sum: %i [%i,%i]" % (largestSum, bestStartPos, bestEndPos)
    
    
if __name__ == "__main__" :
    case1 = (5, -1, 3, 7, -9, 5, 10, 15, -3)
    largestSubSequence(case1)
    #expected: 0, 7 = 35
    
    case2 = (5, -1, 3, 7, -19, 5, 10, 15, -3)
    largestSubSequence(case2)
    #expected 5, 7 = 30
    
    case3 = (5, -1, 3, 7, -19, 5, 10, 15, -999, 1000)
    largestSubSequence(case3)
    #expected 9, 9 = 1000
    
    case4 = (-1, -2, -3, -4, -5)
    largestSubSequence(case4)
    #expected 0, 0 = -1