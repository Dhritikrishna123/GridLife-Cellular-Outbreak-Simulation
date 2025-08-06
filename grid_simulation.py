"""
GridLife: Cellular Outbreak Simulation
Enhanced core simulation logic with improved performance and features
"""

import numpy as np
from scipy import ndimage

class GridSimulation:
    def __init__(self, width=50, height=50):
        """Initialize the simulation grid with enhanced tracking"""
        self.width = width
        self.height = height
        self.reset_grid()
        
        # Neighbor counting kernel (3x3 grid with Moore neighborhood)
        self.neighbor_kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],  # Center cell doesn't count itself
            [1, 1, 1]
        ])
        
        # Cell states - using constants for clarity
        self.HEALTHY = 0
        self.INFECTED = 1
        self.IMMUNE = 2
        self.DEAD = 3
        
        # Enhanced tracking for better analytics
        self.achievements = set()
        self.infection_trails = np.zeros((self.height, self.width))
        self.infection_history = []  # Track infection spread over time
        
    def reset_grid(self):
        """Reset grid to all healthy cells with comprehensive state reset"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.step_count = 0
        self.achievements = set()
        self.infection_trails = np.zeros((self.height, self.width))
        
        # Enhanced statistics tracking
        self.peak_infected = 0
        self.total_ever_infected = 0
        self.total_deaths = 0
        self.total_recoveries = 0
        self.infection_history = []
        self.first_infection_step = None
        self.outbreak_contained_step = None
        
    def apply_outbreak_pattern(self, pattern_name):
        """Apply different outbreak starting patterns with validation"""
        self.reset_grid()
        
        patterns = {
            "patient_zero": self._pattern_patient_zero,
            "airport_spread": self._pattern_airport_spread,
            "border_invasion": self._pattern_border_invasion,
            "urban_centers": self._pattern_urban_centers,
            "random_chaos": self._pattern_random_chaos
        }
        
        if pattern_name in patterns:
            patterns[pattern_name]()
            self.first_infection_step = 0
            self._update_infection_stats()
        else:
            raise ValueError(f"Unknown pattern: {pattern_name}")
            
    def _pattern_patient_zero(self):
        """Single infection in center - classic epidemic start"""
        center_x, center_y = self.width // 2, self.height // 2
        self.grid[center_y, center_x] = self.INFECTED
        self.infection_trails[center_y, center_x] = 1
        
    def _pattern_airport_spread(self):
        """Multiple distant infection points simulating travel-based spread"""
        # Calculate positions based on grid size for better scaling
        positions = [
            (self.width // 4, self.height // 4),
            (3 * self.width // 4, self.height // 4),
            (self.width // 2, 3 * self.height // 4),
            (self.width // 4, 3 * self.height // 4)
        ]
        
        for x, y in positions:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = self.INFECTED
                self.infection_trails[y, x] = 1
                
    def _pattern_border_invasion(self):
        """Infection starts from edges - external threat simulation"""
        border_density = max(3, min(8, self.width // 8))  # Adaptive spacing
        
        # Top and bottom borders
        for i in range(0, self.width, border_density):
            if i < self.width:
                self.grid[0, i] = self.INFECTED
                self.grid[self.height-1, i] = self.INFECTED
                self.infection_trails[0, i] = 1
                self.infection_trails[self.height-1, i] = 1
        
        # Left and right borders  
        for i in range(0, self.height, border_density):
            if i < self.height:
                self.grid[i, 0] = self.INFECTED
                self.grid[i, self.width-1] = self.INFECTED
                self.infection_trails[i, 0] = 1
                self.infection_trails[i, self.width-1] = 1
                
    def _pattern_urban_centers(self):
        """Clustered infections in specific areas - city-like outbreak"""
        # Dynamic center calculation based on grid size
        num_centers = max(2, self.width // 20)
        center_radius = max(2, self.width // 15)
        
        # Generate centers with some randomness
        for i in range(num_centers):
            base_x = (i + 1) * self.width // (num_centers + 1)
            base_y = (i + 1) * self.height // (num_centers + 1)
            
            # Add some randomness to center positions
            cx = base_x + np.random.randint(-self.width//10, self.width//10)
            cy = base_y + np.random.randint(-self.height//10, self.height//10)
            cx = max(center_radius, min(self.width - center_radius, cx))
            cy = max(center_radius, min(self.height - center_radius, cy))
            
            # Create cluster around center
            for dx in range(-center_radius, center_radius + 1):
                for dy in range(-center_radius, center_radius + 1):
                    x, y = cx + dx, cy + dy
                    if (0 <= x < self.width and 0 <= y < self.height and 
                        np.random.random() < 0.3):  # 30% infection probability in cluster
                        self.grid[y, x] = self.INFECTED
                        self.infection_trails[y, x] = 1
                        
    def _pattern_random_chaos(self):
        """Random infections across grid - unpredictable spread"""
        # Scale number of initial infections with grid size
        infection_density = 0.005  # 0.5% of grid
        num_infections = max(5, int(self.width * self.height * infection_density))
        
        infected_positions = set()
        while len(infected_positions) < num_infections:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            infected_positions.add((x, y))
        
        for x, y in infected_positions:
            self.grid[y, x] = self.INFECTED
            self.infection_trails[y, x] = 1

    def infect_cell(self, x, y):
        """Manually infect a cell at position (x, y) with validation"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
            
        if self.grid[y, x] == self.HEALTHY:
            self.grid[y, x] = self.INFECTED
            self.infection_trails[y, x] = 1
            self._update_infection_stats()
            return True
        return False
        
    def count_neighbors(self, cell_type):
        """Count neighbors of specific type using optimized convolution"""
        # Create binary mask for specific cell type
        type_mask = (self.grid == cell_type).astype(np.uint8)
        
        # Use optimized convolution for neighbor counting
        neighbor_count = ndimage.convolve(
            type_mask, 
            self.neighbor_kernel, 
            mode='constant', 
            cval=0
        )
        return neighbor_count
        
    def update_step(self, infection_rate=0.3, death_rate=0.1, immunity_rate=0.05):
        """Enhanced simulation step with better state management"""
        if not self.has_infected_cells():
            if self.step_count > 0 and self.outbreak_contained_step is None:
                self.outbreak_contained_step = self.step_count
            return
            
        # Count infected neighbors for transmission calculation
        infected_neighbors = self.count_neighbors(self.INFECTED)
        
        # Generate random probability matrices for stochastic processes
        infection_prob = np.random.random((self.height, self.width))
        death_prob = np.random.random((self.height, self.width))
        immunity_prob = np.random.random((self.height, self.width))
        
        # Enhanced infection calculation with distance-based transmission
        # Normalize by maximum possible neighbors (8) for probability calculation
        base_infection_chance = infected_neighbors * infection_rate / 8.0
        
        # Apply infection rules - healthy cells with infected neighbors
        new_infections = (
            (self.grid == self.HEALTHY) & 
            (infected_neighbors > 0) & 
            (infection_prob < base_infection_chance)
        )
        
        # Apply death rules - infected cells die based on death rate
        new_deaths = (
            (self.grid == self.INFECTED) & 
            (death_prob < death_rate)
        )
        
        # Apply immunity rules - infected cells that survive may become immune
        new_immunity = (
            (self.grid == self.INFECTED) & 
            (~new_deaths) &  # Can't become immune if dead
            (immunity_prob < immunity_rate)
        )
        
        # Update grid states atomically to avoid conflicts
        self.grid[new_infections] = self.INFECTED
        self.grid[new_deaths] = self.DEAD
        self.grid[new_immunity] = self.IMMUNE
        
        # Update infection trails for visualization
        self.infection_trails[new_infections] = 1
        
        # Increment step counter
        self.step_count += 1
        
        # Update comprehensive statistics
        self._update_infection_stats()
        
        # Record infection history for analysis
        current_infected = np.sum(self.grid == self.INFECTED)
        self.infection_history.append({
            'step': self.step_count,
            'infected': current_infected,
            'new_infections': np.sum(new_infections),
            'new_deaths': np.sum(new_deaths),
            'new_recoveries': np.sum(new_immunity)
        })
        
        # Check for achievements after state update
        self._check_achievements()

    def _update_infection_stats(self):
        """Update comprehensive infection statistics"""
        current_infected = np.sum(self.grid == self.INFECTED)
        self.peak_infected = max(self.peak_infected, current_infected)
        
        # Calculate total ever infected (current + recovered + dead)
        self.total_ever_infected = np.sum(
            (self.grid == self.INFECTED) | 
            (self.grid == self.IMMUNE) | 
            (self.grid == self.DEAD)
        )
        
        self.total_deaths = np.sum(self.grid == self.DEAD)
        self.total_recoveries = np.sum(self.grid == self.IMMUNE)

    def _check_achievements(self):
        """Enhanced achievement system with more detailed conditions"""
        stats = self.get_population_stats()
        total_pop = self.width * self.height
        
        # Patient Zero - first infection started
        if stats['infected'] > 0 and 'Patient Zero' not in self.achievements:
            self.achievements.add("Patient Zero")
            
        # Rapid Spread - 25% infected within 10 steps
        if (self.step_count <= 10 and 
            stats['infected'] >= 0.25 * total_pop and 
            'Rapid Spread' not in self.achievements):
            self.achievements.add("Rapid Spread")
            
        # Pandemic - 80% peak infection rate achieved
        if self.peak_infected >= 0.8 * total_pop and 'Pandemic' not in self.achievements:
            self.achievements.add("Pandemic")
            
        # Extinction Event - 100% mortality
        if stats['dead'] == total_pop and 'Extinction Event' not in self.achievements:
            self.achievements.add("Extinction Event")
            
        # Survivor - 50% healthy after 100 steps with no active infections
        if (self.step_count >= 100 and 
            stats['healthy'] >= 0.5 * total_pop and 
            stats['infected'] == 0 and 
            'Survivor' not in self.achievements):
            self.achievements.add("Survivor")
            
        # Herd Immunity - stable population with >30% immunity and no infections
        if (stats['immune'] >= 0.3 * total_pop and 
            stats['infected'] == 0 and 
            stats['healthy'] > 0 and 
            'Herd Immunity' not in self.achievements):
            self.achievements.add("Herd Immunity")
            
        # Containment Master - low infection rate maintained
        if (self.step_count >= 50 and 
            self.peak_infected <= 0.2 * total_pop and 
            stats['infected'] == 0 and 
            'Containment Master' not in self.achievements):
            self.achievements.add("Containment Master")
            
        # Endemic State - stable low-level infection for 50+ steps
        if (self.step_count >= 50 and 
            len(self.infection_history) >= 20):
            recent_infections = [h['infected'] for h in self.infection_history[-20:]]
            if (all(0 < inf < 0.1 * total_pop for inf in recent_infections) and 
                'Endemic State' not in self.achievements):
                self.achievements.add("Endemic State")
        
        # Ghost Town - >90% mortality rate
        if (self.total_ever_infected > 0.5 * total_pop and 
            self.total_deaths >= 0.9 * self.total_ever_infected and
            'Ghost Town' not in self.achievements):
            self.achievements.add("Ghost Town")
            
    def get_infection_risk_map(self):
        """Enhanced risk map calculation with weighted neighbors"""
        infected_neighbors = self.count_neighbors(self.INFECTED)
        risk_map = np.zeros_like(self.grid, dtype=float)
        
        # Calculate risk only for healthy cells
        healthy_mask = (self.grid == self.HEALTHY)
        
        # Risk is proportional to infected neighbors, capped at 1.0
        risk_map[healthy_mask] = np.minimum(
            infected_neighbors[healthy_mask] / 8.0, 1.0
        )
        
        # Add slight risk boost for cells near recent infections (trails)
        trail_boost = ndimage.gaussian_filter(self.infection_trails, sigma=1.0) * 0.1
        risk_map[healthy_mask] += trail_boost[healthy_mask]
        risk_map = np.minimum(risk_map, 1.0)  # Keep risk ≤ 1.0
        
        return risk_map
        
    def get_transmission_rate(self):
        """Calculate current effective transmission rate"""
        if len(self.infection_history) < 2:
            return 0.0
            
        recent_history = self.infection_history[-5:]  # Last 5 steps
        total_new_infections = sum(h['new_infections'] for h in recent_history)
        total_infected_exposure = sum(h['infected'] for h in recent_history[:-1])
        
        if total_infected_exposure == 0:
            return 0.0
            
        return total_new_infections / total_infected_exposure
        
    def get_mortality_rate(self):
        """Calculate current mortality rate"""
        if self.total_ever_infected == 0:
            return 0.0
        return self.total_deaths / self.total_ever_infected
        
    def get_recovery_rate(self):
        """Calculate current recovery rate"""
        if self.total_ever_infected == 0:
            return 0.0
        return self.total_recoveries / self.total_ever_infected
        
    def get_new_achievements(self, previous_achievements):
        """Get newly earned achievements since last check"""
        return self.achievements - previous_achievements

    def get_population_stats(self):
        """Get comprehensive population statistics"""
        unique, counts = np.unique(self.grid, return_counts=True)
        stats = {i: 0 for i in range(4)}  # Initialize all states to 0
        
        for state, count in zip(unique, counts):
            stats[state] = count
            
        # Calculate additional derived statistics
        total_pop = self.width * self.height
        
        return {
            'healthy': stats[self.HEALTHY],
            'infected': stats[self.INFECTED], 
            'immune': stats[self.IMMUNE],
            'dead': stats[self.DEAD],
            'step': self.step_count,
            'peak_infected': self.peak_infected,
            'total_ever_infected': self.total_ever_infected,
            'total_deaths': self.total_deaths,
            'total_recoveries': self.total_recoveries,
            'transmission_rate': self.get_transmission_rate(),
            'mortality_rate': self.get_mortality_rate(),
            'recovery_rate': self.get_recovery_rate(),
            'population_density': total_pop / (self.width * self.height),
            'achievements': self.achievements.copy(),
            'outbreak_contained': self.outbreak_contained_step is not None,
            'outbreak_active': self.has_infected_cells()
        }
        
    def has_infected_cells(self):
        """Check if simulation should continue (any infected cells remain)"""
        return np.any(self.grid == self.INFECTED)
        
    def get_grid_copy(self):
        """Get a copy of current grid state for visualization"""
        return self.grid.copy()
        
    def get_trails_copy(self):
        """Get a copy of infection trails for enhanced visualization"""
        return self.infection_trails.copy()
        
    def get_infection_history(self):
        """Get complete infection history for analysis"""
        return self.infection_history.copy()
        
    def export_state(self):
        """Export complete simulation state for analysis or saving"""
        return {
            'grid': self.grid.copy(),
            'step_count': self.step_count,
            'infection_trails': self.infection_trails.copy(),
            'infection_history': self.infection_history.copy(),
            'achievements': self.achievements.copy(),
            'statistics': self.get_population_stats()
        }