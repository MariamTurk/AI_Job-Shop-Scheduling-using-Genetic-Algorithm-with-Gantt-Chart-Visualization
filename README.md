# Job Shop Scheduling using Genetic Algorithm with Gantt Chart Visualization

This project implements a Genetic Algorithm (GA) to solve the **Job Shop Scheduling Problem (JSSP)**. It optimizes the schedule of jobs across multiple machines to minimize the total completion time (makespan), and visualizes the final job schedule using a Gantt chart.

## 👥 Authors
- Mariam Turk  
- Shahd Loai 

## 🚀 Features
- Takes dynamic input for any number of jobs and machines
- Simulates operations with specific machine assignments and durations
- Uses a Genetic Algorithm to evolve optimal scheduling solutions
- Visualizes the final optimized schedule using a Gantt chart with `matplotlib`

## 📌 Problem Description
Each job consists of a sequence of operations that must be performed in a specific order on different machines. The goal is to schedule all jobs while:
- Respecting operation sequences
- Ensuring no two operations overlap on the same machine
- Minimizing the **total completion time (makespan)**

## 🔬 Genetic Algorithm Details
- **Population Size**: 100
- **Generations**: 100
- **Crossover Rate**: 0.8
- **Mutation Rate**: 0.1
- **Selection**: Fitness-proportional (roulette wheel)

## 🛠️ How It Works
1. The user inputs job names, the number of operations per job, and operation details (machine number and time).
2. The algorithm initializes a random population of job schedules.
3. It evolves the population using:
   - **Selection**: Chooses parents based on fitness
   - **Crossover**: Combines parent chromosomes
   - **Mutation**: Swaps random genes
4. The best chromosome (schedule) is decoded into a readable format and visualized.

## 📊 Visualization

The final schedule is displayed using a Gantt chart:
- Each bar represents an operation on a machine
- Different colors indicate different machines
- The X-axis represents time, Y-axis represents machines

## 🧪 Sample Input Format
Number of Jobs: 2
Number of Machines: 3

Job 1 Name: A
Number of Operations: 2
Machine 1: 1
Time: 5
Machine 2: 2
Time: 3

Job 2 Name: B
Number of Operations: 2
Machine 1: 2
Time: 4
Machine 2: 3
Time: 2
