__author__ = 'Bennri'

import random
# import math
import pprint
# import numpy as np

# 5 cities for the TSP problem
# e.g. distance from S1 to S2 is 5
cities = {
    "S1": {
        "S2": 5,
        "S3": 6,
        "S4": 5,
        "S5": 10
    },
    "S2": {
        "S1": 5,
        "S3": 3,
        "S4": 7,
        "S5": 6
    },
    "S3": {
        "S2": 3,
        "S1": 6,
        "S4": 3,
        "S5": 4
    },
    "S4": {
        "S1": 5,
        "S2": 7,
        "S3": 3,
        "S5": 8
    },
    "S5": {
        "S1": 10,
        "S2": 6,
        "S3": 3,
        "S4": 8,
    }
}


# how many cities I have to visit
def get_amount_of_cities(dictionary):
    amount = len(dictionary.keys())
    # print "Amount: ", amount
    return amount

# initialise start population
def init_population(dictionary, population_size):
    amount = get_amount_of_cities(dictionary)

    # Because of coincidence, I do not check if there an identical chromosome 2 times in the
    # population, because after a huge amount of iterations they will be either stay in the
    # population because they are the best or sorted out because they are not good enough
    # this is why I am not check population size against the number of possible unique permutations.
    # If you want to do that, you have to had in mind, that the first and the last position has to
    # be identical, which reduces the possible unique permutations and have to be calculated at the beginning
    # if population_size > math.factorial(amount-1):
    #    raise Exception("Size of population higher than possible unique chromosomes")

    population = list()
    while len(population) < population_size:
        tmp_list = list()
        # defining start city, which will be the point to go back to as well:
        s = random.randint(1, amount)
        tmp_list.append(s)
        print "Start: ", s
        # because I have to visit all cities and go back to the first,
        # I need a chromosome of size cities + 1
        while len(tmp_list) < amount:
            k = random.randint(1, amount)
            if k != s and k not in tmp_list:
                tmp_list.append(k)
        tmp_list.append(s)

        if tmp_list not in population:
            population.append(tmp_list)
    # see how the population looks like
    for i in population:
        print i

    return population

# fitness function to evaluate all chromosomes of a population
def fitness_whole_population(dictionary, population):
    population_with_fitness = list()
    for p in population:
        val = int()
        for i in range(len(p)-1):
            c1 = "S" + str(p[i])
            c2 = "S" + str(p[i+1])
            tmp = dictionary[c1][c2]
            val += tmp
            print "Current costs: ", val
        # later I have to choose the greatest chromosomes
        population_with_fitness.append((1.0/val, p))
    print 10*"#" + "Current population:" + 10*"#"
    pprint.pprint(population_with_fitness)
    return population_with_fitness

# fitness function to evaluate one chromosome
def fitness(chrom, dictionary):
    val = int()
    for i in range(len(chrom)-1):
        c1 = "S" + str(chrom[i])
        c2 = "S" + str(chrom[i+1])
        tmp = dictionary[c1][c2]
        val += tmp
        print "Current costs: ", val
    return (1.0/val, chrom)


# selection 2 chromosomes of a population to create 2 new chromosomes
def selection(population):
    print 10*"#" + "Current sorted population:" + 10*"#"
    # because of the normalized values, it have to be reversed sorted
    population = sorted(population, key=lambda x: x[0], reverse=True)
    pprint.pprint(population)

    # to be sure that two different chromosomes will be chosen from the population
    # I will check after each loop if the condition selected_1 != selected_2 is true
    # because if it is true I will return and jump out the loop
    # equal = True

    while True:

        # get an 60 percent probability that a good chromosome will be chosen
        prob1 = random.random()
        prob2 = random.random()
        # if prop1 is greater than 0.4 I choose a chromosome of the first half
        if prob1 > 0.4:
            p1 = random.randint(1, (len(population)/2)-1)
        else:
            # if it is less than 0.4 I will choose a chromosome of the second half of the population
            # which has not the best fitness value
            p1 = random.randint(len(population)/2, len(population)-1)
        selected_1 = population[p1]

        # do that for both parent chromosomes
        if prob2 > 0.4:
            p2 = random.randint(1, (len(population)/2)-1)
        else:
            p2 = random.randint(len(population)/2, len(population)-1)
        selected_2 = population[p2]

        if selected_1 != selected_2:
            # equal = False
            return selected_1[1], selected_2[1]

# crossing the selected chromosomes
def crossing(chrom1, chrom2):
    crossing_point = random.randint(0, len(chrom1)-2)
    print "crossing point: ", crossing_point
    child1 = chrom1[:crossing_point+1]
    child2 = chrom2[:crossing_point+1]
    # I will loop until the second last element, because the last one
    # has to be equal to the first and insert an element from chrom2 in chrom1.
    # child1 and child2 are the two new chromosomes
    for crossing_point in range(len(chrom1)-2):
        for i in chrom2:
            if i not in child1:
                child1.append(i)
                break

    child1.append(chrom1[0])

    for crossing_point in range(len(chrom2)-2):
            for i in chrom1:
                if i not in child2:
                    child2.append(i)
                    break

    child2.append(chrom2[0])

    print "chrom1: ", chrom1
    print "child1: ", child1
    print "chrom2: ", chrom2
    print "child2: ", child2

    return child1, child2

# mutate the two new chromosomes
def mutate(chrom1, chrom2):
    # I want to mutate the chromosomes with a probability of 20 percent
    chrom_size = len(chrom1)

    # prevent getting equal chromosomes
    mutated_chroms_are_equal = True

    while mutated_chroms_are_equal:
        # mutation of the first chromosome
        prob = random.randint(0, 100)

        if prob > 80:
            print "mutate chrom1"
            # Mutation will be done by switching the position of 2 random cities.
            # I do not want to switch e.g city 3 with city 3, so
            # I have to be sure, that both cities are different.
            equal_city = True
            while equal_city:
                # position city 1
                c1 = random.randint(1, chrom_size-2)
                # position city 2
                c2 = random.randint(1, chrom_size-2)
                if c1 != c2:
                    equal_city = False
            tmp_city = chrom1[c1]
            chrom1[c1] = chrom1[c2]
            chrom1[c2] = tmp_city


        # mutation of the second chromosome
        prob = random.randint(0, 100)
        if prob > 80:
            print "mutate chrom2"
            # checking if the cities position is equal
            equal_city = True
            while equal_city:
                # position city 1
                c1 = random.randint(1, chrom_size-2)
                # position city 2
                c2 = random.randint(1, chrom_size-2)
                if c1 != c2:
                    equal_city = False

            tmp_city = chrom2[c1]
            chrom2[c1] = chrom2[c2]
            chrom2[c2] = tmp_city

        # If both chromosomes are equal now, I have to mutate again.
        # If not, I will jump out the loop.
        if chrom1 != chrom2:
            mutated_chroms_are_equal = False

        print "mut1: ", chrom1
        print "mut2: ", chrom2

    return chrom1, chrom2


# start search a solution for the Travelling-Salesman-Problem for the given cities
def main():


    population = init_population(cities, 10)
    fitted_population = fitness_whole_population(cities, population)
    fitted_population.sort(key=lambda x: x[0], reverse=True)

    for i in range(300):
        """ selection """
        sel1, sel2 = selection(fitted_population)
        print "selection 1: ", sel1
        print "selection 2: ", sel2

        """ crossing """
        child1, child2 = crossing(sel1, sel2)
        """ mutation """
        mut1, mut2 = mutate(child1, child2)

        """ fitness for the new chromosomes """
        new_ch1 = fitness(mut1, cities)
        new_ch2 = fitness(mut2, cities)

        """ sorting population """
        # because i am using the normalized values, i have to sort them reversed
        fitted_population.sort(key=lambda x: x[0], reverse=True)

        pprint.pprint(fitted_population)
        """ getting the worst ones """
        bad1 = pprint.pprint(fitted_population[-1])
        print "new_ch1: ", new_ch1

        bad2 = pprint.pprint(fitted_population[-2])
        print "new_ch2: ", new_ch2

        """ checking if the new ones are better """
        if new_ch1 > bad1:
            print "adding new_ch1"
            # fitted_population.remove(bad1)
            del fitted_population[-1]
            fitted_population.append(new_ch1)

        if new_ch2 > bad2:
            print "adding new_ch2"
            # if i append chromosome 1, the second worst chromosome will stay at the second last position in the
            # population, so i can delete this one without getting issues
            del fitted_population[-2]
            # i can append chromosome 2 without thinking about the position of it, because it is the final manipulation
            # at the population gets sorted after appending it
            fitted_population.append(new_ch2)
        """ sort the new population """
        fitted_population.sort(key=lambda x: x[0], reverse=True)


    print 50*"#" + " done " + 50*"#"
    print "best route: ", fitted_population[0]
    n = fitted_population[0][0]
    print "Length: ", (1.0/n)


if __name__ == '__main__':
    main()