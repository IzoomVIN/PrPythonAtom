def simple_decorator(function):
    def check_func(n):
        if n <= -1:
            raise "this number is less whan zero!"
        else:
            return function(n)
    return check_func
	
@simple_decorator
def fib(n):
    if n == 1 or n == 0:
        return 1
    else:
        return fib(n-1) + fib(n-2)