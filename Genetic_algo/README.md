
# Optimization of Lennard-Jones Parameters for Liquid Argon Using Genetic Algorithms and Machine Learning

## Overview

This project aims to optimize the Lennard-Jones (LJ) potential parameters for molecular dynamics simulations of liquid argon. The optimization is performed using a genetic algorithm implemented in Python, with the simulation backend powered by LAMMPS. By optimizing the epsilon and sigma parameters of the LJ potential, this project seeks to improve the accuracy of molecular simulations in replicating experimental properties such as density, potential energy, and enthalpy.

## Installation

### Prerequisites

- Python 3.x
- LAMMPS (compiled with MPI support)
- pip (Python package installer)


**LAMMPS Setup**
   - Ensure LAMMPS is properly installed and accessible from your command line.
   - Verify that LAMMPS can run the provided `argon.data` file by executing a test run.

## Usage

### Running the Genetic Algorithm

1. **Open the Jupyter Notebook**
   ```bash
   jupyter notebook Genetic_lj_avg.ipynb
   ```

2. **Run the Notebook**
   - Execute the cells step by step.
   - The notebook runs a genetic algorithm to optimize the epsilon and sigma parameters of the LJ potential by minimizing the error between simulated and experimental properties.


### Modifying Parameters

- **Gene Space**: Adjust the `gene_space` dictionary in the notebook to explore different ranges for epsilon and sigma.
- **Experimental Properties**: Update the `experimental_properties` dictionary if you have different target properties for your simulation.

## Example

Below is an example of the output you might get after running the genetic algorithm:

```
Best solution: epsilon = 0.2385, sigma = 3.405
Fitness value of the best solution: -0.001234
```

