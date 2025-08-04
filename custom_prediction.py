#!/usr/bin/env python3
"""
Custom Earthquake Risk Prediction for Any Location
"""

from advanced_earthquake_predictor import AdvancedEarthquakePredictor

def predict_location(location_name, lat, lon, magnitude=6.0, depth=15):
    """Predict earthquake risk for a custom location"""

    predictor = AdvancedEarthquakePredictor()

    print(f"\n🌍 EARTHQUAKE RISK PREDICTION")
    print(f"📍 Location: {location_name}")
    print(f"⏰ Prediction Timeframes: Multiple scales")
    print("="*60)

    # Get volcanic influence
    volcanic_risk, volcano_dist, active_nearby = predictor.calculate_volcanic_influence(lat, lon)

    # Get plate information
    plate_stress, movement_rate, boundary_type = predictor.predict_plate_movement(lat, lon)
    plate_dist, plate_name, _, plate_activity = predictor.calculate_plate_boundary_distance(lat, lon)

    # Display results
    print(f"🌋 VOLCANIC ANALYSIS:")
    print(f"   Volcanic Risk Index: {volcanic_risk:.2f}")
    print(f"   Nearest Volcano: {volcano_dist:.1f} km away")
    print(f"   Active Volcanoes Nearby: {active_nearby}")

    print(f"\n🌍 TECTONIC ANALYSIS:")
    print(f"   Nearest Plate: {plate_name}")
    print(f"   Plate Distance: {plate_dist:.1f} km")
    print(f"   Boundary Type: {boundary_type}")
    print(f"   Movement Rate: {movement_rate:.1f} cm/year")
    print(f"   Tectonic Stress: {plate_stress:.2f}")

    # Overall risk assessment
    risk_score, risk_level = predictor.enhanced_risk_assessment(lat, lon, magnitude, depth)

    # Display prediction timeframes
    print(f"\n⏰ PREDICTION TIMEFRAMES:")
    print(f"   🔹 Short-term (1-30 days): Statistical probability based on current conditions")
    print(f"   🔹 Medium-term (1-10 years): Tectonic stress accumulation patterns")
    print(f"   🔹 Long-term (10-100 years): Plate movement and geological evolution")
    print(f"   🔹 Very long-term (100+ years): Major geological changes and supervolcano cycles")

    # Current risk interpretation
    if risk_level in ["VERY HIGH", "HIGH"]:
        timeframe = "Elevated risk in short to medium term (months to years)"
    elif risk_level == "MODERATE":
        timeframe = "Moderate risk over medium term (years to decades)"
    else:
        timeframe = "Lower probability over all timeframes"

    print(f"\n📊 CURRENT RISK INTERPRETATION:")
    print(f"   {timeframe}")

    return risk_score, risk_level

if __name__ == "__main__":
    # Example predictions for different locations
    locations = [
        ("Mexico City, Mexico", 19.4326, -99.1332),
        ("Naples, Italy", 40.8518, 14.2681),  # Near Vesuvius
        ("Seattle, Washington", 47.6062, -122.3321),
        ("Manila, Philippines", 14.5995, 120.9842),  # Ring of Fire
        ("Your Custom Location", 0.0, 0.0)  # Replace with your coordinates
    ]

    for name, lat, lon in locations[:-1]:  # Skip the custom placeholder
        predict_location(name, lat, lon)
        print("\n" + "="*60)
