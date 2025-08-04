#!/usr/bin/env python3
"""
Tectonic Plate Movement Simulator
Simulates and predicts tectonic plate movements and their effects on seismic activity.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.spatial.distance import cdist
from scipy.interpolate import griddata
import warnings
warnings.filterwarnings('ignore')

class PlateMovementSimulator:
    def __init__(self):
        self.plates = self.initialize_plates()
        self.stress_grid = None
        self.collision_zones = []
        
    def initialize_plates(self):
        """Initialize major tectonic plates with movement vectors"""
        plates = {
            'Pacific': {
                'center': {'lat': 0, 'lon': -150},
                'velocity': {'lat': 0.02, 'lon': 0.05},  # degrees per year
                'area': 103300000,  # km²
                'thickness': 70,  # km
                'density': 2.9,  # g/cm³
                'age': 180,  # million years
                'boundaries': [
                    {'lat': 60, 'lon': -140, 'type': 'transform'},
                    {'lat': 40, 'lon': -125, 'type': 'transform'},
                    {'lat': 20, 'lon': -105, 'type': 'divergent'},
                    {'lat': -20, 'lon': -70, 'type': 'convergent'},
                    {'lat': -40, 'lon': -75, 'type': 'transform'}
                ]
            },
            'North_American': {
                'center': {'lat': 45, 'lon': -100},
                'velocity': {'lat': -0.01, 'lon': -0.02},
                'area': 75900000,
                'thickness': 40,
                'density': 2.7,
                'age': 200,
                'boundaries': [
                    {'lat': 60, 'lon': -140, 'type': 'transform'},
                    {'lat': 40, 'lon': -125, 'type': 'transform'},
                    {'lat': 30, 'lon': -85, 'type': 'divergent'}
                ]
            },
            'Eurasian': {
                'center': {'lat': 55, 'lon': 100},
                'velocity': {'lat': 0.01, 'lon': 0.03},
                'area': 67800000,
                'thickness': 35,
                'density': 2.7,
                'age': 250,
                'boundaries': [
                    {'lat': 70, 'lon': -10, 'type': 'divergent'},
                    {'lat': 35, 'lon': 70, 'type': 'convergent'},
                    {'lat': 28, 'lon': 85, 'type': 'convergent'}
                ]
            },
            'Indo_Australian': {
                'center': {'lat': -25, 'lon': 135},
                'velocity': {'lat': 0.04, 'lon': 0.06},
                'area': 58900000,
                'thickness': 50,
                'density': 2.8,
                'age': 130,
                'boundaries': [
                    {'lat': 28, 'lon': 85, 'type': 'convergent'},
                    {'lat': 0, 'lon': 90, 'type': 'divergent'},
                    {'lat': -20, 'lon': 110, 'type': 'transform'}
                ]
            }
        }
        return plates
    
    def simulate_plate_movement(self, years_ahead=100):
        """Simulate plate movements over time"""
        movements = {}
        
        for plate_name, plate_data in self.plates.items():
            current_center = plate_data['center'].copy()
            velocity = plate_data['velocity']
            
            # Calculate future position
            future_lat = current_center['lat'] + (velocity['lat'] * years_ahead)
            future_lon = current_center['lon'] + (velocity['lon'] * years_ahead)
            
            # Calculate movement distance
            movement_distance = np.sqrt(
                (velocity['lat'] * years_ahead * 111) ** 2 + 
                (velocity['lon'] * years_ahead * 111 * np.cos(np.radians(current_center['lat']))) ** 2
            )
            
            movements[plate_name] = {
                'current_center': current_center,
                'future_center': {'lat': future_lat, 'lon': future_lon},
                'movement_distance_km': movement_distance,
                'velocity_cm_year': movement_distance * 100000 / years_ahead,
                'direction': np.degrees(np.arctan2(velocity['lat'], velocity['lon']))
            }
        
        return movements
    
    def detect_collision_zones(self, movements):
        """Detect potential collision zones between plates"""
        collision_zones = []
        plate_names = list(movements.keys())
        
        for i, plate1 in enumerate(plate_names):
            for j, plate2 in enumerate(plate_names[i+1:], i+1):
                p1_data = movements[plate1]
                p2_data = movements[plate2]
                
                # Calculate distance between current centers
                current_dist = self.haversine_distance(
                    p1_data['current_center']['lat'], p1_data['current_center']['lon'],
                    p2_data['current_center']['lat'], p2_data['current_center']['lon']
                )
                
                # Calculate distance between future centers
                future_dist = self.haversine_distance(
                    p1_data['future_center']['lat'], p1_data['future_center']['lon'],
                    p2_data['future_center']['lat'], p2_data['future_center']['lon']
                )
                
                # Check if plates are approaching each other
                if future_dist < current_dist:
                    collision_probability = max(0, (current_dist - future_dist) / current_dist)
                    
                    collision_zones.append({
                        'plate1': plate1,
                        'plate2': plate2,
                        'current_distance': current_dist,
                        'future_distance': future_dist,
                        'approach_rate': current_dist - future_dist,
                        'collision_probability': collision_probability,
                        'estimated_collision_zone_lat': (p1_data['future_center']['lat'] + p2_data['future_center']['lat']) / 2,
                        'estimated_collision_zone_lon': (p1_data['future_center']['lon'] + p2_data['future_center']['lon']) / 2
                    })
        
        return sorted(collision_zones, key=lambda x: x['collision_probability'], reverse=True)
    
    def calculate_stress_accumulation(self, movements, grid_resolution=2):
        """Calculate stress accumulation across the globe"""
        # Create global grid
        lats = np.arange(-90, 91, grid_resolution)
        lons = np.arange(-180, 181, grid_resolution)
        lat_grid, lon_grid = np.meshgrid(lats, lons)
        
        stress_grid = np.zeros_like(lat_grid, dtype=float)
        
        for plate_name, movement in movements.items():
            plate_data = self.plates[plate_name]
            
            # Calculate stress contribution from each plate
            for i, lat in enumerate(lats):
                for j, lon in enumerate(lons):
                    # Distance to plate center
                    dist_to_center = self.haversine_distance(
                        lat, lon,
                        movement['current_center']['lat'],
                        movement['current_center']['lon']
                    )
                    
                    # Calculate stress based on plate characteristics
                    velocity_magnitude = movement['velocity_cm_year']
                    plate_thickness = plate_data['thickness']
                    plate_density = plate_data['density']
                    
                    # Stress decreases with distance but increases with velocity and density
                    if dist_to_center < 3000:  # Within 3000km of plate center
                        stress_contribution = (
                            (velocity_magnitude * plate_thickness * plate_density) / 
                            (1 + dist_to_center / 1000)
                        )
                        stress_grid[j, i] += stress_contribution
        
        self.stress_grid = {'lats': lats, 'lons': lons, 'stress': stress_grid}
        return self.stress_grid
    
    def predict_seismic_hotspots(self, stress_threshold=50):
        """Predict seismic hotspots based on stress accumulation"""
        if self.stress_grid is None:
            raise ValueError("Must calculate stress grid first")
        
        hotspots = []
        stress = self.stress_grid['stress']
        lats = self.stress_grid['lats']
        lons = self.stress_grid['lons']
        
        # Find high-stress areas
        high_stress_indices = np.where(stress > stress_threshold)
        
        for i, j in zip(high_stress_indices[0], high_stress_indices[1]):
            if i < len(lons) and j < len(lats):
                hotspots.append({
                    'lat': lats[j],
                    'lon': lons[i],
                    'stress_level': stress[i, j],
                    'risk_category': self.categorize_risk(stress[i, j])
                })
        
        return sorted(hotspots, key=lambda x: x['stress_level'], reverse=True)
    
    def categorize_risk(self, stress_level):
        """Categorize seismic risk based on stress level"""
        if stress_level > 100:
            return 'EXTREME'
        elif stress_level > 75:
            return 'VERY HIGH'
        elif stress_level > 50:
            return 'HIGH'
        elif stress_level > 25:
            return 'MODERATE'
        else:
            return 'LOW'
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points on Earth"""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return R * c
    
    def visualize_plate_movements(self, movements, collision_zones):
        """Visualize plate movements and collision zones"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        # Plot 1: Current vs Future plate positions
        ax1.set_title('Tectonic Plate Movement Prediction (100 years)', fontsize=14, fontweight='bold')
        
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        
        for i, (plate_name, movement) in enumerate(movements.items()):
            color = colors[i % len(colors)]
            
            # Current position
            ax1.scatter(movement['current_center']['lon'], movement['current_center']['lat'], 
                       s=200, c=color, marker='o', label=f'{plate_name} (Current)', alpha=0.7)
            
            # Future position
            ax1.scatter(movement['future_center']['lon'], movement['future_center']['lat'], 
                       s=200, c=color, marker='s', alpha=0.5)
            
            # Movement arrow
            ax1.arrow(movement['current_center']['lon'], movement['current_center']['lat'],
                     movement['future_center']['lon'] - movement['current_center']['lon'],
                     movement['future_center']['lat'] - movement['current_center']['lat'],
                     head_width=5, head_length=3, fc=color, ec=color, alpha=0.6)
        
        # Mark collision zones
        for zone in collision_zones[:3]:  # Top 3 collision zones
            ax1.scatter(zone['estimated_collision_zone_lon'], zone['estimated_collision_zone_lat'],
                       s=300, c='red', marker='X', label=f'Collision Zone ({zone["collision_probability"]:.2f})')
        
        ax1.set_xlabel('Longitude')
        ax1.set_ylabel('Latitude')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(-180, 180)
        ax1.set_ylim(-90, 90)
        
        # Plot 2: Stress accumulation heatmap
        if self.stress_grid is not None:
            ax2.set_title('Global Tectonic Stress Distribution', fontsize=14, fontweight='bold')
            
            lon_mesh, lat_mesh = np.meshgrid(self.stress_grid['lons'], self.stress_grid['lats'])
            
            im = ax2.contourf(lon_mesh, lat_mesh, self.stress_grid['stress'].T, 
                             levels=20, cmap='YlOrRd', alpha=0.8)
            
            # Add plate centers
            for plate_name, movement in movements.items():
                ax2.scatter(movement['current_center']['lon'], movement['current_center']['lat'], 
                           s=100, c='black', marker='o', alpha=0.8)
                ax2.text(movement['current_center']['lon'], movement['current_center']['lat'] + 3, 
                        plate_name, ha='center', fontsize=8, fontweight='bold')
            
            plt.colorbar(im, ax=ax2, label='Stress Level')
            ax2.set_xlabel('Longitude')
            ax2.set_ylabel('Latitude')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('plate_movement_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_comprehensive_report(self, years_ahead=100):
        """Generate comprehensive plate movement analysis report"""
        print(f"\n{'='*80}")
        print("TECTONIC PLATE MOVEMENT ANALYSIS REPORT")
        print(f"{'='*80}")
        print(f"Analysis Period: {years_ahead} years ahead")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Simulate movements
        movements = self.simulate_plate_movement(years_ahead)
        collision_zones = self.detect_collision_zones(movements)
        stress_grid = self.calculate_stress_accumulation(movements)
        hotspots = self.predict_seismic_hotspots()
        
        print(f"\n{'PLATE MOVEMENT PREDICTIONS'}")
        print(f"{'-'*50}")
        
        for plate_name, movement in movements.items():
            print(f"\n{plate_name} Plate:")
            print(f"  Current Position: {movement['current_center']['lat']:.2f}°N, {movement['current_center']['lon']:.2f}°E")
            print(f"  Future Position: {movement['future_center']['lat']:.2f}°N, {movement['future_center']['lon']:.2f}°E")
            print(f"  Movement Distance: {movement['movement_distance_km']:.1f} km")
            print(f"  Movement Rate: {movement['velocity_cm_year']:.1f} cm/year")
            print(f"  Direction: {movement['direction']:.1f}°")
        
        print(f"\n{'COLLISION ZONE ANALYSIS'}")
        print(f"{'-'*50}")
        
        if collision_zones:
            for i, zone in enumerate(collision_zones[:5], 1):
                print(f"\n{i}. {zone['plate1']} ↔ {zone['plate2']}")
                print(f"   Collision Probability: {zone['collision_probability']:.3f}")
                print(f"   Approach Rate: {zone['approach_rate']:.1f} km/{years_ahead} years")
                print(f"   Estimated Zone: {zone['estimated_collision_zone_lat']:.2f}°N, {zone['estimated_collision_zone_lon']:.2f}°E")
        else:
            print("No significant collision zones detected in the analysis period.")
        
        print(f"\n{'SEISMIC HOTSPOT PREDICTIONS'}")
        print(f"{'-'*50}")
        
        for i, hotspot in enumerate(hotspots[:10], 1):
            print(f"{i:2d}. {hotspot['lat']:6.2f}°N, {hotspot['lon']:7.2f}°E - "
                  f"Stress: {hotspot['stress_level']:6.1f} - Risk: {hotspot['risk_category']}")
        
        # Create visualizations
        self.visualize_plate_movements(movements, collision_zones)
        
        print(f"\n{'SUMMARY'}")
        print(f"{'-'*20}")
        print(f"Total Plates Analyzed: {len(movements)}")
        print(f"Collision Zones Identified: {len(collision_zones)}")
        print(f"High-Risk Seismic Hotspots: {len(hotspots)}")
        print(f"Visualization saved as: plate_movement_analysis.png")
        
        return {
            'movements': movements,
            'collision_zones': collision_zones,
            'stress_grid': stress_grid,
            'hotspots': hotspots
        }


def main():
    """Main function for plate movement simulation"""
    print("🌍 Tectonic Plate Movement Simulator")
    print("="*40)
    
    simulator = PlateMovementSimulator()
    
    # Generate comprehensive analysis
    analysis = simulator.generate_comprehensive_report(years_ahead=100)
    
    print(f"\n🎯 Plate movement analysis completed!")
    print("Check 'plate_movement_analysis.png' for visualizations.")


if __name__ == "__main__":
    main()
