#!/usr/bin/env python3
"""
Interactive Earthquake Risk Assessment Tool
Allows users to input custom parameters for earthquake risk prediction.
"""

import numpy as np
from earthquake_predictor import EarthquakePredictor

def get_user_input():
    """Get earthquake parameters from user input"""
    print("\n🌍 Interactive Earthquake Risk Assessment")
    print("=========================================")
    print("Please enter the following parameters:\n")
    
    try:
        magnitude = float(input("Magnitude (0.0-10.0): "))
        depth = float(input("Depth in km (0-700): "))
        latitude = float(input("Latitude (-90 to 90): "))
        longitude = float(input("Longitude (-180 to 180): "))
        previous_activity = int(input("Previous earthquake activity count (0-20): "))
        fault_distance = float(input("Distance to nearest fault in km (0-500): "))
        rock_density = float(input("Rock density g/cm³ (1.0-5.0): "))
        stress_accumulation = float(input("Stress accumulation level (0-50): "))
        groundwater_level = float(input("Groundwater level in meters (0-200): "))
        tidal_force = float(input("Tidal force influence (-1.0 to 1.0): "))
        
        return np.array([magnitude, depth, latitude, longitude, previous_activity,
                        fault_distance, rock_density, stress_accumulation, 
                        groundwater_level, tidal_force])
    
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return None

def main():
    """Main interactive function"""
    # Initialize and train the predictor with synthetic data
    predictor = EarthquakePredictor()
    print("Training earthquake prediction models...")
    
    # Generate training data
    df = predictor.generate_synthetic_data(1000)
    X, y = predictor.prepare_data(df)
    predictor.train_models(X, y)
    
    print("✅ Models trained successfully!\n")
    
    while True:
        # Get user input
        features = get_user_input()
        
        if features is not None:
            # Generate risk report
            predictor.create_risk_report(features)
            
            # Ask if user wants to continue
            continue_choice = input("\nWould you like to assess another location? (y/n): ").lower()
            if continue_choice != 'y':
                break
        else:
            retry = input("Would you like to try again? (y/n): ").lower()
            if retry != 'y':
                break
    
    print("\n👋 Thank you for using the Earthquake Risk Assessment Tool!")

if __name__ == "__main__":
    main()
