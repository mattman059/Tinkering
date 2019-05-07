#prime.py

primes = []

def genPrime(n): #Generate first n prime numbers
    prime=True
    for i in range(2,n+1):
        #prime is only divisible by itself and 1
        #can't be divided by anything higher than N
        for j in range (2, i):
            #print(str(i) + " % " + str(j) + " = " + str(i % j))
            if i % j == 0:
                prime=False
                break
            else:
                prime=True

        if prime:
            primes.append(i)


genPrime(15)
print(primes)    
