import random


class deck:
    '''
    A class for simulating deck shuffling
    __init__: Initializes the deck. Creates a sorted list of numbers 1-52; sets the number of times sorted to 0
    sort: Replaces the list with a new one, with range 1-52; increases the timesSorted variable by 1
    shuffle_once: applies one round of the overhand shuffle
    save_probabilities: updates the occurrences variable to show how often each card appears in each position
    shuffle_save: applies the shuffling and then saves the probabilities to the occurrences variable
    get_standard_deviation: Converts occurrences to probabilities, then gets the standard deviation of those probabilities
    '''

    def __init__(self):
        # Initializes the deck

        # Create a new list from 1-52
        self.lst = []
        for card in range(1, 53):
            self.lst.append(card)

        # Reset occurrences
        self.occurrences = []
        for i in range(52):
            self.occurrences.append([0] * 52)

        # Set the times sorted to 0. Used to calculate standard deviation.
        self.timesSorted = 0

    def sort(self):
        # Sorts the deck - Resets the list so that it's 1-52.

        # Resets the list
        self.lst = []
        for card in range(1, 53):
            self.lst.append(card)

        # Increment the timesSorted by 1.
        self.timesSorted += 1

    def shuffle_once(self, minTake, maxTake, minPlace, maxPlace):
        '''
        Shuffles the deck once with the overhand method
        :param minTake: Sets the minimum number of cards we can take from the back
        :param maxTake: Sets the maximum number of cards we can take from the back
        :param minPlace: Sets the minimum number of cards we can place at the front
        :param maxPlace: Sets the maximum number of cards we can place at the front
        :return: Nothing
        '''

        # Decide how many cards we take from the back
        takeFromBack = random.randint(minTake, maxTake)

        # Seperate the deck into our two new decks
        newList = self.lst[-takeFromBack:]
        for i in range(takeFromBack):
            self.lst.pop()

        # While our new deck is not empty
        while (len(newList) > 0):
            # Make sure we're not crossing (minSelect<maxSelect)
            minSelect = minPlace
            maxSelect = min(maxPlace, len(newList))
            # If len(newList)<minPlace, then we might get an error
            temp = minSelect
            minSelect = min(temp, maxSelect)
            maxSelect = max(temp, maxSelect)

            # Decide however many we can put back, then put that at the front of the old deck and remove it from the new deck.
            putBack = random.randint(minSelect, maxSelect)
            self.lst = newList[:putBack] + self.lst
            newList = newList[putBack:]

    def save_probabilities(self):
        # Save the number of times the cards appear in each position

        # For each position in the deck
        for i in range(len(self.lst)):
            # Select which card number was at that position, and increment that position in our occurrences variable.
            self.occurrences[i][self.lst[i] - 1] += 1

    def shuffle_save(self, minTake, maxTake, minPlace, maxPlace, shuffles):
        '''
        Shuffle the deck multiple times and save the occurrences.
        :param minTake: Minimum number of cards we can take from the back
        :param maxTake: Maximum number of cards we can take from the back
        :param minPlace: Minimum number of cards we can place at the front
        :param maxPlace: Maximum number of cards we can place at the front
        :param shuffles: Number of times we apply the shuffle
        :return: None
        '''
        for shuffleNum in range(shuffles):
            self.shuffle_once(minTake, maxTake, minPlace, maxPlace)
        self.save_probabilities()

    def get_standard_deviation(self):
        # Calculates the probabilities each card is in each position and calcualte standard deviation
        # return: standard deviation

        sum = 0
        # For each position
        for line in self.occurrences:
            # For each card that could be there
            for val in line:
                # Calculate the sum
                sum += ((1 / 52) - val/self.timesSorted) ** 2
        # Divide by N and sqrt it
        sum = sum / (52 * 52 - 1)
        sum = (sum) ** 0.5
        return sum


def test_selections(minTakes_, maxTakes_, maxTests):
    '''
    Runs the code that checks how changing the selections affects the efficiency of shuffling
    :param minTakes_: Minimum cards we can take from the back
    :param maxTakes_: Maximum cards we can take from the back
    :param maxTests: Maximum number of tests we apply
    :return:
    '''

    # Create scores, stores the standard deviation.
    scores = []
    for i in range(52):
        scores.append([''] * 52)

    # Test all values from 1-minTakes_
    for minTakes in range(1,minTakes_):
        # Used to check how long the code will take to run
        #print(minTakes)
        # Test all values from minTakes-maxTakes
        for maxTakes in range(minTakes, maxTakes_):
            # Create a new deck
            myDeck = deck()

            # Test however many times specified
            for testRun in range(maxTests):
                myDeck.shuffle_save(minTakes,maxTakes,3,10,5)
                myDeck.sort()
            # Save the standard deviation of the tested decks
            scores[minTakes-1][maxTakes-1]=myDeck.get_standard_deviation()

    # Print the standard deviation in a way that's easy to import to excel
    for line in scores:
        print(str(line)[1:-1].replace("'",""))

def test_replacements(minReplace, maxReplace, maxTests):
    '''
    Runs the code that checks how changing the replacements affects the efficiency of shuffling
    :param minReplace: Minimum cards we can place at the front
    :param maxReplace: Maximum cards we can place at the front
    :param maxTests: Maximum number of tests we apply
    :return:
    '''

    # Create scores, stores the standard deviation.
    scores = []
    for i in range(52):
        scores.append([''] * 52)

    # Test all values from 1-minReplace
    for minPuts in range(1, minReplace):
        # Used for checking how long the code takes to run
        #print(minPuts)
        # Test all values from minReplace-maxReplace
        for maxPuts in range(minPuts, maxReplace):

            # Create a new deck
            myDeck = deck()

            # Test however many times specified
            for testRun in range(maxTests):
                myDeck.shuffle_save(17, 26, minPuts, maxPuts, 5)
                myDeck.sort()
            # Save the standard deviation of the tested decks
            scores[minPuts - 1][maxPuts - 1] = myDeck.get_standard_deviation()

    # Print the standard deviation in a way that's easy to import to excel
    for line in scores:
        print(str(line)[1:-1].replace("'", ""))

def test_max_shuffles(minTest, maxTest, maxTests):
    '''
    Runs the code that checks how changing the shuffling number affects the efficiency of shuffling
    :param minTest: Minimum number of shuffles we try
    :param maxTest: Maximum number of shuffles we try
    :param maxTests: Maximum number of tests we apply
    :return: None
    '''

    # Create a list to store the standard deviations
    scores = []

    # For every valid number of shuffles we need to try
    for maxShuffles in range(minTest, maxTest):
        # Used to test the time it takes to run the code
        #print(maxShuffles)

        # Create a new deck
        myDeck = deck()
        # For each test we need to run
        for testRun in range(maxTests):
            # Shuffle, save, and sort
            myDeck.shuffle_save(17, 26, 3, 10, maxShuffles)
            myDeck.sort()
        # Store the standard deviation to print later
        scores.append(myDeck.get_standard_deviation())

    # Print all the standard deviations
    print(str(scores)[1:-1])