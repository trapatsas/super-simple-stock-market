# Super Simple Stock Market

The "Super Simple Stock Market" is a Python-based simulation designed to illustrate the basic principles of a stock market system. This project facilitates the simulation of trading activities, calculation of dividend yields, and tracking of stock price changes in a simplified environment.

## Running the project using Dev Containers
This project supports development in a containerized environment using Docker and Visual Studio Code DevContainers. This ensures that you have a consistent, isolated, and reproducible environment.

### Prerequisites
- Install Docker
- Install Visual Studio Code
- Install the `Dev Containers` extension for Visual Studio Code

### Steps to Open and Run the Project
1. Open Visual Studio Code and clone the repository within VS Code or open the project folder if already cloned.
2. Press F1 to open the command palette and type `Dev Containers: Open Folder in Container...`. Select the project folder and it will start building the container.
3. Wait for the container to build. This may take a few minutes the first time as it downloads the necessary Docker image and sets up the environment.
4. Once the build is complete, VS Code will automatically connect to the container. You can now run scripts and use the terminal inside Visual Studio Code to execute any project-related commands in a Docker environment.
5. Run the project or tests by using the integrated terminal in VS Code.

## Running the project without Dev Containers
If you prefer not to use Docker and Visual Studio Code Dev Containers, you can run the project directly on your local machine. Follow these steps to set up and run the project locally:

### Upgrade pip and install required packages
```bash
echo "Upgrading pip and installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the unit tests
```bash
echo "Running unit tests..."
python -m unittest discover -s tests -v
```
### Run coverage analysis
```bash
echo "Analyzing code coverage..."
coverage run -m unittest discover -s tests -v
coverage html
```

This should produce the following report:
![Test Coverage Report](<coverage_report.png>)

### Run the simulation example
```bash
echo "Running the stock market simulation..."
python3 -m examples.simulation
```

## Code Pointers to Requirements Implementation

This section provides direct links to the specific code implementations of major functionalities and requirements outlined in the project requirements file. Each link points to the relevant file and line in this GitHub repository where you can see how each feature is coded.

1. **Functions to return the Dividend Yield for any given stock**
   - Dividend Yield for Common stock: [app/stock.py](https://github.com/trapatsas/super-simple-stock-market/blob/main/app/stock.py#L18)
   - Dividend Yield for Preferred stock: [app/stock.py](https://github.com/trapatsas/super-simple-stock-market/blob/main/app/stock.py#L43)
   - Calculatiuons of the divident yield for each stock: [examples/simulation.py](https://github.com/trapatsas/super-simple-stock-market/blob/main/examples/simulation.py#L33)

2. Function to update multiple stock prices at once: [app/market.py](https://github.com/trapatsas/super-simple-stock-market/blob/43160e1eb268244019d8a1b3d328a6b7f295dfcd/app/market.py#L48)
3. Function to to record a trade: [app/market.py](https://github.com/trapatsas/super-simple-stock-market/blob/43160e1eb268244019d8a1b3d328a6b7f295dfcd/app/market.py#L21)
4. Function to return the Volume Weighted Stock Price on the trades in the past 15 minutes, for a given stock: [app/market.py](https://github.com/trapatsas/super-simple-stock-market/blob/43160e1eb268244019d8a1b3d328a6b7f295dfcd/app/market.py#L54)
5. Function to compute the Geometric Mean of prices for all stocks: [app/market.py](https://github.com/trapatsas/super-simple-stock-market/blob/43160e1eb268244019d8a1b3d328a6b7f295dfcd/app/market.py#L66)


