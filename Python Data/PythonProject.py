import pandas as pd
import glob
import matplotlib.pyplot as plt
import os


# Define the folder containing the CSV files
folder_path = '/Users/farimah/PycharmProjects/pythonassessment2/2015-2024data'

# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Define columns to be renamed
columns_to_rename = {
    'Eng Displ': 'Engine Displacement',
    '# Cyl': '# Cylinders',
    'City FE (Guide) - Conventional Fuel': 'City FE',
    'Hwy FE (Guide) - Conventional Fuel': 'Highway FE',
    'Comb FE (Guide) - Conventional Fuel': 'Combined FE',
    'Air Aspiration Method Desc': 'Air Aspiration Method',
    'Trans Desc': 'Transmission Description',
    'City CO2 Rounded Adjusted': 'City CO2',
    'Hwy CO2 Rounded Adjusted': 'Highway CO2',
    'Comb CO2 Rounded Adjusted (as shown on FE Label)': 'Combined CO2'
}

# Columns to retain
columns_to_retain = [
    'Model Year', 'Mfr Name', 'Division', 'Carline', 'Engine Displacement', '# Cylinders', 'Transmission',
    'City FE', 'Highway FE', 'Combined FE', 'Air Aspiration Method', 'Transmission Description', '# Gears',
    'Drive Desc', 'Carline Class Desc', 'Release Date', 'City CO2', 'Highway CO2', 'Combined CO2'
]

# Initialize an empty list to hold individual DataFrames
dfs = []

# Loop through each CSV file, rename columns, retain specified columns, and append cleaned DataFrame to 'dfs'
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)

    # Rename columns
    df.rename(columns=columns_to_rename, inplace=True)

    # Retain specified columns and drop any other columns
    df = df[columns_to_retain]

    # Append cleaned DataFrame to 'dfs'
    dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
concatenated_df = pd.concat(dfs, ignore_index=True)

# Define the output file path
output_file_path = os.path.join(folder_path, 'concatenated_data_2015_2024.csv')

# Save the concatenated DataFrame to a new CSV file in the same directory
concatenated_df.to_csv(output_file_path, index=False)


# Path to the concatenated CSV file
concatenated_file_path = '/Users/farimah/PycharmProjects/pythonassessment2/2015-2024data/concatenated_data_2015_2024.csv'

# Load the concatenated data into a DataFrame
combined_data = pd.read_csv(concatenated_file_path)


# Convert 'Model Year' column to datetime if it's not already in datetime format
combined_data['Model Year'] = pd.to_datetime(combined_data['Model Year'], format='%Y')


# Define functions for each question

def average_fe_2015_2023():

    # Question 1-How has the average fuel economy evolved from
    # to 2015 to 2023, and what have experts predicted for 2024?

    # Filter data for Model Years between 2015 and 2024
    filtered_data = combined_data[(combined_data['Model Year'].dt.year >= 2015) & (combined_data['Model Year'].dt.year <= 2024)]

    # Group by 'Model Year' and calculate average 'Comb FE (Guide) - Conventional Fuel' for each year
    avg_comb_fe_conventional_by_year = filtered_data.groupby(filtered_data['Model Year'].dt.year)['Combined FE'].mean()

    # Plotting average 'Comb FE (Guide) - Conventional Fuel' for all cars over the years 2016-2024
    plt.figure(figsize=(10, 6))
    plt.plot(avg_comb_fe_conventional_by_year.index, avg_comb_fe_conventional_by_year.values, marker='o', linestyle='-', color='orange')
    plt.xlabel('Year')
    plt.ylabel('Average Combined')
    plt.title('Average Fuel Economy for All Cars from 2015-2024')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def FE_hw_city_152324():

    # Question 2 - Compare City fuel economy and Highway Fuel Economy in terms of how they've evolved
    # from  to 2015 to 2023, and what experts have predicted for 2024.

    # Filter data for Model Years between 2015 and 2024
    filtered_data = combined_data[
        (combined_data['Model Year'].dt.year >= 2015) & (combined_data['Model Year'].dt.year <= 2024)]

    # Group by 'Model Year' and calculate average 'City CO2' and 'Highway CO2' for each year
    avg_city_co2_by_year = filtered_data.groupby(filtered_data['Model Year'].dt.year)['City FE'].mean()
    avg_highway_co2_by_year = filtered_data.groupby(filtered_data['Model Year'].dt.year)['Highway FE'].mean()

    # Plotting average 'City CO2' and 'Highway CO2' for all cars over the years 2015-2024
    plt.figure(figsize=(10, 6))

    # Plotting City CO2
    plt.plot(avg_city_co2_by_year.index, avg_city_co2_by_year.values, marker='o', linestyle='-', color='green',
             label='City FE')

    # Plotting Highway CO2
    plt.plot(avg_highway_co2_by_year.index, avg_highway_co2_by_year.values, marker='o', linestyle='-', color='turquoise',
             label='Highway FE')

    plt.xlabel('Year')
    plt.ylabel('Average Fuel Economy')
    plt.title('Average City and Highway Fuel Economy for All Cars from 2015-2024')
    plt.legend()  # Show legend with labels for City and Highway CO2
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def correlation_fe_engdis_2015_2023():
    # Question 3 -Is there a correlation between engine displacement and fuel economy
    # in the years between 2015 to 2023, and what have experts predicted for 2024?

    # Create empty lists to store correlation coefficients and years
    correlation_coefficients = []
    years = []

    # Loop through each year from 2016 to 2024
    for year in range(2015, 2025):
        data_year = combined_data[combined_data['Model Year'].dt.year == year]
        correlation_coefficient = data_year['Engine Displacement'].corr(data_year['Combined FE'])
        correlation_coefficients.append(correlation_coefficient)
        years.append(year)

    # Plotting correlation coefficients for each year
    plt.figure(figsize=(10, 6))
    bars = plt.bar(years, correlation_coefficients, color='magenta')
    plt.xlabel('Year')
    plt.ylabel('Correlation Coefficient')
    plt.title('Correlation Coefficient between Engine Displacement and Fuel Economy from 2015 to 2024')
    plt.xticks(years)
    plt.grid(axis='y')

    # Annotating each bar with its value
    for bar, coef in zip(bars, correlation_coefficients):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{coef:.2f}',
                 ha='center', va='bottom', color='black', fontsize=12)

    plt.tight_layout()
    plt.show()

def fe_division_2016():
    # Question 4- Create a visualisation that shows the average fuel economy for each division in 2016.

    # Filter data for 2016
    data_2016 = combined_data[combined_data['Model Year'].dt.year == 2016]

    # Group by 'Division' and calculate average 'Comb FE (Guide) - Conventional Fuel' for 2016
    avg_comb_fe_2016 = data_2016.groupby('Division')['Combined FE'].mean().sort_values(ascending=False)

    # Plotting average 'Comb FE (Guide) - Conventional Fuel' for each unique division in 2016
    plt.figure(figsize=(10, 6))
    ax = avg_comb_fe_2016.plot(kind='bar', color='coral')
    ax.set_xlabel('Division')
    ax.set_ylabel('Average Combined FE (2016)')
    ax.set_title('Average FE for Each Division in 2016')
    ax.grid(axis='y')

    plt.tight_layout()
    plt.show()


def fe_division_2024():
    # Question 5- Create a visualisation that shows what experts have predicted for the
    # average fuel economy for each division in 2024.

    # Filter data for 2024
    data_2024 = combined_data[combined_data['Model Year'].dt.year == 2024]

    # Group by 'Division' and calculate average 'Comb FE (Guide) - Conventional Fuel' for 2024
    avg_comb_fe_2024 = data_2024.groupby('Division')['Combined FE'].mean().sort_values(ascending=False)

    # Plotting average 'Comb FE (Guide) - Conventional Fuel' for each unique division in 2024
    plt.figure(figsize=(10, 6))
    ax = avg_comb_fe_2024.plot(kind='bar', color='pink')
    ax.set_xlabel('Division')
    ax.set_ylabel('Average Combined FE (2024)')
    ax.set_title('Average FE for Each Division in 2024')
    ax.grid(axis='y')

    plt.tight_layout()
    plt.show()


def co2_2015_2024():
    # Question 6-How has the average CO2 emissions evolved from  2015 to 2023, and
    # what have experts predicted for 2024?

    # Filter data for Model Years between 2016 and 2024
    filtered_data = combined_data[(combined_data['Model Year'].dt.year >= 2015) & (combined_data['Model Year'].dt.year <= 2024)]

    # Group by 'Model Year', calculate average 'Comb CO2 Rounded Adjusted'
    avg_co2_by_year = filtered_data.groupby(filtered_data['Model Year'].dt.year)['Combined CO2'].mean()

    # Plotting average 'Comb CO2 Rounded Adjusted' trend for years 2016-2024
    avg_co2_by_year.plot(figsize=(10, 6), marker='o')
    plt.xlabel('Year')
    plt.ylabel('Average CO2 Emissions')
    plt.title('Graph showing how the average CO2 Emissions have evolved between 2015 to 2024')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def CO2_hw_city_152324():

    # Question 7 - Compare City CO2 emissions and Highway CO2 emissions in terms of how they've evolved from
    # 2015 to 2023, and what have experts predicted for 2024?

    # Filter data for Model Years between 2015 and 2024
    filtered_data = combined_data[
        (combined_data['Model Year'].dt.year >= 2015) & (combined_data['Model Year'].dt.year <= 2024)]

    # Group by 'Model Year' and calculate average 'City CO2' and 'Highway CO2' for each year
    avg_city_co2_by_year = filtered_data.groupby(filtered_data['Model Year'].dt.year)['City CO2'].mean()
    avg_highway_co2_by_year = filtered_data.groupby(filtered_data['Model Year'].dt.year)['Highway CO2'].mean()

    # Plotting average 'City CO2' and 'Highway CO2' for all cars over the years 2015-2024
    plt.figure(figsize=(10, 6))

    # Plotting City CO2
    plt.plot(avg_city_co2_by_year.index, avg_city_co2_by_year.values, marker='o', linestyle='-', color='magenta',
             label='City CO2')

    # Plotting Highway CO2
    plt.plot(avg_highway_co2_by_year.index, avg_highway_co2_by_year.values, marker='o', linestyle='-', color='indigo',
             label='Highway CO2')

    plt.xlabel('Year')
    plt.ylabel('Average CO2 Emissions')
    plt.title('Average City and Highway CO2 Emissions for All Cars from 2015-2024')
    plt.legend()  # Show legend with labels for City and Highway CO2
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def correlation_fe_co2_2015_2024():
    # Question 8-Is there a correlation between engine displacement and CO2 emissions
    # in the years between 2015 to 2023, and what have experts predicted for 2024?

    # Create empty lists to store correlation coefficients and years
    correlation_coefficients = []
    years = []

    # Loop through each year from 2016 to 2024
    for year in range(2015, 2025):
        data_year = combined_data[combined_data['Model Year'].dt.year == year]
        correlation_coefficient = data_year['Engine Displacement'].corr(data_year['Combined CO2'])
        correlation_coefficients.append(correlation_coefficient)
        years.append(year)

    # Plotting correlation coefficients for each year
    plt.figure(figsize=(10, 6))
    bars = plt.bar(years, correlation_coefficients, color='magenta')
    plt.xlabel('Year')
    plt.ylabel('Correlation Coefficient')
    plt.title('Correlation Coefficient between Engine Displacement and CO2 Emissions from 2015 to 2024')
    plt.xticks(years)
    plt.grid(axis='y')

    # Annotating each bar with its value
    for bar, coef in zip(bars, correlation_coefficients):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{coef:.2f}',
                 ha='center', va='bottom', color='black', fontsize=12)

    plt.tight_layout()
    plt.show()
def co2_2016_division():
    # Question 9-Create a visualisation that shows the average CO2 emissions for each
    # division in 2016.

    # Filter data for 2016
    data_2016 = combined_data[combined_data['Model Year'].dt.year == 2016]

    # Group by 'Division' and calculate average 'Comb CO2 Rounded Adjusted' for 2016
    avg_co2_2016 = data_2016.groupby('Division')['Combined CO2'].mean().sort_values(ascending=False)

    # Plotting average 'Comb CO2 Rounded Adjusted' for each unique division in 2016
    plt.figure(figsize=(9, 6))
    ax = avg_co2_2016.plot(kind='bar', color='blue')
    ax.set_xlabel('Division')
    ax.set_ylabel('Average CO2 (2016)')
    ax.set_title('Average CO2 Emissions in 2016')
    ax.grid(axis='y')
    ax.tick_params(axis='x', labelsize=8)  # Adjusting x-axis tick label size

    plt.tight_layout()
    plt.show()

def co2_2024_division():
    # Question 10-Create a visualisation that shows what experts have predicted for the average CO2
    # emissions for each division in 2024.

    # Filter data for 2024
    data_2024 = combined_data[combined_data['Model Year'].dt.year == 2024]

    # Group by 'Division' and calculate average 'Comb CO2 Rounded Adjusted' for 2024
    avg_co2_2024 = data_2024.groupby('Division')['Combined CO2'].mean().sort_values(ascending=False)

    # Plotting average 'Comb CO2 Rounded Adjusted' for each unique division in 2024
    plt.figure(figsize=(9, 6))
    ax = avg_co2_2024.plot(kind='bar', color='limegreen')
    ax.set_xlabel('Division')
    ax.set_ylabel('Average CO2 (2024)')
    ax.set_title('Average CO2 Emissions in 2024')
    ax.grid(axis='y')
    ax.tick_params(axis='x', labelsize=8)

    plt.tight_layout()
    plt.show()



def console_interface():
    while True:
        print("Enter the question number (1-10) or 'exit' to quit:")
        choice = input().strip()  # Remove leading/trailing whitespace

        if choice.lower() == 'exit':
            break

        try:
            question_number = int(choice)
            if 1 <= question_number <= 10:  # Validate question number range
                if question_number == 1:
                    average_fe_2015_2023()
                elif question_number == 2:
                    FE_hw_city_152324()
                elif question_number == 3:
                    correlation_fe_engdis_2015_2023()
                elif question_number == 4:
                    fe_division_2016()
                elif question_number == 5:
                    fe_division_2024()
                elif question_number == 6:
                    co2_2015_2024()
                elif question_number == 7:
                    CO2_hw_city_152324()
                elif question_number == 8:
                    correlation_fe_co2_2015_2024()
                elif question_number == 9:
                    co2_2016_division()
                elif question_number == 10:
                    co2_2024_division()
            else:
                print("Invalid question number. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number or 'exit'.")

# Run console interface
console_interface()

