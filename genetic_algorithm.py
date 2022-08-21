################################################################
# Date: 17 Aug 2022
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
import random
from typing import List
from colorama import Fore, Back, Style

N_QUEEN_CONST = 8
MUTATION_PROBABILITY_CONST = 10
CELL = '   '
QUEEN = '♛'


class CONST:
    WHITE_CELL = f'{Back.WHITE}{CELL}{Style.RESET_ALL}'
    BLACK_CELL = f'{Back.BLACK}{CELL}{Style.RESET_ALL}'
    WHITE_QUEEN = f'{Back.WHITE} {Fore.RED}{QUEEN} {Style.RESET_ALL}'
    BLACK_QUEEN = f'{Back.BLACK} {Fore.LIGHTRED_EX}{QUEEN} {Style.RESET_ALL}'


class Gen:

    def __init__(self, gen: List[int], generation: int = 0) -> None:
        """
        Gen: [0,1,2,3,4,5,6,7]
        where position is the row and value is the column
        for example:
            [0,1,2,4,3,5,6,7]
            first queen is in row 0 and column 0
            second queen is in row 1 and column 1
            third queen is in row 2 and column 2
            fourth queen is in row 3 and column 4
            fifth queen is in row 4 and column 3
            ...
        """
        self.gen = gen
        self.generation = generation
        self.fitness = self._calculate_fitness()


    def _calculate_fitness(self) -> int:
        """
        Calculate fitness of the gen
        """
        
        fitness = 0
        gen = self.gen
        for q_row, q_column in enumerate(gen):
            for q_row2, q_column2 in enumerate(gen[q_row + 1:], start=q_row + 1):
                row_diff = abs(q_row - q_row2)
                col_diff = abs(q_column - q_column2)
                if row_diff == col_diff:
                    # diagonal conflict
                    fitness += 1

                # same column [1,0, 1] row 0 and row 2 have same column
                elif q_column == q_column2:
                    # same row conflict
                    fitness += 1

                else:
                    # no conflict
                    fitness += 2

        return fitness


class GeneticAlgorithm:

    n_queen: int = 0
    population: List[Gen] = []
    mutation_probability: int = 0
    best_fitness: int = 0
    current_generation: int = 0

    def __init__(self, initial_population_number: int, n_queen: int,
                 mutation_probability: int) -> None:

        self.n_queen = n_queen
        self.population = self._create_initial_population(initial_population_number)
        self.mutation_probability = mutation_probability
        self.best_fitness = n_queen * (n_queen - 1)  # sum of fitness function


    def _create_initial_population(self, initial_population_number: int) -> List[Gen]:
        """
        Create initial population
        """
        n_queen = self.n_queen
        gen_list = [
            Gen(gen=[random.randint(0, n_queen - 1)
                for _ in range(n_queen)], generation=0)
            for _ in range(initial_population_number)
        ]

        return gen_list


    @property
    def best_gen(self) -> Gen:
        """
        Get best gen
        """
        gen = max(self.population, key=lambda x: x.fitness)
        return gen


    def _crossover(self, gen_1: Gen, gen_2: Gen) -> Gen:
        """
        index = random.randint(0, self.n_queen - 1) => 3 random crossover 
        gen1: [3,4,2,1,0,5,6,7]
        gen2: [4,3,2,7,1,3,5,7]
        new_gen: gen1[0:3] + gen2[3:n_queen - 1] = [3,4,2,7,1,3,5,7]

        ## mutation
        gen = [3,4,2,7,1,3,6,7]
        mutated_gen = [3,*1,2,7,1,3,*5,7] ## * is a placeholder for mutation
        """
        n_queen = self.n_queen
        index = random.randint(0, n_queen - 1)
        gen_solution = gen_1.gen[0:index] + gen_2.gen[index:]
        

        # mutation: value of new_gen
        mutation_probability = self.mutation_probability
        for i in range(n_queen):
            if random.randint(0, 100) < mutation_probability:
                gen_solution[i] = random.randint(0, n_queen - 1)
                
        new_gen = Gen(gen=gen_solution, generation=self.current_generation)
        
        return new_gen


    def _create_generation(self) -> None:
        """
        Create new generation
        """
        self.current_generation += 1
        new_population: List[Gen] = []
        population = self.population  # copy of population optimization
        # we want to position 0 to length - 1
        length_population = len(population) - 1

        for _ in range(length_population):
            # Gen selection 1 (tournament selection)
            gen_1 = population[random.randint(0, length_population)]
            gen_2 = population[random.randint(0, length_population)]
            selected_gen_1 = gen_1 if gen_1.fitness < gen_2.fitness else gen_2

            # Gen selection 2 (tournament selection)
            gen_1 = population[random.randint(0, length_population)]
            gen_2 = population[random.randint(0, length_population)]
            selected_gen_2 = gen_1 if gen_1.fitness < gen_2.fitness else gen_2

            ## crossover and mutation
            new_gen = self._crossover(selected_gen_1, selected_gen_2)
            new_population.append(new_gen)

        new_population.append(self.best_gen)

        self.population = new_population


    def solve(self, generation_number) -> int:
        """
        Return number of generations needed to solve the problem
        if no solution found return -1
        """

        solved_generation = 0
        best_fitness = self.best_fitness
        if self.best_gen.fitness == best_fitness:
            generation = solved_generation

        else:
            for k in range(generation_number):
                self._create_generation()

                if self.best_gen.fitness == best_fitness:
                    generation = k + 1
                    break
                  
            generation = -1

        return generation


    def _create_chessboard(self) -> str:
        """
        Create chessboard
        This is for printing purpose, not for solving the problem hahaha for this 
        reason I did it this way, complicated but it works
        """
        PUT_QUEEN = 1
        NOT_PUT_QUEEN = 0
        line = '+---' * self.n_queen + '+'
        board = [[PUT_QUEEN if queen_pos == _ else NOT_PUT_QUEEN for _ in range(self.n_queen)]
                 for queen_pos in self.best_gen.gen]
        chessboard = ''
        chessboard += f'{line}\n'

        cell_color = lambda i, j:  f'{CONST.BLACK_CELL}' if (i + j) % 2 else f'{CONST.WHITE_CELL}'
        queen_color = lambda i, j:  f'{CONST.BLACK_QUEEN}' if (i + j) % 2 else f'{CONST.WHITE_QUEEN}'
        
        for i, row in enumerate(board):
            chessboard += '|' + '|'.join('{}'.format(
                queen_color(i, j) if col == PUT_QUEEN else cell_color(i, j)
            ) for j, col in enumerate(row)
            ) + '|\n'
            chessboard += f'{line}\n'

        return chessboard


    def __repr__(self) -> str:

        representation = ""
        representation += "Best gen: {}\n".format(self.best_gen.gen)
        representation += "Best fitness gen: {}/{}\n".format(self.best_gen.fitness, self.best_fitness)
        representation += "Best Gen Generation: {}\n".format(self.best_gen.generation)
        representation += "Generation: {}\n".format(self.current_generation)
        representation += "\n"
        representation += self._create_chessboard()

        return representation
