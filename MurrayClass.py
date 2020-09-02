# Gabe Murray
# Last update: 2 Sep 20
# Python II, Professor Prather
# Program 1. Classes

"""
Must have the followin functionality
1. display all contacts
2. create new contacts
3. exit

"""

class Contact:
    counter = 0
    roster = []
    
    def getCount():
        return Contact.counter
    
    def __init__(self, last, first, email): #Constructor
        
        self.first = first.title()
        self.last = last.title()
        self.email = email
        self.full = first.title() + ' ' + last.title()

        if not any(i['full'] == self.full for i in Contact.roster):        
            ID = str(self.last[:3]).lower() + str(Contact.counter+1)
            first = self.first.title()
            last = self.last.title()
            full = self.full.title()
            entry = {
                'first' : first,
                'last' : last,
                'email' : email,
                'ID' : ID,
                'full' : full
                }
            Contact.roster.append(entry)
            print(str(Contact.roster[-1]['last'] +', ' + Contact.roster[-1]['first'] + ' has been added to the roster.'))
            Contact.counter += 1
            
        else:
            print(self.full + " is already in roster.")

    
    def getRoster(): #Accessors
        print("="*65)
        print("{0:<20}{1:20}{2:20}".format('First Name','Last Name','Email'))
        for i in range(Contact.counter):
            print("{0:<20}{1:20}{2:20}".format(Contact.roster[i]['first'],Contact.roster[i]['last'],Contact.roster[i]['email']))
        print("="*65)


    def getContact(self):
        return self.full


gabe = Contact('murray', 'gabe', 'murray@email.com') #Few defaults for the roster
prof = Contact('prather', 'mark', 'prather@email.com')


def main():
    print("Program options")
    choices = str("1. Display all contact \n2. Create new contact\n3. Exit")

    
    while True:
        print(choices)
        
        try: # Error catching
            option = int(input("Enter 1, 2, or 3: "))
        except UnboundLocalError:
            print("Not a valid option. \n")
            continue
        except ValueError:
            print("Not a valid option. \n")
            continue
        if option >3 or option < 1:
            print("Not a valid option. \n")
            continue
        
        if option == 1:
            Contact.getRoster()
            continue
        
        elif option == 2:
            x = input("Enter contact in the following format: LastName, FirstName, Email" + '\n')
            x = x.split(',')
            x = [x.strip() for x in x]
            if x not in Contact.roster:
                try:
                    x = Contact(x[0], x[1], x[2])
                except:
                    print("Incorrect format. Please try again.")
            
            continue
        elif option == 3:
            return print("Goodbye World!")



if __name__ == "main":
    main()
