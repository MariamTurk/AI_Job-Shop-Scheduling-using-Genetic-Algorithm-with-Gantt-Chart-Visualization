# Mariam turk     shahd loai
# 1211115         1211019
# section : 1
# instructor : Dr . Yazan Abu Farha

#to get the jobs randomly
import random
# to get the gantt chart for job schedule
import matplotlib.pyplot as plt

# define class
# this class to get the machines and the time for reach machine
class Operation:
    def __init__(self, machine, Time):
        self.machine = machine
        self.Time = Time

# class job to get the JobName and operations for each job in the factory
class Job:
    def __init__(self, JobName, operations):
        self.JobName = JobName
        self.operations = operations

# Define Schedule class
class Schedule:
    def __init__(self, NumOfMachines, jobs):
        # number of machines for each job
        self.NumOfMachines = NumOfMachines
        # the job in the system
        self.jobs = jobs
        # the chromosome_length is number of operations for each job
        self.chromosome_length = sum(len(job.operations) for job in jobs)
        # GA will take 100 jobs at the same time to do the algorithm on this 100 jobs
        self.population_size = 100
        # the algorithm will do 100 generations (run 100 times)
        self.generations = 100
        # probability of crossover two parent schedules
        self.crossover_rate = 0.8
        # probability of mutation two parent schedules
        self.mutation_rate = 0.1
        # initializes the population
        self.population = self.generate_initial_population()

    def generate_initial_population(self):
        # array for the initial population of chromosomes.
        population = []
        #
        for _ in range(self.population_size):
            # array for chromosome
            chromosome = []
            for job in self.jobs:
                # to create tuples that have the JobName of the job and the position for each operation for this job and put these operations in the chromosome array
                chromosome.extend([(job.JobName, i) for i in range(len(job.operations))])
            # take operations for each chromosome randomly
            random.shuffle(chromosome)
            # to add the chromosome in the population array
            population.append(chromosome)
        # return the population with all generation chromosomes
        return population

    # the fitness function calculates the total time for each job to end
    def fitness(self, chromosome):
        # this for end time for each job scheduled on each machine
        EndOfTimeMachine = {i: 0 for i in range(self.NumOfMachines)}
        # this for time of the last operation for each job
        EndOfTimeJob = {job.JobName: 0 for job in self.jobs}
        # this for total time for all jobs
        TotalTime = 0

        for job_JobName, operation_index in chromosome:
            operation = self.jobs_by_JobName[job_JobName].operations[operation_index]
            machine, duration = operation.machine, operation.Time
            # this to take the start time for current operation
            begin_time = max(EndOfTimeMachine[machine], EndOfTimeJob[job_JobName])
            finish_time = begin_time + duration
            # to update the end time for the machine
            EndOfTimeMachine[machine] = finish_time
            # to update the end time for the job that its operation schedule
            EndOfTimeJob[job_JobName] = finish_time

            TotalTime = max(TotalTime, finish_time)
        # it returns the fitness of the chromosome
        return 1 / TotalTime

    # select random chromosome from population
    def selection(self):
        selected = random.choices(
            # select two random elements from population
            self.population,
            # probability of each element to be selected based on the fitness of chromosome
            weights=[self.fitness(chromo) for chromo in self.population],
            # to select 2 elements from population
            k=2
        )
        return selected

    def crossover(self, P1, P2):
        # if the random generation is greater than crossover rate, just return P1 and P2
        if random.random() > self.crossover_rate:
            return P1, P2
        # represent the positions where the chromosomes will be cut during the crossover operation
        cut1 = random.randint(0, self.chromosome_length - 1)
        cut2 = random.randint(0, self.chromosome_length - 1)
        # swaps the values of cut1 and cut2
        if cut1 > cut2:
            cut1, cut2 = cut2, cut1

        def CreateChild(p1, p2):
            # this to get part from beginning to the p1[cut1] and put it with the part from p2 that does not have the part that has been cut in p1
            child = p1[:cut1] + [gene for gene in p2 if gene not in p1[:cut1]]
            # it takes the part 2 from p1 cut1 to the end of p1 but only if those genes are not already present in the child list.
            child.extend(gene for gene in p1[cut1:] if gene not in child)
            return self.fix_chromosome(child)

        # to make new children to generate them
        child1 = CreateChild(P1, P2)
        child2 = CreateChild(P2, P1)

        return child1, child2

    # this function is to take a chromosome and fix it by ensuring that each job has a unique operation index
    def fix_chromosome(self, chromosome):
        job_operation_counts = {job.JobName: 0 for job in self.jobs}
        fixed_chromosome = []
        for job_JobName, operation_index in chromosome:
            # make tuple in the fixed_chromosome that have the job JobName and the current count of operations
            fixed_chromosome.append((job_JobName, job_operation_counts[job_JobName]))
            job_operation_counts[job_JobName] += 1
        return fixed_chromosome

        #mutate function selects two positions in the chromosome list and swaps their values
    def mutate(self, chromosome):
        if random.random() < self.mutation_rate:
            index1, index2 = random.sample(range(len(chromosome)), 2)
            # swaps the values at the two randomly selected indices in the chromosome list
            chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
            #to knoe if the chromsom is valid or not
            chromosome = self.fix_chromosome(chromosome)
        return chromosome


        #NewGeneration function to generate the next generation of a population
    def NewGeneration(self):
        # array for the new genaration
        NewPop = []
        # loop that runs to create a new generation of the same size
        for _ in range(self.population_size // 2):
            P1, P2 = self.selection()
            #two new child by crossing over the genetic information
            child1, child2 = self.crossover(P1, P2)
            # add the mutated children to the new population
            NewPop.extend([self.mutate(child1), self.mutate(child2)])
        #replacing the current population with the new population
        self.population = NewPop
     # function to genartion and
    def run(self):
        #maps job JobNames to job objects
        self.jobs_by_JobName = {job.JobName: job for job in self.jobs}
        for generation in range(self.generations):
            print(f"Generation {generation + 1}")
            self.NewGeneration()
            # to find chromsom that have highst fitness function
        fittest_individual = max(self.population, key=self.fitness)
        return self.decode_chromosome(fittest_individual), 1 / self.fitness(fittest_individual)
    # function to retur the jobes with it start time and end time of there machiens acording to the sqance that the user enter it
    def decode_chromosome(self, chromosome):
        # initial eash of the three varibles
        decoded_schedule = []
        EndOfTimeMachine = {i: 0 for i in range(self.NumOfMachines)}
        EndOfTimeJob = {job.JobName: 0 for job in self.jobs}
        for job_JobName, operation_index in chromosome:
            # return the object by job JobName and operations
            operation = self.jobs_by_JobName[job_JobName].operations[operation_index]
            # the machine number and the time of the machine
            machine, duration = operation.machine, operation.Time
            #the start time for the operation, when the machine is available and when the previous operation of the same job is finish
            begin_time = max(EndOfTimeMachine[machine], EndOfTimeJob[job_JobName])
            finish_time = begin_time + duration
            EndOfTimeMachine[machine] = finish_time
            EndOfTimeJob[job_JobName] = finish_time
            #addtuple to the decoded schedule array ( the job JobName, machine number, start time, and end time of the machine)
            decoded_schedule.append((job_JobName, machine, begin_time, finish_time))
        return decoded_schedule

# Function to get user input
def get_user_input():
    num_jobs = int(input("welcome, please enter the number of jobs: "))
    NumOfMachines = int(input("sorry for annoying, please enter the number of machines:"))

    jobs = []
    for i in range(num_jobs):
        job_JobName = input(f"please enter the JobName of job {i + 1}: ")
        NumofOperations = int(input(f"please enter the number of operations for job {i + 1}: "))
        operations = []
        for j in range(NumofOperations):
            machine = int(input(f"please enter the machine number for operation {j + 1} of job {i + 1}: ")) - 1
            Time = int(input(f"please enter the Time for operation {j + 1} of job {i + 1}: "))
            operations.append(Operation(machine, Time))
        jobs.append(Job(job_JobName, operations))

    return jobs, NumOfMachines

# Function to plot the Gantt chart
def plot_gantt(schedule):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title("Job Schedule Gantt Chart")
    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")

    machine_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    for job_JobName, machine, begin_time, finish_time in schedule:
        machine_index = machine
        ax.barh(machine_index, finish_time - begin_time, left=begin_time, height=0.8, color=machine_colors[machine_index % len(machine_colors)], edgecolor='black')
        ax.text(begin_time + (finish_time - begin_time) / 2, machine_index, job_JobName, va='center', ha='center')

    ax.set_yticks(range(len(set(machine for _, machine, _, _ in schedule))))
    ax.set_yticklabels([f'M{i+1}' for i in range(len(set(machine for _, machine, _, _ in schedule)))])
    ax.set_xlim(0, max(finish_time for _, _, _, finish_time in schedule))
    ax.grid(True)
    plt.show()

# Define main function to integrate genetic algorithm with job scheduling
def main():
    jobs, NumOfMachines = get_user_input()
    schedule = Schedule(NumOfMachines, jobs)
    decoded_schedule, TotalTime = schedule.run()
    print(f"Total completion time: {TotalTime}")
    plot_gantt(decoded_schedule)

if __name__ == "__main__":
    main()
