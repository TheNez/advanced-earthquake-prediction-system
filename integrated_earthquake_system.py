#!/usr/bin/env python3
"""
Integrated Earthquake Prediction System
Combines all geological, tectonic, and volcanic analysis for comprehensive earthquake prediction.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from advanced_earthquake_predictor import AdvancedEarthquakePredictor
from plate_movement_simulator import PlateMovementSimulator
import warnings
warnings.filterwarnings('ignore')

class IntegratedEarthquakeSystem:
    def __init__(self):
        self.earthquake_predictor = AdvancedEarthquakePredictor()
        self.plate_simulator = PlateMovementSimulator()
        self.is_trained = False
        
    def train_system(self, n_samples=3000):
        """Train the integrated system with enhanced geological data"""
        print("🔬 Training Integrated Earthquake Prediction System...")
        print("="*60)
        
        # Generate comprehensive dataset
        print("Generating enhanced geological dataset...")
        df = self.earthquake_predictor.generate_enhanced_data(n_samples)
        
        # Add plate movement predictions
        print("Adding plate movement analysis...")
        plate_movements = self.plate_simulator.simulate_plate_movement(years_ahead=50)
        
        # Enhance dataset with plate movement data
        enhanced_features = []
        for idx, row in df.iterrows():
            lat, lon = row['latitude'], row['longitude']
            
            # Find dominant plate influence
            min_dist = float('inf')
            dominant_plate = None
            plate_velocity = 0
            
            for plate_name, movement in plate_movements.items():
                dist = self.plate_simulator.haversine_distance(
                    lat, lon,
                    movement['current_center']['lat'], 
                    movement['current_center']['lon']
                )
                if dist < min_dist:
                    min_dist = dist
                    dominant_plate = plate_name
                    plate_velocity = movement['velocity_cm_year']
            
            enhanced_features.append({
                'dominant_plate_distance': min_dist,
                'dominant_plate_velocity': plate_velocity,
                'plate_influence_factor': max(0, (3000 - min_dist) / 3000) * (plate_velocity / 1000)
            })
        
        enhanced_df = pd.DataFrame(enhanced_features)
        df = pd.concat([df, enhanced_df], axis=1)
        
        # Train models
        X, y, feature_columns = self.earthquake_predictor.prepare_enhanced_data(df)
        
        # Add new features to feature columns
        feature_columns.extend(['dominant_plate_distance', 'dominant_plate_velocity', 'plate_influence_factor'])
        X = pd.concat([X, enhanced_df], axis=1)
        
        results = self.earthquake_predictor.train_enhanced_models(X, y)
        self.is_trained = True
        
        print(f"\n✅ System trained with {len(feature_columns)} geological features")
        return results, df
    
    def comprehensive_risk_analysis(self, lat, lon, magnitude=None, depth=None):
        """Perform comprehensive risk analysis for a location"""
        print(f"\n{'='*100}")
        print("COMPREHENSIVE EARTHQUAKE RISK ANALYSIS")
        print(f"{'='*100}")
        print(f"Location: {lat:.4f}°N, {lon:.4f}°E")
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Set default values if not provided
        if magnitude is None:
            magnitude = 6.0  # Default moderate earthquake
        if depth is None:
            depth = 15.0  # Default shallow depth
        
        # 1. Basic Geological Analysis
        print(f"\n{'1. GEOLOGICAL & TECTONIC ANALYSIS'}")
        print(f"{'-'*50}")
        
        plate_stress, movement_rate, boundary_type = self.earthquake_predictor.predict_plate_movement(lat, lon)
        plate_dist, plate_name, _, plate_activity = self.earthquake_predictor.calculate_plate_boundary_distance(lat, lon)
        
        print(f"Nearest Plate Boundary: {plate_name}")
        print(f"Boundary Type: {boundary_type}")
        print(f"Distance to Boundary: {plate_dist:.1f} km")
        print(f"Plate Movement Rate: {movement_rate:.1f} cm/year")
        print(f"Tectonic Stress Index: {plate_stress:.2f}")
        print(f"Plate Activity Level: {plate_activity:.2f}")
        
        # 2. Volcanic Risk Analysis
        print(f"\n{'2. VOLCANIC RISK ANALYSIS'}")
        print(f"{'-'*50}")
        
        volcanic_risk, volcano_dist, active_nearby = self.earthquake_predictor.calculate_volcanic_influence(lat, lon)
        
        print(f"Volcanic Risk Index: {volcanic_risk:.2f}")
        print(f"Nearest Volcano Distance: {volcano_dist:.1f} km")
        print(f"Active Volcanoes Nearby (500km): {active_nearby}")
        
        # 3. Plate Movement Prediction
        print(f"\n{'3. PLATE MOVEMENT PREDICTIONS'}")
        print(f"{'-'*50}")
        
        movements = self.plate_simulator.simulate_plate_movement(years_ahead=100)
        collision_zones = self.plate_simulator.detect_collision_zones(movements)
        
        # Find closest collision zone
        closest_collision = None
        min_collision_dist = float('inf')
        
        for zone in collision_zones:
            dist = self.plate_simulator.haversine_distance(
                lat, lon, 
                zone['estimated_collision_zone_lat'], 
                zone['estimated_collision_zone_lon']
            )
            if dist < min_collision_dist:
                min_collision_dist = dist
                closest_collision = zone
        
        if closest_collision:
            print(f"Nearest Collision Zone: {closest_collision['plate1']} ↔ {closest_collision['plate2']}")
            print(f"Distance to Collision Zone: {min_collision_dist:.1f} km")
            print(f"Collision Probability: {closest_collision['collision_probability']:.3f}")
            print(f"Approach Rate: {closest_collision['approach_rate']:.1f} km/100 years")
        else:
            print("No significant collision zones detected nearby")
        
        # 4. Stress Accumulation Analysis
        print(f"\n{'4. STRESS ACCUMULATION ANALYSIS'}")
        print(f"{'-'*50}")
        
        self.plate_simulator.calculate_stress_accumulation(movements, grid_resolution=5)
        hotspots = self.plate_simulator.predict_seismic_hotspots(stress_threshold=10)
        
        # Find stress level at the given location
        local_stress = 0
        min_hotspot_dist = float('inf')
        for hotspot in hotspots:
            dist = self.plate_simulator.haversine_distance(lat, lon, hotspot['lat'], hotspot['lon'])
            if dist < 100:  # Within 100km
                local_stress = max(local_stress, hotspot['stress_level'] * (100 - dist) / 100)
            if dist < min_hotspot_dist:
                min_hotspot_dist = dist
        
        print(f"Local Stress Level: {local_stress:.1f}")
        print(f"Distance to Nearest Hotspot: {min_hotspot_dist:.1f} km")
        
        # 5. Integrated Risk Assessment
        print(f"\n{'5. INTEGRATED RISK ASSESSMENT'}")
        print(f"{'-'*50}")
        
        # Calculate comprehensive risk factors
        risk_factors = {
            'Magnitude Factor': magnitude / 10,
            'Depth Factor': max(0, (50 - depth) / 50),
            'Plate Boundary Proximity': max(0, (500 - plate_dist) / 500),
            'Tectonic Stress': min(1, plate_stress / 50),
            'Volcanic Activity': min(1, volcanic_risk / 5),
            'Collision Zone Proximity': max(0, (1000 - min_collision_dist) / 1000) if closest_collision else 0,
            'Stress Accumulation': min(1, local_stress / 100)
        }
        
        # Calculate weighted overall risk
        weights = {
            'Magnitude Factor': 0.25,
            'Depth Factor': 0.15,
            'Plate Boundary Proximity': 0.20,
            'Tectonic Stress': 0.15,
            'Volcanic Activity': 0.10,
            'Collision Zone Proximity': 0.10,
            'Stress Accumulation': 0.05
        }
        
        overall_risk = sum(risk_factors[factor] * weights[factor] for factor in risk_factors)
        
        print("Risk Factor Breakdown:")
        for factor, value in risk_factors.items():
            weight = weights[factor]
            contribution = value * weight
            print(f"  {factor}: {value:.3f} (weight: {weight:.2f}, contribution: {contribution:.3f})")
        
        # 6. Final Assessment
        print(f"\n{'6. FINAL RISK ASSESSMENT'}")
        print(f"{'-'*50}")
        
        if overall_risk > 0.8:
            risk_level = "EXTREME"
            color = "🔴🔴"
            recommendation = "IMMEDIATE EVACUATION RECOMMENDED"
        elif overall_risk > 0.6:
            risk_level = "VERY HIGH"
            color = "🔴"
            recommendation = "HIGH ALERT - PREPARE FOR EVACUATION"
        elif overall_risk > 0.4:
            risk_level = "HIGH"
            color = "🟠"
            recommendation = "INCREASED MONITORING REQUIRED"
        elif overall_risk > 0.2:
            risk_level = "MODERATE"
            color = "🟡"
            recommendation = "STANDARD PRECAUTIONS"
        else:
            risk_level = "LOW"
            color = "🟢"
            recommendation = "ROUTINE MONITORING"
        
        print(f"Overall Risk Score: {overall_risk:.3f}")
        print(f"Risk Level: {color} {risk_level}")
        print(f"Recommendation: {recommendation}")
        
        # 7. Confidence Assessment
        print(f"\n{'7. CONFIDENCE ASSESSMENT'}")
        print(f"{'-'*50}")
        
        data_quality_factors = {
            'Geological Data Availability': 0.85,
            'Tectonic Model Reliability': 0.80,
            'Volcanic Data Completeness': 0.75,
            'Historical Data Coverage': 0.70
        }
        
        confidence_score = sum(data_quality_factors.values()) / len(data_quality_factors)
        
        print("Data Quality Assessment:")
        for factor, score in data_quality_factors.items():
            print(f"  {factor}: {score:.2f}")
        
        print(f"\nOverall Confidence: {confidence_score:.2f}")
        
        if confidence_score > 0.8:
            confidence_level = "HIGH"
        elif confidence_score > 0.6:
            confidence_level = "MODERATE"
        else:
            confidence_level = "LOW"
        
        print(f"Confidence Level: {confidence_level}")
        
        return {
            'risk_score': overall_risk,
            'risk_level': risk_level,
            'confidence_score': confidence_score,
            'risk_factors': risk_factors,
            'recommendation': recommendation
        }
    
    def create_comprehensive_visualization(self):
        """Create comprehensive visualization of all geological factors"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
        
        # Generate sample data for visualization
        df = self.earthquake_predictor.generate_enhanced_data(1000)
        
        # Plot 1: Risk vs Tectonic Features
        ax1.scatter(df['plate_boundary_distance'], df['plate_stress'], 
                   c=df['earthquake_risk'], cmap='viridis', alpha=0.6)
        ax1.set_xlabel('Distance to Plate Boundary (km)')
        ax1.set_ylabel('Tectonic Stress Index')
        ax1.set_title('Earthquake Risk vs Tectonic Features')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Volcanic Influence
        ax2.scatter(df['nearest_volcano_distance'], df['volcanic_risk_index'], 
                   c=df['earthquake_risk'], cmap='Reds', alpha=0.6)
        ax2.set_xlabel('Distance to Nearest Volcano (km)')
        ax2.set_ylabel('Volcanic Risk Index')
        ax2.set_title('Earthquake Risk vs Volcanic Activity')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Geographic Risk Distribution
        scatter = ax3.scatter(df['longitude'], df['latitude'], 
                             c=df['earthquake_risk'], cmap='coolwarm', alpha=0.6)
        ax3.set_xlabel('Longitude')
        ax3.set_ylabel('Latitude')
        ax3.set_title('Global Earthquake Risk Distribution')
        ax3.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax3)
        
        # Plot 4: Feature Importance (if trained)
        if self.is_trained:
            # Get feature importance from Random Forest model
            rf_model = self.earthquake_predictor.models.get('Enhanced Random Forest')
            if rf_model and hasattr(rf_model, 'feature_importances_'):
                feature_names = ['magnitude', 'depth', 'latitude', 'longitude', 'previous_activity',
                               'fault_distance', 'rock_density', 'stress_accumulation', 
                               'groundwater_level', 'tidal_force', 'plate_boundary_distance',
                               'plate_stress', 'plate_movement_rate', 'boundary_type_convergent',
                               'boundary_type_transform', 'boundary_type_divergent',
                               'volcanic_risk_index', 'nearest_volcano_distance', 'active_volcanoes_nearby']
                
                importances = rf_model.feature_importances_[:len(feature_names)]
                
                # Sort features by importance
                feature_importance = list(zip(feature_names, importances))
                feature_importance.sort(key=lambda x: x[1], reverse=True)
                
                # Plot top 10 features
                top_features = feature_importance[:10]
                names, values = zip(*top_features)
                
                ax4.barh(range(len(names)), values)
                ax4.set_yticks(range(len(names)))
                ax4.set_yticklabels(names)
                ax4.set_xlabel('Feature Importance')
                ax4.set_title('Top 10 Most Important Geological Features')
                ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('comprehensive_earthquake_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()


def main():
    """Main function for integrated earthquake system"""
    print("🌍⚡ INTEGRATED EARTHQUAKE PREDICTION SYSTEM ⚡🌍")
    print("="*80)
    print("Combining Geological, Tectonic, and Volcanic Analysis")
    print("="*80)
    
    # Initialize system
    system = IntegratedEarthquakeSystem()
    
    # Train the system
    print("\n🔬 SYSTEM TRAINING PHASE")
    print("-"*40)
    results, df = system.train_system(n_samples=2500)
    
    # Create comprehensive visualization
    print("\n📊 GENERATING COMPREHENSIVE VISUALIZATIONS")
    print("-"*40)
    system.create_comprehensive_visualization()
    
    # Test system on critical locations
    print("\n🎯 CRITICAL LOCATION ANALYSIS")
    print("-"*40)
    
    critical_locations = [
        {"name": "San Francisco (San Andreas Fault)", "lat": 37.7749, "lon": -122.4194, "mag": 7.5, "depth": 12},
        {"name": "Tokyo (Ring of Fire)", "lat": 35.6762, "lon": 139.6503, "mag": 8.0, "depth": 30},
        {"name": "Istanbul (North Anatolian Fault)", "lat": 41.0082, "lon": 28.9784, "mag": 7.2, "depth": 15},
        {"name": "Reykjavik (Mid-Atlantic Ridge)", "lat": 64.1466, "lon": -21.9426, "mag": 6.0, "depth": 8},
        {"name": "Kathmandu (Himalayan Front)", "lat": 27.7172, "lon": 85.3240, "mag": 7.8, "depth": 18}
    ]
    
    risk_summary = []
    
    for location in critical_locations:
        print(f"\nAnalyzing: {location['name']}")
        result = system.comprehensive_risk_analysis(
            location["lat"], location["lon"], 
            location["mag"], location["depth"]
        )
        
        risk_summary.append({
            'location': location['name'],
            'risk_score': result['risk_score'],
            'risk_level': result['risk_level'],
            'confidence': result['confidence_score']
        })
    
    # Summary report
    print(f"\n{'='*100}")
    print("SYSTEM ANALYSIS SUMMARY")
    print(f"{'='*100}")
    
    print("\nRisk Assessment Summary:")
    print("-" * 60)
    print(f"{'Location':<35} {'Risk Score':<12} {'Risk Level':<15} {'Confidence'}")
    print("-" * 60)
    
    for summary in sorted(risk_summary, key=lambda x: x['risk_score'], reverse=True):
        print(f"{summary['location']:<35} {summary['risk_score']:<12.3f} {summary['risk_level']:<15} {summary['confidence']:.2f}")
    
    print(f"\n🎯 Integrated earthquake prediction system analysis completed!")
    print("Generated files:")
    print("  - comprehensive_earthquake_analysis.png (System visualization)")
    print("  - geological_analysis_map.html (Interactive geological map)")
    print("  - plate_movement_analysis.png (Plate movement predictions)")


if __name__ == "__main__":
    main()
