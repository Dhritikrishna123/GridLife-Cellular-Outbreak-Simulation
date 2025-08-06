"""
GridLife: Enhanced Visualization Components
Advanced plotting and visual display with improved aesthetics and functionality
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

class GridVisualizer:
    def __init__(self):
        """Initialize visualizer with enhanced color schemes and styling"""
        # Enhanced color palette for better visibility and aesthetics
        self.colors = {
            0: '#2E8B57',  # Healthy - Sea Green (more vibrant)
            1: '#FF4500',  # Infected - Orange Red (more visible than crimson)
            2: '#1E90FF',  # Immune - Dodger Blue (brighter blue)
            3: '#2F2F2F'   # Dead - Dark Gray (unchanged)
        }
        
        self.color_list = [self.colors[i] for i in range(4)]
        
        # Enhanced color maps for different visualizations
        self.risk_cmap = LinearSegmentedColormap.from_list(
            "risk", ["#FFFF99", "#FFB366", "#FF6B6B", "#CC2936"], N=256
        )
        
        self.trail_cmap = LinearSegmentedColormap.from_list(
            "trails", ["#FFFFFF00", "#FFD700", "#FF8C00", "#FF4500"], N=256
        )
        
        # Set matplotlib style for better appearance
        plt.style.use('default')
        self.figure_style = {
            'facecolor': 'white',
            'edgecolor': 'none',
            'dpi': 100
        }
        
    def plot_grid(self, grid, title="Grid State", trails=None, show_risk=False, risk_map=None):
        """Enhanced grid visualization with multiple overlay options"""
        fig, ax = plt.subplots(figsize=(10, 10), **self.figure_style)
        
        # Create custom colormap for main grid
        cmap = ListedColormap(self.color_list)
        
        # Plot main grid with enhanced styling
        im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
        
        # Add risk map overlay if requested
        if show_risk and risk_map is not None and np.any(risk_map > 0):
            # Create masked array to show only cells with risk > 0
            risk_overlay = np.ma.masked_where(risk_map <= 0.01, risk_map)
            ax.imshow(risk_overlay, cmap=self.risk_cmap, alpha=0.4, vmin=0, vmax=1)
        
        # Add infection trails overlay if provided
        if trails is not None and np.any(trails > 0):
            trail_overlay = np.ma.masked_where(trails <= 0, trails)
            ax.imshow(trail_overlay, cmap=self.trail_cmap, alpha=0.2)
        
        # Enhanced title and styling
        ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Remove axes spines for cleaner look
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Enhanced colorbar with better positioning and labels
        cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.02, aspect=30)
        cbar.set_ticks([0, 1, 2, 3])
        cbar.set_ticklabels(['🟢 Healthy', '🟠 Infected', '🔵 Immune', '⚫ Dead'])
        cbar.ax.tick_params(labelsize=12)
        
        # Add grid statistics as subtitle
        total_cells = grid.size
        unique, counts = np.unique(grid, return_counts=True)
        stats_dict = {state: 0 for state in range(4)}
        for state, count in zip(unique, counts):
            stats_dict[state] = count
            
        stats_text = f"H:{stats_dict[0]} I:{stats_dict[1]} R:{stats_dict[2]} D:{stats_dict[3]}"
        ax.text(0.5, -0.05, stats_text, transform=ax.transAxes, 
                ha='center', va='top', fontsize=10, alpha=0.7)
        
        plt.tight_layout()
        return fig
        
    def plot_population_stats(self, history, show_derivatives=False):
        """Enhanced population statistics plot with additional insights"""
        if len(history) < 2:
            return None
            
        # Extract data arrays
        steps = np.array([h['step'] for h in history])
        healthy = np.array([h['healthy'] for h in history])
        infected = np.array([h['infected'] for h in history])
        immune = np.array([h['immune'] for h in history])
        dead = np.array([h['dead'] for h in history])
        
        # Create subplots for different views
        if show_derivatives and len(history) > 10:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), **self.figure_style)
        else:
            fig, ax1 = plt.subplots(figsize=(12, 6), **self.figure_style)
        
        # Main population plot with enhanced styling
        ax1.plot(steps, healthy, color=self.colors[0], linewidth=3, label='Healthy', alpha=0.8)
        ax1.plot(steps, infected, color=self.colors[1], linewidth=3, label='Infected', alpha=0.8)
        ax1.plot(steps, immune, color=self.colors[2], linewidth=3, label='Immune', alpha=0.8)
        ax1.plot(steps, dead, color=self.colors[3], linewidth=3, label='Dead', alpha=0.8)
        
        # Fill areas for better visual impact
        ax1.fill_between(steps, 0, healthy, color=self.colors[0], alpha=0.2)
        ax1.fill_between(steps, 0, infected, color=self.colors[1], alpha=0.2)
        ax1.fill_between(steps, 0, immune, color=self.colors[2], alpha=0.2)
        ax1.fill_between(steps, 0, dead, color=self.colors[3], alpha=0.2)
        
        ax1.set_xlabel('Time Steps', fontsize=12)
        ax1.set_ylabel('Population Count', fontsize=12)
        ax1.set_title('Population Dynamics Over Time', fontsize=16, fontweight='bold')
        ax1.legend(loc='upper right', frameon=True, shadow=True)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Add peak infection marker
        peak_idx = np.argmax(infected)
        if infected[peak_idx] > 0:
            ax1.annotate(f'Peak: {infected[peak_idx]}', 
                        xy=(steps[peak_idx], infected[peak_idx]),
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        # Derivative plot (rates of change) if requested
        if show_derivatives and len(history) > 10:
            # Calculate rates of change
            d_infected = np.gradient(infected)
            d_dead = np.gradient(dead)
            d_immune = np.gradient(immune)
            
            ax2.plot(steps, d_infected, color=self.colors[1], linewidth=2, 
                    label='Infection Rate', alpha=0.8)
            ax2.plot(steps, d_dead, color=self.colors[3], linewidth=2, 
                    label='Death Rate', alpha=0.8)
            ax2.plot(steps, d_immune, color=self.colors[2], linewidth=2, 
                    label='Recovery Rate', alpha=0.8)
            
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax2.set_xlabel('Time Steps', fontsize=12)
            ax2.set_ylabel('Rate of Change', fontsize=12)
            ax2.set_title('Population Change Rates', fontsize=14, fontweight='bold')
            ax2.legend(loc='upper right', frameon=True, shadow=True)
            ax2.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        return fig
        
    def create_stats_display(self, stats):
        """Enhanced statistics display with comprehensive metrics"""
        total_pop = sum([stats['healthy'], stats['infected'], stats['immune'], stats['dead']])
        
        # Main population metrics with enhanced styling
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pct = stats['healthy']/total_pop*100 if total_pop > 0 else 0
            delta = None
            if pct < 50:
                delta = "Low"
            elif pct > 80:
                delta = "High"
            st.metric("🟢 Healthy", stats['healthy'], f"{pct:.1f}%")
            
        with col2:
            pct = stats['infected']/total_pop*100 if total_pop > 0 else 0
            delta_color = "normal"
            if pct > 20:
                delta_color = "inverse"
            st.metric("🟠 Infected", stats['infected'], f"{pct:.1f}%")
            
        with col3:
            pct = stats['immune']/total_pop*100 if total_pop > 0 else 0
            st.metric("🔵 Immune", stats['immune'], f"{pct:.1f}%")
            
        with col4:
            pct = stats['dead']/total_pop*100 if total_pop > 0 else 0
            st.metric("⚫ Dead", stats['dead'], f"{pct:.1f}%")
            
        # Enhanced additional statistics
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📈 Peak Infected", stats.get('peak_infected', 0))
        with col2:
            st.metric("🦠 Total Ever Infected", stats.get('total_ever_infected', 0))
        with col3:
            st.metric("⏱️ Time Steps", stats.get('step', 0))
            
        # Advanced statistics if available
        if 'transmission_rate' in stats:
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                transmission_rate = stats.get('transmission_rate', 0)
                st.metric("📊 Transmission Rate", f"{transmission_rate:.3f}")
            with col2:
                mortality_rate = stats.get('mortality_rate', 0) * 100
                st.metric("💀 Mortality Rate", f"{mortality_rate:.1f}%")
            with col3:
                recovery_rate = stats.get('recovery_rate', 0) * 100
                st.metric("🛡️ Recovery Rate", f"{recovery_rate:.1f}%")
                
    def display_achievements(self, achievements):
        """Enhanced achievement display with descriptions and icons"""
        if not achievements:
            return
            
        achievement_descriptions = {
            "Patient Zero": ("🦠", "First outbreak initiated", "Started the simulation"),
            "Rapid Spread": ("⚡", "25% infected in 10 steps", "Lightning-fast transmission"),
            "Pandemic": ("🌍", "80% peak infection rate", "Global outbreak achieved"),
            "Survivor": ("🛡️", "50% survived 100+ steps", "Population resilience"),
            "Extinction Event": ("💀", "Total population extinction", "Complete system collapse"),
            "Herd Immunity": ("🏥", "Stable immune population", "Natural disease control"),
            "Containment Master": ("🔒", "Kept infections under 20%", "Excellent outbreak control"),
            "Endemic State": ("🔄", "Stable low-level infection", "Disease became endemic"),
            "Ghost Town": ("👻", "90%+ mortality rate", "Devastating outbreak")
        }
        
        st.markdown("**🏆 Achievements Unlocked:**")
        
        # Group achievements by type for better organization
        for achievement in sorted(achievements):
            if achievement in achievement_descriptions:
                icon, title, description = achievement_descriptions[achievement]
                st.markdown(f"**{icon} {achievement}**")
                st.caption(f"*{title}* - {description}")
                st.markdown("---")
                
    def create_summary_dashboard(self, stats, history):
        """Create a comprehensive dashboard summary"""
        st.subheader("📋 Simulation Summary")
        
        total_pop = sum([stats['healthy'], stats['infected'], stats['immune'], stats['dead']])
        
        # Key metrics in a clean layout
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            survival_rate = stats['healthy'] / total_pop * 100 if total_pop > 0 else 0
            st.metric("🎯 Survival Rate", f"{survival_rate:.1f}%")
            
        with metric_col2:
            if stats.get('total_ever_infected', 0) > 0:
                fatality_rate = stats['dead'] / stats['total_ever_infected'] * 100
            else:
                fatality_rate = 0
            st.metric("💀 Case Fatality Rate", f"{fatality_rate:.1f}%")
            
        with metric_col3:
            peak_pct = stats['peak_infected'] / total_pop * 100 if total_pop > 0 else 0
            st.metric("📊 Peak Infection", f"{peak_pct:.1f}%")
            
        with metric_col4:
            immunity_pct = stats['immune'] / total_pop * 100 if total_pop > 0 else 0
            st.metric("🛡️ Immunity Level", f"{immunity_pct:.1f}%")
        
        # Outcome assessment
        st.divider()
        outcome = self._assess_outcome(stats, total_pop)
        if outcome['type'] == 'success':
            st.success(f"**Outcome:** {outcome['message']}")
        elif outcome['type'] == 'warning':
            st.warning(f"**Outcome:** {outcome['message']}")
        else:
            st.error(f"**Outcome:** {outcome['message']}")
            
    def _assess_outcome(self, stats, total_pop):
        """Assess the overall outcome of the simulation"""
        survival_rate = stats['healthy'] / total_pop if total_pop > 0 else 0
        mortality_rate = stats['dead'] / total_pop if total_pop > 0 else 0
        immunity_rate = stats['immune'] / total_pop if total_pop > 0 else 0
        
        if mortality_rate >= 0.9:
            return {'type': 'error', 'message': 'Catastrophic - Near total extinction'}
        elif mortality_rate >= 0.5:
            return {'type': 'error', 'message': 'Devastating - High mortality outbreak'}
        elif survival_rate >= 0.7:
            return {'type': 'success', 'message': 'Excellent - Population well protected'}
        elif immunity_rate >= 0.3 and stats['infected'] == 0:
            return {'type': 'success', 'message': 'Good - Herd immunity achieved'}
        elif stats['infected'] == 0 and stats['step'] > 10:
            return {'type': 'success', 'message': 'Contained - Outbreak successfully stopped'}
        else:
            return {'type': 'warning', 'message': 'Moderate - Mixed outcomes'}
            
    def plot_phase_diagram(self, history):
        """Create a phase diagram showing the relationship between different populations"""
        if len(history) < 10:
            return None
            
        infected = np.array([h['infected'] for h in history])
        susceptible = np.array([h['healthy'] for h in history])
        
        fig, ax = plt.subplots(figsize=(8, 6), **self.figure_style)
        
        # Create phase plot
        scatter = ax.scatter(susceptible, infected, c=range(len(infected)), 
                           cmap='viridis', alpha=0.7, s=30)
        
        # Add arrow to show direction of evolution
        for i in range(len(infected)-1):
            dx = susceptible[i+1] - susceptible[i]
            dy = infected[i+1] - infected[i]
            if abs(dx) > 1 or abs(dy) > 1:  # Only show significant changes
                ax.arrow(susceptible[i], infected[i], dx*0.8, dy*0.8,
                        head_width=max(susceptible)*0.02, head_length=max(infected)*0.02,
                        fc='red', ec='red', alpha=0.6)
        
        ax.set_xlabel('Susceptible Population', fontsize=12)
        ax.set_ylabel('Infected Population', fontsize=12)
        ax.set_title('Phase Diagram: Susceptible vs Infected', fontsize=14, fontweight='bold')
        
        # Add colorbar for time
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Time Step', fontsize=10)
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig