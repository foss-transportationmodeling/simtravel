






class Households(object):
    def __init__(self, hid):
        self.hid = hid
        self.persons = []

    def add_person(self, person):
        # person is an object of the Person class
        self.persons.append(person)




