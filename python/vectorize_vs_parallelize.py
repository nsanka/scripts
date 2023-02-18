import numpy as np
import time
import multiprocessing

#A function func is defined to multiply each elements in 'a' and 'b' into c
def func(a,b):
    c=0
    for i in range(1000000):
        c+=a[i]*b[i]
    return c


if __name__ == '__main__':
    a=np.random.rand(1000000) #Randomly assigning a million values to 'a'
    b=np.random.rand(1000000)
    print() #Blank line for better presentation of output
    #Traditional for-loop
    t1=time.time() #t1 is the time when this part of the code starts to execute
    c=func(a,b)
    t2=time.time() #t2 is the time when the for-loop computation is done

    print('Value of c : '+str(c))
    print('Time taken for traditional for-loop code :  '+ str(1000*(t2-t1)) + ' ms' )
    print()
    #t2-t1 gives the exact time taken for computation.
    #We multiply it by 1000 to view the result in milliseconds

    #Parallel Processing Code
    t1=time.time() #t1 is the time when this part of the code starts to execute

    pool = multiprocessing.Pool()
    c = pool.apply_async(func, args = (a,b))

    t2=time.time()
    print('Value of c : '+str(c.get()))
    print('Time taken for parallel processing code :  '+ str(1000*(t2-t1)) + ' ms' )
    print()

    #Vectorization
    t1=time.time()
    c=np.dot(a,b)
    t2=time.time()

    print('Value of c : '+str(c))
    print('Time taken for vectorized code           :  '+ str(1000*(t2-t1)) + ' ms' )
    print()