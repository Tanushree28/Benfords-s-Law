import csv
import math
import random

# for type hint and documentation
from collections.abc import Sequence

# Ideal Benford data/percentage
# Calculate using
# p(d) = log10(1 + 1/d)
BRENFORD_EXPECTED_PERCENTAGES = {
        "1": 0.301, 
        "2": 0.176, 
        "3": 0.125, 
        "4": 0.097, 
        "5": 0.079, 
        "6": 0.067, 
        "7": 0.058, 
        "8": 0.051, 
        "9": 0.046
}


def readfile(filename: str) -> list:
    """
    Description: - read the path to the file in server and read csv file
                 - convert the columns into list if the row is of numerical type

    args: filename (str) - path name directing to the csv file

    return: list_of_number (list) - convert the column into list and returned it
    """

    # conversion of csv file column to list 
    # Closure Implementation
    def conversion_to_list(file:str) -> list:
        return [row[0] for row in reader if row[0].isdigit()]
    
    # Reading the csv file
    with open(filename, 'r') as file:
        reader = csv.reader(file)

        return conversion_to_list(reader)


def calculate_brenford_values(data: list) -> Sequence[list[dict]]:
    """
    Description: - Brenford describes the probability of occurence of number with respective first digit
                 - Ideal data store in variable BRENFORD_EXPECTED_PERCENTAGES
                 - This function calcuates the occurance/percentage of numbers with respective first digit

    args: data (list) - list of number converted from csv file

    return: result (list(dict)) - result of every possible first digti is store as a dictionary
                                - returns the collection of dictionary
    """
    
    # To store result
    result = []

    # Converting to the multi charater digit into single digit (first digit)
    def first_digit_frequency(digits_list: list) -> Sequence[tuple[dict, int]]:
        """
        Description: -Counts the occurance/frequency of first digit

        """
        digits_count = {}
        total_count = 0
        for digit in digits_list:
            if digit == "0":
                continue
            else:
                if digit in digits_count.keys():
                    digits_count[digit] += 1
                else:
                    digits_count[digit] = 1
                total_count += 1
        
        return digits_count, total_count
    
    # conversion of multi character digit into single character (first digit)
    # Use of High Order function - map
    # map needs function as an argument, so, it is called higher order function
    # map takes 2 argument - first one is function and second is array/list
    # lambda function, also called anonymous function (function without a name) 
    list_of_first_digit = sorted(list(map(lambda n: str(n)[0], data)))

    # Determining the frequency
    frequencies_of_first_digit, total_count = first_digit_frequency(list_of_first_digit)

    # Calculate in percantage
    def calculate_percentage(count:int, total:int) -> int:
        return count/total
    
    # calculate expectetd frequency
    def calculate_expected_values(digit:int, total_count:int) -> int:
        return BRENFORD_EXPECTED_PERCENTAGES[str(digit)], BRENFORD_EXPECTED_PERCENTAGES[str(digit)] * total_count
    
    # Possible digit is from 1 to 9. So, looping only from  1 to 9
    for num in range(1, 10):
        observed_frequency = frequencies_of_first_digit[str(num)]

        # Use of functional programming - f(g(x))
        observed_percentage = calculate_percentage(observed_frequency, total_count)

        expected_percentage, expected_frequency = calculate_expected_values(num, total_count)
        
        # storing each result in list
        result.append({
            "digit": num,
            "expected_frequency": expected_frequency,
            "expected_percentage": expected_percentage,
            "observed_frequency": observed_frequency,
            "observed_percentage": observed_percentage
        })

    return result


def test_brenford(distribution: Sequence[list[dict]]) -> bool:
    """
    Description: - chi-square test can be used to test whether the distribution follows Brenford Law or not
                 - chi-square test hypothesize;
                    H0: observed and theoretical distribution are the same (using level of significane 5%)
                 - calculated using;
                    chi_square_stat = ((observed_frequency - expected_frequency)^2)/expected_frequency
                 - if the value < 15.51, the Brenford Law holds true, else false
    
    args: distribution (list(dict)) - list of dictionary; each dictionary holding the data of each digit

    return: condition (bool) - if the sum is less tha 15.51, null hypothesis holds true and proves Brenford Law

    """
    chi_square_stat = 0
    for digit in distribution:
        chi_square = math.pow((digit["observed_frequency"] - digit["expected_frequency"]), 2)
        chi_square_stat += chi_square

    return chi_square < 15.51


def check_brenford(file: str, random_dist: bool=False) -> Sequence[tuple[bool, Sequence[list[dict]]]]:
    """
    Desciption: - main function to connect the different function
                - first read the csv file or create random distribution
                - then calculates requierd Brenford values
                - lastly, does chi-square test

    args: file (str) - csv filename to be read located in server
          random_dist (bool) - whether to create random distribution or not

    return: tuple(bool, list(dict)) - first element of tuple is the bool which gives whether the distribution \
                                        follows Brenford law or not
                                    - second element of tuple gives the resulted data if Brendford law hold true \
                                        else return none
    """
    if random_dist:
        # Randomly generated list
        data_list = [random.randint(1, 1000) for i in range(10000)]
    else:
        # Reading csv file
        data_list = readfile(file)
    
    # Calculating required Brenford values
    result = calculate_brenford_values(data_list)

    # Checking whether the Brenford law holds true of not and returning with respective decisions
    if test_brenford(result):
        return test_brenford(result), result
    return test_brenford(result), None