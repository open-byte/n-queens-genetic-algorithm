################################################################
# Date: 20 Aug 2022
# Author: Izcar J. Muñoz Torrez
# --------------------------------------------------------------
#   ____                     ____        _
#  / __ \                   |  _ \      | |
# | |  | |_ __   ___ _ __   | |_) |_   _| |_ ___
# | |  | | '_ \ / _ \ '_ \  |  _ <| | | | __/ _ \
# | |__| | |_) |  __/ | | | | |_) | |_| | ||  __/
#  \____/| .__/ \___|_| |_| |____/ \__, |\__\___|
#        | |                        __/ |
#        |_|                       |___/
# --------------------------------------------------------------
################################################################

from genetic_algorithm import MUTATION_PROBABILITY_CONST, N_QUEEN_CONST, GeneticAlgorithm
import argparse
from datetime import datetime
from utils import brand, formatter_side_by_side

INITIAL_POPULATION_CONST = 100
GENERATIONS_CONST = 100

def main():
    parser = argparse.ArgumentParser(description='Genetic Algorithm')
    parser.add_argument('-n', '--n-queen', type=int, default=N_QUEEN_CONST,
                        help='Number of queens')
    parser.add_argument('-p', '--population', type=int, default=INITIAL_POPULATION_CONST,
                        help='Population size')
    parser.add_argument('-m', '--mutation-probability', type=int, default=MUTATION_PROBABILITY_CONST,
                        help='Mutation probability')
    parser.add_argument('-g', '--generations', type=int, default=GENERATIONS_CONST,
                        help='Number of generations')
    args = parser.parse_args()
    
    n_queen = GeneticAlgorithm(args.population, args.n_queen, args.mutation_probability)

    ## start time 
    try:
        start_time = datetime.now()
        
        n_queen.solve(args.generations)
        
    except KeyboardInterrupt:
        
        print("\nInterrupted", end="\n")
    finally:
        
        end_time = datetime.now()
        
        duration = 'Duration: {}'.format(end_time - start_time)
        
        text = f'{duration}\n{n_queen}'

        text = formatter_side_by_side(brand, text)

        print(text)


if '__main__':
    
    main()
