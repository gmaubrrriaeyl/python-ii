# Gabe Murray
# Last update: 27 Aug 20
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
    
    def __init__(self, first, last): #Constructor
        
        self.first = first.title()
        self.last = last.title()
        self.full = first.title() + ' ' + last.title()
        Contact.counter += 1
        self.ID = last + str(Contact.counter)
        if self.full not in Contact.roster:
            empid = str(self.last[:3]) + str(Contact.counter)
            Contact.roster.append(self.full)
        else:
            print("Contact already in roster")

    
    def getRoster(): #Accessors
        return Contact.roster
    def getContact(self):
        return self.full


        


gabe = Contact('gabe', 'murray') #Few defaults for the roster
prof = Contact('mark', 'prather')

def main():
    print("Program options")
    print("1. Display all contact")
    print("2. Create new contact")
    print("3. Exit")
    option = int(input("Enter 1,2, or 3: ")
    #if (isinstance(option, int) and (option<=3 and option>=1)):
    #    print("Not a valid option. Exiting..")
    if option == 1:
        return Contact.getRoster()
    elif option == 2:
        x = input("Enter contact in the following format: Doe, John" + '\n')
        x = x.split(',')
        x = [x.strip() for x in x]
        x = Contact(x[1], x[0])
    elif option == 3:
        print("Goodbye! Thanks for using my program :)")
