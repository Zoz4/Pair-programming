


if __name__ == '__main__':
    
    s = '123456789'
    t = list(s)
    t[0],t[-1] = t[-1],t[0]
    s2 = ''.join(t) 
    print(s)
    print(s.index('6'))
    print(s2)