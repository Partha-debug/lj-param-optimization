# Lennard-Jones Parameter Optimization for Liquid Argon Simulations

This project focuses on optimizing Lennard-Jones parameters for liquid argon simulations using genetic algorithms and machine learning techniques.

## Project Structure

```
lj-param-optimization/
├── Genetic_algo/
│   ├── argon.data
│   ├── Genetic_lj_avg.ipynb
│   └── README.md
└── ML_models/
    ├── deep_learn.ipynb
    ├── GBM.ipynb
    ├── rf.ipynb
    ├── Data/
    │   ├── argon.data
    │   ├── data_maker.py
    │   ├── log.lammps
    │   └── simulation_results.csv
    └── Models/
        └── README.md
```

## Project Components

### Genetic Algorithm

The `Genetic_algo` directory contains:
- `argon.data`: Data file for argon simulations
- `Genetic_lj_avg.ipynb`: Jupyter notebook implementing the genetic algorithm for parameter optimization
- `README.md`: Detailed information about the genetic algorithm approach

### Machine Learning Models

The `ML_models` directory includes:
- `deep_learn.ipynb`: Deep learning model implementation
- `GBM.ipynb`: Gradient Boosting Machine model implementation
- `rf.ipynb`: Random Forest model implementation

#### Data

The `Data` subdirectory contains:
- `argon.data`: Input data for argon simulations
- `data_maker.py`: Script for generating simulation data
- `log.lammps`: LAMMPS simulation log file
- `simulation_results.csv`: Compiled results from simulations

