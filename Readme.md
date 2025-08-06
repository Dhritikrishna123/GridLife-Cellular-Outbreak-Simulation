# 🧬 GridLife: Cellular Outbreak Simulation

A sophisticated cellular automaton simulation that models infectious disease spread through a population grid using NumPy-based calculations and Streamlit visualization.

## 🎮 How It Works

### Core Simulation Logic

GridLife uses a **cellular automaton** approach where each cell in the grid represents an individual in one of four states:

- **🟢 Healthy (0)**: Susceptible to infection
- **🔴 Infected (1)**: Actively spreading the disease
- **🔵 Immune (2)**: Protected from future infection
- **⚫ Dead (3)**: No longer participates in simulation

### Infection Mechanics

The simulation uses **neighbor-based transmission** with the following rules:

1. **Infection Spread**: Healthy cells become infected based on:
   - Number of infected neighbors (3x3 grid around each cell)
   - Base infection rate parameter
   - Random probability calculation
   - Formula: `infection_chance = (infected_neighbors × infection_rate) / 8`

2. **State Transitions**: Each simulation step, infected cells can:
   - **Die**: Based on death_rate probability
   - **Recover with Immunity**: Based on immunity_rate probability
   - **Remain Infected**: Continue spreading if neither occurs

3. **Neighbor Counting**: Uses scipy's `ndimage.convolve()` with a 3x3 kernel for efficient neighbor detection:
   ```
   [1, 1, 1]
   [1, 0, 1]  # Center cell doesn't count itself
   [1, 1, 1]
   ```

### Mathematical Model

For each time step, the simulation calculates:

- **Infection Probability**: `P(infection) = min(1, neighbors_infected × rate / 8)`
- **Death Probability**: `P(death) = death_rate` (for infected cells)
- **Immunity Probability**: `P(immunity) = immunity_rate` (for infected cells that don't die)

## 🚀 Features

### Outbreak Patterns
- **🎯 Patient Zero**: Single central infection point
- **✈️ Airport Spread**: Multiple distant infection clusters
- **🛡️ Border Invasion**: Infection starts from grid edges
- **🏙️ Urban Centers**: Clustered infections in specific areas
- **🎲 Random Chaos**: Random infections across the grid

### Preset Scenarios
- **🧟 Zombie Apocalypse**: High spread (80%), low death (5%)
- **🛡️ Super Immunity**: Moderate spread (30%), high immunity (40%)
- **💀 Black Death**: Moderate spread (40%), high death (30%)
- **🔬 Lab Experiment**: Balanced parameters for study
- **🤧 Seasonal Flu**: Mild outbreak with typical flu characteristics

### Achievement System
- **Patient Zero**: Start your first outbreak
- **Pandemic**: Achieve 80% peak infection rate
- **Survivor**: Keep 50% healthy after 100 steps
- **Extinction Event**: Reach 100% mortality
- **Herd Immunity**: Achieve population stability through immunity
- **Containment Master**: Maintain low infection rates

### Visualization Features
- **Risk Map**: Shows infection probability heat map for healthy cells
- **Population Trends**: Real-time graphs of population changes
- **Interactive Controls**: Adjust parameters and observe results
- **Auto-Run Mode**: Continuous simulation with adjustable speed

## 🛠️ Technical Implementation

### Performance Optimizations
- **Vectorized Operations**: All calculations use NumPy arrays for speed
- **Efficient Neighbor Counting**: Convolution-based neighbor detection
- **Memory Management**: Minimal object creation during simulation steps

### File Structure
```
gridlife/
│
├── app.py                 # Main Streamlit application
├── grid_simulation.py     # Core simulation logic
├── visualization.py       # Matplotlib plotting and UI components
└── README.md             # This file
```

## 🎯 Getting Started

### Installation
```bash
pip install streamlit numpy scipy matplotlib
```

### Running the Simulation
```bash
streamlit run app.py
```

### Quick Start Guide
1. **Choose Scenario**: Select from presets or create custom parameters
2. **Select Pattern**: Pick an outbreak starting pattern
3. **Start Simulation**: Click "🚀 Start" to begin
4. **Control Flow**: Use "▶️ Auto Run" or step manually with "➡️ Step"
5. **Analyze Results**: Watch population trends and earn achievements

## 🔬 Educational Applications

### Epidemiology Concepts
- **Basic Reproduction Number (R₀)**: Observe how infection rates affect spread
- **Herd Immunity Threshold**: Experiment with immunity rates
- **Contact Networks**: Understand neighbor-based transmission
- **Outbreak Patterns**: Compare different initial infection distributions

### Parameter Sensitivity
- **Infection Rate**: Higher values create faster, wider spread
- **Death Rate**: Affects population survival and immunity development
- **Immunity Rate**: Determines if population develops resistance
- **Grid Size**: Influences population density effects

## 🎮 Gameplay Strategy

### Achieving Different Outcomes
- **Pandemic**: Use high infection rate with border invasion pattern
- **Containment**: Balance parameters to limit spread
- **Survival**: High immunity rate with strategic starting patterns
- **Extinction**: High death rate with widespread initial infections

### Experimental Questions
- What happens with zero immunity rate?
- How does grid size affect outbreak dynamics?
- Which starting pattern is most/least dangerous?
- Can you create a "slow burn" outbreak?

## 🔧 Customization

### Adding New Patterns
Extend the `OUTBREAK_PATTERNS` dictionary in `app.py` and implement corresponding methods in `grid_simulation.py`.

### New Achievements
Add achievement logic in the `_check_achievements()` method of `GridSimulation` class.

### Visual Enhancements
Modify color schemes and plot styles in the `GridVisualizer` class.

## 📊 Understanding the Data

### Population Statistics
- **Current Counts**: Real-time population in each state
- **Peak Infected**: Maximum simultaneous infections reached
- **Total Ever Infected**: Cumulative infections throughout simulation
- **Step Count**: Current simulation time step

### Trend Analysis
Watch for:
- **Exponential Growth**: Rapid infection increase
- **Peak and Decline**: Natural outbreak progression  
- **Steady States**: Stable population distributions
- **Oscillations**: Cyclic infection patterns

## 🏆 Achievement Guide

Each achievement represents different epidemiological outcomes:

- **Patient Zero**: Understanding outbreak initiation
- **Pandemic**: Observing uncontrolled spread
- **Survivor**: Population resilience mechanisms
- **Extinction Event**: Total system collapse
- **Herd Immunity**: Natural disease control
- **Containment Master**: Successful intervention

## 💡 Tips for Exploration

1. **Start Simple**: Begin with preset scenarios to understand basics
2. **Vary One Parameter**: Change one setting at a time to isolate effects
3. **Compare Patterns**: Try same parameters with different starting patterns
4. **Watch the Trends**: Population graphs reveal important dynamics
5. **Use Risk Maps**: Understand spatial infection probability
6. **Experiment with Extremes**: Try very high/low parameter values

## 🔮 Future Enhancements

Potential additions:
- Vaccination mechanics
- Population mobility
- Variable transmission rates
- Age-structured populations
- Seasonal effects
- Multiple pathogen strains

---

**GridLife** provides an engaging way to explore infectious disease dynamics through interactive simulation and visualization. Perfect for educational use, research exploration, or simply understanding how outbreaks spread through populations.