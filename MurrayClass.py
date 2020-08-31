# Gabe Murray
# Last update: 31 Aug 20
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
    
    def __init__(self, last, first): #Constructor
        
        self.first = first.title()
        self.last = last.title()
        self.full = first.title() + ' ' + last.title()
        Contact.counter += 1
        self.ID = last[:3].lower() + str(Contact.counter)
        
        if self.full not in Contact.roster:
            ID = str(self.last[:3]) + str(Contact.counter)
            Contact.roster.append(self.full)
        else:
            print("Contact already in roster.")

    
    def getRoster(): #Accessors
        return Contact.roster
    def getContact(self):
        return self.full


gabe = Contact('murray', 'gabe') #Few defaults for the roster
prof = Contact('prather', 'mark')


def main():
    print("Program options")
    choices = str("1. Display all contact \n2. Create new contact\n3. Exit")

    
    while True:
        print(choices)
        option = int(input("Enter 1,2, or 3: "))
        if not (isinstance(option, int) and (option<=3 and option>=1)):
            print("Not a valid option.\n" + choices)
        if option == 1:
            print(str(Contact.getRoster()) + '\n')
            continue
        elif option == 2:
            x = input("Enter contact in the following format: Doe, John" + '\n')
            x = x.split(',')
            x = [x.strip() for x in x]
            if x not in Contact.roster:
                x = Contact(x[0], x[1])
                print(str(Contact.roster[-1] + " has been added to your contacts. Their contact id is " + x.ID + ". \n\n"))
            
            continue
        elif option == 3:
            return print("Goodbye World!")
            
if __name__ == "main":
    main()
