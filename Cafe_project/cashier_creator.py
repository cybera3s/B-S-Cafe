import argparse, re

class Cashier:
    def __init__(self,fname, lname, phonenumber, email, password):
        self.firstname=fname
        self.lastname=lname
        self.phonenumber=phonenumber
        self.email=email
        self.password=password

    def __str__(self):
        return f"{self.firstname},{self.lastname},{self.phonenumber},{self.email},{self.password}"

if __name__=="__main__":

    parser=argparse.ArgumentParser()

    parser.add_argument('-l', '--lastname')
    parser.add_argument('-f', '--firstname')
    parser.add_argument('-p', '--phonenumber')
    parser.add_argument('-e', '--email')
    parser.add_argument('-k', '--password')

#arguments=parser.parse_args()
args = parser.parse_args()
#firstname=input('please enter your first name :')
print(args.firstname)
print(args.lastname)
print(args.phonenumber)
print(args.email)
print(args.password)

def validate_firstname(firstname): #firstname
    pattern = r'[a-zA-Z]'
    if re.search(pattern,firstname):
        print('valid firstname')
    else:
        raise Exception('invalid firstname')

def validate_lastname(lastname):
    pattern=r'[a-zA-Z]'
    if re.search(pattern,lastname):
        print('valid lastname')
    else:
        raise Exception('invalid lastname')

def validate_phonenumber(phonenumber):
    pattern=r'[^'+'0-9]'
    if re.search(pattern,phonenumber):
        print('valid phonenumber')
    else:
        raise Exception('invalid phonenumber')

def validate_email(email):
    pattern= r'[a-zA-Z0-9]+@(host)+\.(domain)'
    if re.search(pattern, email):
        print('valid email')
    else:
        raise Exception('invalid email')

def validate_password(password):
    pattern=r'(\w{6,16})'
    if re.search(pattern,password):
        print('valid password')
    else:
        raise Exception('invalid password')



    validate_firstname(args.firstname)
    validate_lastname(args.lastname)
    validate_phonenumber(args.phonenumber)
    validate_email(args.email)
    validate_password(args.password)






