# simple generator
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

gen = infinite_sequence()
for i in range(10):
    print(next(gen))

# util function
def is_parlindrome(num):
    if num // 10 == 0:
        return False
    temp = num
    reversed_num = 0

    while temp != 0:
        reversed_num = reversed_num * 10 + temp % 10
        temp = temp // 10

    if num == reversed_num:
        return num
    else:
        return False

# build with generator expression
nums_squared_gc = (x ** 2 for x in range(10))
print(nums_squared_gc)

# yield
def multi_yield():
     yield_str = "This will print the first string"
     yield yield_str
     yield_str = "This will print the second string"
     yield yield_str
     yield_str = "This will print the third string"
     yield yield_str

gen = multi_yield()
while True:
    try:
        s = next(gen)
    except StopIteration:
        print("Stop")
        break
    print(s)

# advanced generator methods
def infinite_parlindromes():
    num = 0
    while True:
        if is_parlindrome(num):
            i = (yield num)
            if i is not None:
                num = i
        num += 1

pal_gen = infinite_parlindromes()
for i in pal_gen:
    print(i)
    digits = len(str(i))
    if digits == 7:
        # pal_gen.throw(ValueError("We don't like large palindromes"))
        # pal_gen.close()
        print("Stop")
        break
    # the generator will start at 10 ** digits iteration
    pal_gen.send(10 ** digits)

# creating pipelines with generators, one depending on another
file_name = "techcrunch.csv"
lines = (line for line in open(file_name, 'r'))
list_line = (s.rstrip().split(',') for s in lines)
# first iteration is the column names
cols = next(list_line)
company_dicts = (dict(zip(cols, data)) for data in list_line)
funding = (
    int(company_dict['raisedAmt'])
    for company_dict in company_dicts
    if company_dict['round'] == "a"
)
# calling sum will begin the iteration and return total amount
total_series_a = sum(funding)
print(f"Total series A fundraising: ${total_series_a}")
