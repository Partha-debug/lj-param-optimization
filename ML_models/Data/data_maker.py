import lammps
import pandas as pd
import numpy as np


# Runs The lammps simulation with inputs as epsilon and sigma
def run_simulation(epsilon, sigma):

    # Initialize LAMMPS instance
    lmp = lammps.lammps(cmdargs=["-screen", "none"])

    # Simulation parameters
    P = 0.986923  # atm
    Ti = 100  # K
    out = 10  # timestep
    step = 1  # fs
    runtime = 1000  # steps
    seed = 7545  # unitless
    Tdamp = 10  # timestep
    Pdamp = 100  # timestep

    # Setup commands
    lmp.command("units real")
    lmp.command("boundary p p p")
    lmp.command("atom_style atomic")
    lmp.command("atom_modify map array sort 0 0")

    # Read data file
    data_file = "argon.data"
    lmp.command(f"read_data {data_file}")

    # LJ potential setup for argon
    lmp.command("pair_style lj/cut 10.0")
    lmp.command(f"pair_coeff * * {epsilon} {sigma}")

    # Initialize velocities
    lmp.command(f"velocity all create {Ti} {seed}")

    # Neighbor and timestep settings
    lmp.command("neighbor 2.0 nsq")
    lmp.command("neigh_modify delay 0 every 1 check yes")
    lmp.command(f"timestep {step}")

    # Define thermo output style
    lmp.command(f"thermo {out}")
    lmp.command("thermo_style custom step density pe enthalpy")
    lmp.command("thermo_modify flush yes")

    # Fix for NPT simulation
    lmp.command(f"fix 1 all npt temp {Ti} {Ti} {Tdamp} iso {P} {P} {Pdamp}")

    # Run the simulation and return the properties
    lmp.command(f"run {runtime}")


# Parse The log file and returns The data as a Pandas Dataframe
def parse_log_file(file_path="log.lammps"):

    # As defined in the thermo style
    properties = ["Step", "Density", "PotEng", "Enthalpy"]

    # Read the file and find the start of the thermo data
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Find the header line and the start of data
    header_index = None
    for i, line in enumerate(lines):
        if all(prop in line for prop in properties):
            header_index = i
            break

    if header_index is None:
        raise ValueError(
            "Thermo data header with required properties not found in the log file."
        )

    # Determine the start and end indices of the data section
    footer_start_index = None
    for i in reversed(range(len(lines))):
        if lines[i].startswith("Loop time"):
            footer_start_index = i
            break

    if footer_start_index is None:
        raise ValueError("Footer section marker 'Loop time' not found.")

    # Read the thermo data lines into a list, excluding the footer lines
    thermo_data_lines = lines[header_index + 1 : footer_start_index]

    # Create a DataFrame from the thermo data lines
    data = pd.DataFrame(
        [line.split() for line in thermo_data_lines], columns=properties
    )
    data = data.dropna()
    data[properties] = data[properties].apply(pd.to_numeric, errors="coerce")

    return data


# Calculate averages of defined properties over the bottom provided percentage data


def bottom_average(data, percentage=30):

    # can be a subset of the properties as defined in thermo style
    properties = ["Density", "PotEng", "Enthalpy"]

    # Calculate the start index for the last `percentage`% of the data
    start_index = int(
        (100 - percentage) / 100 * len(data)
    )  # Convert percentage to start index

    # Select the last `percentage`% of the data
    last_percentage_data = data.iloc[start_index:]

    # Calculate averages for the last `percentage`% of the data
    averages = {prop: last_percentage_data[prop].mean() for prop in properties}

    return averages


# Calculate Average simulation properties as a function of epsilon and sigma


def calculate_properties(epsilon, sigma):

    run_simulation(epsilon, sigma)

    file_path = "log.lammps"

    data = parse_log_file(file_path)

    averages = bottom_average(data, percentage=35)

    # Append epsilon and sigma to averages dictionary
    averages["Epsilon"] = epsilon
    averages["Sigma"] = sigma

    return averages


epsilon_range = np.arange(1.535, 2.00, 0.001)  # Original start 0.1
sigma_range = np.arange(2.00, 4.00, 0.02)


# Initialize iteration counters and timing
import time
import os

# from IPython.display import clear_output

total_iterations = len(epsilon_range) * len(sigma_range)
iter = 0
start_time = time.time()
results = []
writes = 0
chunk_size = 500

# Iterate over epsilon and sigma ranges
for epsilon in epsilon_range:
    for sigma in sigma_range:
        # Calculate properties for current epsilon and sigma
        properties = calculate_properties(epsilon, sigma)
        # Append to results list
        results.append(properties)

        # Update iteration counter
        iter += 1
        rem_iter = total_iterations - iter

        # Calculate elapsed time and estimated remaining time
        elapsed_time = time.time() - start_time
        avg_time_per_iter = elapsed_time / (total_iterations - rem_iter)
        est_time_remaining = avg_time_per_iter * rem_iter
        est_time_remaining_minutes = est_time_remaining / 60

        # Display progress
        # clear_output()
        os.system("cls")
        print(f"Iterations: {iter}/{total_iterations}")
        print(
            f"ETA: {est_time_remaining_minutes:.2f} mins = {est_time_remaining_minutes/60:.2f} hrs = {est_time_remaining_minutes/(24*60):.1f} Days"
        )
        print(f"Completed writes: {writes}/{(total_iterations//chunk_size)}")

    # Convert the results list to a DataFrame and append to the CSV file
    if len(results) > chunk_size or epsilon == epsilon_range[-1]:
        df = pd.DataFrame(results)
        results = []
        df.to_csv("simulation_results.csv", index=False, header=False, mode="a")
        writes += 1

print("CSV export complete.")
