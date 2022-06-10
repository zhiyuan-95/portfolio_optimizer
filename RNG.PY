import math
def LCG(seed,m):#linear congruential generators
    #1<a<m,0<c<m
    #m must be power of 2
    #a = 4n+1
    #then period = m
    n =seed
    a = 13
    c = 11
    U = 0
    out = []
    for x in range(m):
        n = (a*n+c)%m
        if x == 0:
            mark = n
        U = (n+0.5)/m
        out.append(U)
    return out
def MWC_optimaiser(m):#Multiply-with-Carry, it returns parameter “a” in a certain period which gives the longest period
#0 ≤ n < m, 0 ≤ c < a
    #m must be power of 2
    #n is seed
    c = 1
    n = 5
    period_list = []
    for a in range(1,10):
        signal =  True
        period = 0
        while signal == True:
            n1 = (a*n+c)%m
            c1 = (a*n+c)/m
            n = n1
            c = math.floor(c1)
            if period == 0:
                i = n
                j = c
            if n == i and c == j and period!=0:
                signal = False
                period_list.append((period, a))
            period+=1
        print((period, a))
    def takeFirst(elem):
        return elem[0]
    period_list.sort(key=takeFirst)
    return period_list[-1]
def MWC(n):
    # it generates (978/2)*2**16-1=32047103 random numbers
    c= 1
    a = 978#,1058
    m = 2**16
    output_list=[]
    i = 1;j=0
    signal = True
    period = 0
    five = 0
    while signal ==True:
        n1 = (a*n+c)%m
        c1 = (a*n+c)/m
        c = math.floor(c1)
        n = n1
        if i == n and j==c:
            signal = False
        if period==0:
            i = n
            j = c
#        print(n)
        if n==110:
            five+=1
        output_list.append(n)
        period+=1
    return output_list
x = LCG(0,32768)
print(x[0:10])
