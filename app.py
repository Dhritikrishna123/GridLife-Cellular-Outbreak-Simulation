"""
GridLife: Cellular Outbreak Simulation
Main Streamlit application - Enhanced UI with better organization
"""

import streamlit as st
import numpy as np
import time
from grid_simulation import GridSimulation
from visualization import GridVisualizer

# Page configuration
st.set_page_config(
    page_title="GridLife: Outbreak Simulation",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'simulation' not in st.session_state:
    st.session_state.simulation = GridSimulation(width=40, height=40)
    st.session_state.visualizer = GridVisualizer()
    st.session_state.history = []
    st.session_state.auto_run = False
    st.session_state.previous_achievements = set()
    st.session_state.show_risk_map = False
    st.session_state.show_stats_panel = True
    st.session_state.simulation_speed = 0.8

# Preset scenarios with descriptions
SCENARIOS = {
    "🧟 Zombie Apocalypse": {
        "infection": 0.8, "death": 0.05, "immunity": 0.01,
        "description": "Highly contagious but low mortality - spreads like wildfire!"
    },
    "🛡️ Super Immunity": {
        "infection": 0.3, "death": 0.1, "immunity": 0.4,
        "description": "Strong immune response helps population resist infection"
    },
    "💀 Black Death": {
        "infection": 0.4, "death": 0.3, "immunity": 0.05,
        "description": "Deadly plague with high mortality and little immunity"
    },
    "🔬 Lab Experiment": {
        "infection": 0.2, "death": 0.15, "immunity": 0.25,
        "description": "Controlled parameters for scientific observation"
    },
    "🤧 Seasonal Flu": {
        "infection": 0.25, "death": 0.02, "immunity": 0.15,
        "description": "Common seasonal outbreak with mild symptoms"
    }
}

# Outbreak patterns with descriptions
OUTBREAK_PATTERNS = {
    "🎯 Patient Zero": {
        "key": "patient_zero",
        "description": "Single infection point in center - classic outbreak"
    },
    "✈️ Airport Spread": {
        "key": "airport_spread",
        "description": "Multiple distant points - like international travel"
    },
    "🛡️ Border Invasion": {
        "key": "border_invasion",
        "description": "Infection enters from edges - external threat"
    },
    "🏙️ Urban Centers": {
        "key": "urban_centers",
        "description": "Clustered infections in populated areas"
    },
    "🎲 Random Chaos": {
        "key": "random_chaos",
        "description": "Random scattered infections - unpredictable spread"
    }
}

def reset_simulation():
    """Reset the simulation to initial state"""
    st.session_state.simulation.reset_grid()
    st.session_state.history = []
    st.session_state.auto_run = False
    st.session_state.previous_achievements = set()

def get_simulation_status():
    """Get current simulation status for display"""
    current_stats = st.session_state.simulation.get_population_stats()
    total_pop = st.session_state.simulation.width * st.session_state.simulation.height
    
    if st.session_state.simulation.has_infected_cells():
        return "🟢 Active Outbreak", "success"
    elif current_stats['step'] > 0:
        if current_stats['dead'] == total_pop:
            return "💀 Total Extinction", "error"
        elif current_stats['immune'] > current_stats['dead']:
            return "🛡️ Immunity Prevailed", "success"
        else:
            return "🎯 Outbreak Contained", "info"
    else:
        return "⏸️ Ready to Start", "info"

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .scenario-card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .status-indicator {
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        padding: 0.5rem;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with improved styling
st.markdown("""
<div class="main-header">
    <h1>🧬 GridLife: Outbreak Simulation</h1>
    <p>Interactive cellular automaton for studying infectious disease dynamics</p>
</div>
""", unsafe_allow_html=True)

# Enhanced sidebar with better organization
with st.sidebar:
    st.header("🎛️ Simulation Controls")
    
    # Simulation settings section
    with st.expander("⚙️ Grid Settings", expanded=True):
        grid_size = st.selectbox(
            "Grid Size", 
            [20, 30, 40, 50, 60], 
            index=2,
            help="Larger grids show more complex dynamics but run slower"
        )
        if grid_size != st.session_state.simulation.width:
            st.session_state.simulation = GridSimulation(width=grid_size, height=grid_size)
            st.session_state.history = []
    
    st.divider()
    
    # Scenario selection with enhanced UI
    with st.expander("🦠 Disease Parameters", expanded=True):
        scenario_choice = st.selectbox(
            "Choose Scenario", 
            ["Custom Parameters"] + list(SCENARIOS.keys()),
            help="Select a preset scenario or customize your own parameters"
        )
        
        if scenario_choice != "Custom Parameters":
            scenario_data = SCENARIOS[scenario_choice]
            st.info(scenario_data["description"])
            infection_rate = scenario_data["infection"]
            death_rate = scenario_data["death"] 
            immunity_rate = scenario_data["immunity"]
            
            # Display current parameters
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🦠 Infection", f"{infection_rate:.0%}")
            with col2:
                st.metric("💀 Death", f"{death_rate:.0%}")
            with col3:
                st.metric("🛡️ Immunity", f"{immunity_rate:.0%}")
        else:
            # Custom parameters with better descriptions
            infection_rate = st.slider(
                "🦠 Infection Rate", 
                0.05, 0.95, 0.3, 0.05,
                help="Probability of infection spread per infected neighbor"
            )
            death_rate = st.slider(
                "💀 Death Rate", 
                0.01, 0.5, 0.08, 0.01,
                help="Probability that infected individuals die each step"
            )
            immunity_rate = st.slider(
                "🛡️ Immunity Rate", 
                0.0, 0.6, 0.05, 0.01,
                help="Probability that infected individuals recover with immunity"
            )
    
    st.divider()
    
    # Outbreak pattern selection
    with st.expander("🎯 Starting Pattern", expanded=True):
        pattern_choice = st.selectbox(
            "Outbreak Pattern", 
            list(OUTBREAK_PATTERNS.keys()),
            help="How the initial infections are distributed"
        )
        pattern_info = OUTBREAK_PATTERNS[pattern_choice]
        st.caption(pattern_info["description"])
    
    # Control buttons with better layout
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start Outbreak", use_container_width=True, type="primary"):
            pattern_key = pattern_info["key"]
            st.session_state.simulation.apply_outbreak_pattern(pattern_key)
            st.success("Outbreak started!")
    with col2:
        if st.button("🔄 Reset Grid", use_container_width=True):
            reset_simulation()
            st.success("Grid reset!")
    
    st.divider()
    
    # Simulation controls
    with st.expander("▶️ Playback Controls", expanded=True):
        st.session_state.auto_run = st.checkbox(
            "Auto Run", 
            st.session_state.auto_run,
            help="Automatically advance simulation steps"
        )
        
        if st.session_state.auto_run:
            st.session_state.simulation_speed = st.slider(
                "Speed", 
                0.2, 3.0, 
                st.session_state.simulation_speed, 
                0.2,
                help="Steps per second"
            )
        
        if not st.session_state.auto_run:
            if st.button("➡️ Next Step", use_container_width=True):
                if st.session_state.simulation.has_infected_cells():
                    st.session_state.simulation.update_step(infection_rate, death_rate, immunity_rate)
                else:
                    st.warning("No active infections to simulate")
    
    # Display options
    st.divider()
    with st.expander("👁️ Display Options"):
        st.session_state.show_risk_map = st.checkbox(
            "🎯 Show Risk Map", 
            st.session_state.show_risk_map,
            help="Highlight areas at risk of infection"
        )
        st.session_state.show_stats_panel = st.checkbox(
            "📊 Show Statistics Panel", 
            st.session_state.show_stats_panel,
            help="Display detailed population statistics"
        )

# Main content area with improved layout
if st.session_state.show_stats_panel:
    grid_col, stats_col = st.columns([2, 1])
else:
    grid_col = st.container()
    stats_col = None

with grid_col:
    # Get current stats and update history
    current_stats = st.session_state.simulation.get_population_stats()
    if not st.session_state.history or st.session_state.history[-1]['step'] != current_stats['step']:
        st.session_state.history.append(current_stats)
    
    # Check for new achievements
    new_achievements = st.session_state.simulation.get_new_achievements(st.session_state.previous_achievements)
    if new_achievements:
        for achievement in new_achievements:
            st.balloons()
            st.success(f"🏆 Achievement Unlocked: **{achievement}**!")
        st.session_state.previous_achievements = current_stats['achievements'].copy()
    
    # Display simulation status
    status_text, status_type = get_simulation_status()
    if status_type == "success":
        st.success(status_text)
    elif status_type == "error":
        st.error(status_text)
    else:
        st.info(status_text)
    
    # Main grid visualization
    risk_map = st.session_state.simulation.get_infection_risk_map() if st.session_state.show_risk_map else None
    
    grid_fig = st.session_state.visualizer.plot_grid(
        st.session_state.simulation.get_grid_copy(),
        f"Step {current_stats['step']} - Population: {sum([current_stats['healthy'], current_stats['infected'], current_stats['immune'], current_stats['dead']])}",
        show_risk=st.session_state.show_risk_map,
        risk_map=risk_map
    )
    st.pyplot(grid_fig)

# Statistics panel (if enabled)
if stats_col and st.session_state.show_stats_panel:
    with stats_col:
        st.subheader("📊 Live Statistics")
        
        # Population metrics with enhanced display
        st.session_state.visualizer.create_stats_display(current_stats)
        
        # Achievements section
        if current_stats['achievements']:
            st.divider()
            st.subheader("🏆 Achievements")
            st.session_state.visualizer.display_achievements(current_stats['achievements'])
        
        # Population trends chart
        if len(st.session_state.history) > 3:
            st.divider()
            st.subheader("📈 Population Trends")
            trend_fig = st.session_state.visualizer.plot_population_stats(st.session_state.history)
            if trend_fig:
                st.pyplot(trend_fig)
        
        # Quick stats summary
        st.divider()
        st.subheader("📋 Summary")
        total_pop = grid_size * grid_size
        infection_rate_current = current_stats['infected'] / total_pop * 100
        mortality_rate = current_stats['dead'] / max(1, current_stats['total_ever_infected']) * 100
        
        st.metric("Current Infection Rate", f"{infection_rate_current:.1f}%")
        st.metric("Mortality Rate", f"{mortality_rate:.1f}%")
        if current_stats['step'] > 0:
            st.metric("Days Elapsed", current_stats['step'])

# Auto-run logic
if st.session_state.auto_run and st.session_state.simulation.has_infected_cells():
    time.sleep(1.0 / st.session_state.simulation_speed)
    st.session_state.simulation.update_step(infection_rate, death_rate, immunity_rate)
    st.rerun()

# Enhanced footer with tips
st.divider()
with st.expander("💡 Quick Tips & Help"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Getting Started:**
        1. Choose a scenario preset or customize parameters
        2. Select an outbreak starting pattern
        3. Click "🚀 Start Outbreak"
        4. Enable "Auto Run" to watch it evolve
        """)
    with col2:
        st.markdown("""
        **Pro Tips:**
        - Use Risk Map to see infection probability
        - Try extreme parameters for interesting results
        - Watch for achievement notifications
        - Compare different starting patterns
        """)

st.markdown("---")
st.caption("**GridLife** - An interactive cellular automaton for exploring infectious disease dynamics • Built with Streamlit & NumPy")