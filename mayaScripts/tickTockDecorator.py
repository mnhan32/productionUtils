def ticktoc(func):
    import time
    tick = time.clock()
    def wrapper(*args, **kwargs):        
        return func(*args, **kwargs)
    tock = time.clock()
    print  'time logging %s : %f sec'%(func.__name__, (tock-tick))        
    return wrapper
