################################################################							
# Date: 17 Aug 2022                                                                                 
# Author: Izcar J. Muñoz Torrez		                                                                
#---------------------------------------------------------------     
#   ____                     ____        _                                                          
#  / __ \                   |  _ \      | |                                                         
# | |  | |_ __   ___ _ __   | |_) |_   _| |_ ___                                                    
# | |  | | '_ \ / _ \ '_ \  |  _ <| | | | __/ _ \                                                   
# | |__| | |_) |  __/ | | | | |_) | |_| | ||  __/                                                   
#  \____/| .__/ \___|_| |_| |____/ \__, |\__\___|                                                   
#        | |                        __/ |                                                           
#        |_|                       |___/                                                                           
#---------------------------------------------------------------										
################################################################ 

import random
from typing import List
from colorama import Fore, Back, Style

N_QUEEN_CONST = 8
MUTATION_PROBABILITY_CONST = 10
CELL = '   '
QUEEN = '●'
class CONST:
    WHITE_CELL = f'{Back.WHITE}{CELL}{Style.RESET_ALL}'
    BLACK_CELL = f'{Back.BLACK}{CELL}{Style.RESET_ALL}'
    WHITE_QUEEN = f'{Back.WHITE} {Fore.LIGHTRED_EX}{QUEEN} {Style.RESET_ALL}'
    BLACK_QUEEN = f'{Back.BLACK} {Fore.LIGHTRED_EX}{QUEEN} {Style.RESET_ALL}'

class Gen:
    
    def __init__(self, gen: List[int]) -> None:
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


    @property
    def fitness(self) -> int:
        
        fitness = 0
        for q_row, q_column in enumerate(self.gen):
            for q_row2, q_column2 in enumerate(self.gen[q_row + 1:], start=q_row + 1):
                row_diff = abs(q_row - q_row2)
                col_diff = abs(q_column - q_column2)
                if row_diff == col_diff:
                    # diagonal conflict
                    fitness += 1
                
                elif q_column == q_column2: # same column [1,0, 1] row 0 and row 2 have same column
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
    
    
    def __init__(self, initial_population_number: int, n_queen: int = N_QUEEN_CONST ,
                 mutation_probability: int = MUTATION_PROBABILITY_CONST) -> None:
        
        self.n_queen = n_queen
        self.population = self._create_initial_population(initial_population_number)
        self.mutation_probability = mutation_probability
        self.best_fitness = n_queen * (n_queen - 1) ## sum of fitness function


    def _create_initial_population(self, initial_population_number: int) -> List[Gen]:
        """
        Create initial population
        """
        gen_list = [
            Gen(gen = [random.randint(0, self.n_queen - 1) for _ in range(self.n_queen)]) 
            for _ in range(initial_population_number)
        ]
        
        return gen_list


    @property
    def best_gen(self) -> Gen:
        """
        Get best gen
        """
        best_gen = self.population[0]
        
        for gen in self.population[1:]:
            if best_gen.fitness < gen.fitness:
                best_gen = gen
                
                if best_gen.fitness == self.best_fitness:
                    break
        
        return best_gen

    
    def _gen_selection(self) -> Gen:
        """
        Select gen for crossover
        minimum elitism(best fitness between two random gens)
        """
        
        gen_1 = self.population[random.randint(0, len(self.population) - 1)]
        gen_2 = self.population[random.randint(0, len(self.population) - 1)]

        selected_gen = gen_1 if gen_1.fitness < gen_2.fitness else gen_2
        
        return selected_gen
    
    
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
        index = random.randint(0, self.n_queen - 1) 
        new_gen = Gen(gen = gen_1.gen[0:index] + gen_2.gen[index:self.n_queen])
        
        ## mutation: value of new_gen
        for i in range(self.n_queen):
            if random.randint(0, 100) < self.mutation_probability:
                new_gen.gen[i] = random.randint(0, self.n_queen - 1)
        
        return new_gen
        
        
    def _create_generation(self) -> None:
        """
        Create new generation
        """
        new_population: List[Gen] = []
        
        for _ in range(len(self.population)):
            gen_1 = self._gen_selection()
            gen_2 = self._gen_selection()
            
            ## crossover and mutation
            new_gen = self._crossover(gen_1, gen_2)
            new_population.append(new_gen)
        
        self.population = new_population
    
    
    def _create_chessboard(self) -> str:
        """
        Create chessboard
        This is for printing purpose, not for solving the problem hahaha for this 
        reason I did it this way, complicated but it works
        """
        PUT_QUEEN = 1
        NOT_PUT_QUEEN = 0
        line = '+---' * self.n_queen + '+'
        board = [ [ PUT_QUEEN if queen_pos == _ else NOT_PUT_QUEEN for _ in range(self.n_queen) ] 
                    for queen_pos in self.best_gen.gen ]
        chessboard = ''
        chessboard += f'\t{line}\n'
        cell_color = lambda i, j: f'{CONST.BLACK_CELL}' if (i + j) % 2 else f'{CONST.WHITE_CELL}'
        queen_color = lambda i, j: f'{CONST.BLACK_QUEEN}' if (i + j) % 2 else f'{CONST.WHITE_QUEEN}'                                
        for i, row in enumerate(board):
            chessboard += '\t|' + '|'.join('{}'.format(
                                            queen_color(i, j) if col == PUT_QUEEN else cell_color(i, j)
                                            ) for j, col in enumerate(row)
                                        ) + '|\n'
            chessboard += f'\t{line}\n'

        return chessboard
    
    
    def __repr__(self) -> str:
        
        representation = ""
        representation += "Best gen: {}\n".format(self.best_gen.gen)
        representation += "Best fitness gen: {}/{}\n".format(self.best_gen.fitness, self.best_fitness)
        representation += "\n\n"
        
        representation += self._create_chessboard()

        return representation
    

if '__main__':
    
    t = GeneticAlgorithm(initial_population_number = 10000)
    print(t)
