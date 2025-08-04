#!/usr/bin/env python3
"""
Advanced Earthquake Prediction System
Incorporates tectonic plate movements, volcanic activity, and comprehensive geological analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from geopy.distance import geodesic
import requests
import json
import warnings
warnings.filterwarnings('ignore')

class AdvancedEarthquakePredictor:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.is_trained = False
        self.tectonic_plates = self.load_tectonic_plate_data()
        self.volcanoes = self.load_volcanic_data()

    def load_tectonic_plate_data(self):
        """
        Load tectonic plate boundary data
        In a real implementation, this would load from geological databases
        """
        # Major tectonic plate boundaries (simplified dataset)
        plates = {
            'Pacific_Ring_of_Fire': {
                'boundaries': [
                    {'lat': 60, 'lon': -140, 'type': 'transform', 'activity': 0.8},
                    {'lat': 40, 'lon': -125, 'type': 'transform', 'activity': 0.9},
                    {'lat': 35, 'lon': -120, 'type': 'transform', 'activity': 0.95},
                    {'lat': 20, 'lon': -105, 'type': 'divergent', 'activity': 0.7},
                    {'lat': 0, 'lon': -90, 'type': 'convergent', 'activity': 0.85},
                    {'lat': -20, 'lon': -70, 'type': 'convergent', 'activity': 0.8},
                    {'lat': -40, 'lon': -75, 'type': 'transform', 'activity': 0.6}
                ],
                'movement_rate': 3.5,  # cm/year
                'direction': 'northwest'
            },
            'Mid_Atlantic_Ridge': {
                'boundaries': [
                    {'lat': 70, 'lon': -10, 'type': 'divergent', 'activity': 0.6},
                    {'lat': 50, 'lon': -30, 'type': 'divergent', 'activity': 0.7},
                    {'lat': 30, 'lon': -40, 'type': 'divergent', 'activity': 0.65},
                    {'lat': 0, 'lon': -25, 'type': 'divergent', 'activity': 0.8},
                    {'lat': -30, 'lon': -15, 'type': 'divergent', 'activity': 0.7},
                    {'lat': -50, 'lon': 0, 'type': 'divergent', 'activity': 0.6}
                ],
                'movement_rate': 2.5,  # cm/year
                'direction': 'spreading'
            },
            'Himalayan_Front': {
                'boundaries': [
                    {'lat': 35, 'lon': 70, 'type': 'convergent', 'activity': 0.9},
                    {'lat': 30, 'lon': 80, 'type': 'convergent', 'activity': 0.95},
                    {'lat': 28, 'lon': 85, 'type': 'convergent', 'activity': 1.0},
                    {'lat': 30, 'lon': 90, 'type': 'convergent', 'activity': 0.9},
                    {'lat': 32, 'lon': 95, 'type': 'convergent', 'activity': 0.85}
                ],
                'movement_rate': 5.0,  # cm/year
                'direction': 'northward'
            }
        }
        return plates

    def load_volcanic_data(self):
        """
        Load comprehensive volcanic activity data including lesser-known but significant volcanoes
        Emphasis on volcanoes near major fault lines and plate boundaries
        """
        volcanoes = [
            # PACIFIC RING OF FIRE - Western Americas
            {'name': 'Mount St. Helens', 'lat': 46.20, 'lon': -122.18, 'elevation': 2549, 'status': 'active', 'last_eruption': 2008, 'vei': 5},
            {'name': 'Mount Rainier', 'lat': 46.85, 'lon': -121.76, 'elevation': 4392, 'status': 'active', 'last_eruption': 1894, 'vei': 4},
            {'name': 'Mount Baker', 'lat': 48.78, 'lon': -121.81, 'elevation': 3286, 'status': 'active', 'last_eruption': 1880, 'vei': 3},
            {'name': 'Mount Shasta', 'lat': 41.41, 'lon': -122.19, 'elevation': 4322, 'status': 'active', 'last_eruption': 1786, 'vei': 4},
            {'name': 'Lassen Peak', 'lat': 40.49, 'lon': -121.51, 'elevation': 3187, 'status': 'active', 'last_eruption': 1917, 'vei': 3},
            {'name': 'Mount Mazama', 'lat': 42.94, 'lon': -122.11, 'elevation': 2487, 'status': 'extinct', 'last_eruption': -5677, 'vei': 7},

            # CALIFORNIA & NEVADA - Near San Andreas Fault
            {'name': 'Mammoth Mountain', 'lat': 37.63, 'lon': -119.03, 'elevation': 3369, 'status': 'active', 'last_eruption': 1260, 'vei': 3},
            {'name': 'Long Valley Caldera', 'lat': 37.70, 'lon': -118.87, 'elevation': 2500, 'status': 'active', 'last_eruption': 1350, 'vei': 6},
            {'name': 'Mono-Inyo Craters', 'lat': 37.88, 'lon': -119.03, 'elevation': 2581, 'status': 'active', 'last_eruption': 1350, 'vei': 3},
            {'name': 'Coso Volcanic Field', 'lat': 36.03, 'lon': -117.82, 'elevation': 2400, 'status': 'active', 'last_eruption': 1040, 'vei': 2},

            # ALASKA - Aleutian Arc
            {'name': 'Mount Redoubt', 'lat': 60.49, 'lon': -152.74, 'elevation': 3108, 'status': 'active', 'last_eruption': 2009, 'vei': 4},
            {'name': 'Mount Cleveland', 'lat': 52.82, 'lon': -169.95, 'elevation': 1730, 'status': 'active', 'last_eruption': 2023, 'vei': 3},
            {'name': 'Katmai', 'lat': 58.28, 'lon': -154.96, 'elevation': 2047, 'status': 'active', 'last_eruption': 1912, 'vei': 6},
            {'name': 'Aniakchak', 'lat': 56.88, 'lon': -158.17, 'elevation': 1341, 'status': 'active', 'last_eruption': 1931, 'vei': 5},

            # HAWAII - Pacific Hotspot
            {'name': 'Kilauea', 'lat': 19.42, 'lon': -155.29, 'elevation': 1247, 'status': 'active', 'last_eruption': 2023, 'vei': 2},
            {'name': 'Mauna Loa', 'lat': 19.48, 'lon': -155.61, 'elevation': 4169, 'status': 'active', 'last_eruption': 2022, 'vei': 2},
            {'name': 'Hualalai', 'lat': 19.69, 'lon': -155.87, 'elevation': 2521, 'status': 'active', 'last_eruption': 1801, 'vei': 2},

            # JAPAN - Pacific Ring of Fire
            {'name': 'Mount Fuji', 'lat': 35.36, 'lon': 138.73, 'elevation': 3776, 'status': 'active', 'last_eruption': 1707, 'vei': 3},
            {'name': 'Sakurajima', 'lat': 31.59, 'lon': 130.66, 'elevation': 1117, 'status': 'active', 'last_eruption': 2024, 'vei': 4},
            {'name': 'Mount Asama', 'lat': 36.40, 'lon': 138.53, 'elevation': 2568, 'status': 'active', 'last_eruption': 2019, 'vei': 3},
            {'name': 'Unzen', 'lat': 32.76, 'lon': 130.30, 'elevation': 1483, 'status': 'active', 'last_eruption': 1996, 'vei': 3},
            {'name': 'Aso', 'lat': 32.88, 'lon': 131.10, 'elevation': 1592, 'status': 'active', 'last_eruption': 2021, 'vei': 4},

            # INDONESIA - Ring of Fire
            {'name': 'Krakatoa', 'lat': -6.10, 'lon': 105.42, 'elevation': 813, 'status': 'active', 'last_eruption': 2020, 'vei': 6},
            {'name': 'Tambora', 'lat': -8.25, 'lon': 118.00, 'elevation': 2722, 'status': 'active', 'last_eruption': 1967, 'vei': 7},
            {'name': 'Merapi', 'lat': -7.54, 'lon': 110.45, 'elevation': 2910, 'status': 'active', 'last_eruption': 2023, 'vei': 4},
            {'name': 'Kelud', 'lat': -7.93, 'lon': 112.31, 'elevation': 1731, 'status': 'active', 'last_eruption': 2014, 'vei': 4},
            {'name': 'Sinabung', 'lat': 3.17, 'lon': 98.39, 'elevation': 2460, 'status': 'active', 'last_eruption': 2023, 'vei': 3},
            {'name': 'Toba', 'lat': 2.69, 'lon': 98.83, 'elevation': 505, 'status': 'dormant', 'last_eruption': -72000, 'vei': 8},

            # PHILIPPINES - Ring of Fire
            {'name': 'Mayon', 'lat': 13.26, 'lon': 123.69, 'elevation': 2463, 'status': 'active', 'last_eruption': 2023, 'vei': 4},
            {'name': 'Pinatubo', 'lat': 15.13, 'lon': 120.35, 'elevation': 1486, 'status': 'active', 'last_eruption': 1993, 'vei': 6},
            {'name': 'Taal', 'lat': 14.00, 'lon': 120.99, 'elevation': 311, 'status': 'active', 'last_eruption': 2022, 'vei': 4},

            # NEW ZEALAND - Ring of Fire
            {'name': 'Ruapehu', 'lat': -39.28, 'lon': 175.57, 'elevation': 2797, 'status': 'active', 'last_eruption': 2007, 'vei': 3},
            {'name': 'Tarawera', 'lat': -38.23, 'lon': 176.51, 'elevation': 1111, 'status': 'active', 'last_eruption': 1886, 'vei': 5},
            {'name': 'White Island', 'lat': -37.52, 'lon': 177.18, 'elevation': 321, 'status': 'active', 'last_eruption': 2019, 'vei': 2},

            # CENTRAL AMERICA - Ring of Fire
            {'name': 'Arenal', 'lat': 10.46, 'lon': -84.70, 'elevation': 1633, 'status': 'active', 'last_eruption': 2010, 'vei': 3},
            {'name': 'Poás', 'lat': 10.20, 'lon': -84.23, 'elevation': 2708, 'status': 'active', 'last_eruption': 2021, 'vei': 2},
            {'name': 'Irazú', 'lat': 9.98, 'lon': -83.85, 'elevation': 3432, 'status': 'active', 'last_eruption': 1994, 'vei': 3},
            {'name': 'Masaya', 'lat': 11.98, 'lon': -86.16, 'elevation': 635, 'status': 'active', 'last_eruption': 2023, 'vei': 2},

            # SOUTH AMERICA - Andes & Ring of Fire
            {'name': 'Cotopaxi', 'lat': -0.68, 'lon': -78.44, 'elevation': 5897, 'status': 'active', 'last_eruption': 2016, 'vei': 4},
            {'name': 'Reventador', 'lat': -0.08, 'lon': -77.66, 'elevation': 3562, 'status': 'active', 'last_eruption': 2024, 'vei': 3},
            {'name': 'Villarrica', 'lat': -39.42, 'lon': -71.93, 'elevation': 2847, 'status': 'active', 'last_eruption': 2023, 'vei': 2},
            {'name': 'Llaima', 'lat': -38.69, 'lon': -71.73, 'elevation': 3125, 'status': 'active', 'last_eruption': 2009, 'vei': 2},

            # ITALY - Mediterranean
            {'name': 'Mount Vesuvius', 'lat': 40.82, 'lon': 14.43, 'elevation': 1281, 'status': 'active', 'last_eruption': 1944, 'vei': 4},
            {'name': 'Mount Etna', 'lat': 37.75, 'lon': 14.99, 'elevation': 3329, 'status': 'active', 'last_eruption': 2024, 'vei': 3},
            {'name': 'Stromboli', 'lat': 38.79, 'lon': 15.21, 'elevation': 924, 'status': 'active', 'last_eruption': 2024, 'vei': 2},
            {'name': 'Vulcano', 'lat': 38.40, 'lon': 14.96, 'elevation': 499, 'status': 'active', 'last_eruption': 1890, 'vei': 3},

            # ICELAND - Mid-Atlantic Ridge
            {'name': 'Eyjafjallajökull', 'lat': 63.63, 'lon': -19.62, 'elevation': 1651, 'status': 'active', 'last_eruption': 2010, 'vei': 4},
            {'name': 'Hekla', 'lat': 63.98, 'lon': -19.70, 'elevation': 1491, 'status': 'active', 'last_eruption': 2000, 'vei': 3},
            {'name': 'Katla', 'lat': 63.63, 'lon': -19.05, 'elevation': 1512, 'status': 'active', 'last_eruption': 1918, 'vei': 4},
            {'name': 'Grímsvötn', 'lat': 64.42, 'lon': -17.33, 'elevation': 1725, 'status': 'active', 'last_eruption': 2011, 'vei': 3},
            {'name': 'Bárðarbunga', 'lat': 64.64, 'lon': -17.53, 'elevation': 2009, 'status': 'active', 'last_eruption': 2015, 'vei': 2},

            # TURKEY - Near North Anatolian Fault
            {'name': 'Mount Ararat', 'lat': 39.70, 'lon': 44.30, 'elevation': 5137, 'status': 'dormant', 'last_eruption': -2500, 'vei': 4},
            {'name': 'Nemrut', 'lat': 38.65, 'lon': 42.23, 'elevation': 3050, 'status': 'active', 'last_eruption': 1597, 'vei': 3},

            # RUSSIA - KAMCHATKA PENINSULA (Pacific Ring of Fire)
            {'name': 'Shiveluch', 'lat': 56.65, 'lon': 161.36, 'elevation': 3283, 'status': 'active', 'last_eruption': 2024, 'vei': 4},
            {'name': 'Klyuchevskoy', 'lat': 56.06, 'lon': 160.64, 'elevation': 4754, 'status': 'active', 'last_eruption': 2024, 'vei': 3},
            {'name': 'Bezymianny', 'lat': 55.97, 'lon': 160.60, 'elevation': 2882, 'status': 'active', 'last_eruption': 2024, 'vei': 5},
            {'name': 'Karymsky', 'lat': 54.05, 'lon': 159.45, 'elevation': 1536, 'status': 'active', 'last_eruption': 2024, 'vei': 3},
            {'name': 'Avachinsky', 'lat': 53.26, 'lon': 158.83, 'elevation': 2741, 'status': 'active', 'last_eruption': 2001, 'vei': 3},
            {'name': 'Mutnovsky', 'lat': 52.45, 'lon': 158.20, 'elevation': 2323, 'status': 'active', 'last_eruption': 2000, 'vei': 2},
            {'name': 'Tolbachik', 'lat': 55.83, 'lon': 160.33, 'elevation': 3682, 'status': 'active', 'last_eruption': 2013, 'vei': 3},
            {'name': 'Zhupanovsky', 'lat': 53.59, 'lon': 159.15, 'elevation': 2958, 'status': 'active', 'last_eruption': 2016, 'vei': 2},

            # RUSSIA - KURIL ISLANDS (Pacific Ring of Fire)
            {'name': 'Ebeko', 'lat': 50.69, 'lon': 156.01, 'elevation': 1103, 'status': 'active', 'last_eruption': 2024, 'vei': 2},
            {'name': 'Chikurachki', 'lat': 50.32, 'lon': 155.46, 'elevation': 1816, 'status': 'active', 'last_eruption': 2023, 'vei': 3},
            {'name': 'Sarychev Peak', 'lat': 48.09, 'lon': 153.20, 'elevation': 1496, 'status': 'active', 'last_eruption': 2009, 'vei': 4},
            {'name': 'Nemrut', 'lat': 38.65, 'lon': 42.23, 'elevation': 3050, 'status': 'active', 'last_eruption': 1597, 'vei': 3},

            # SUPERVOLCANOES & LARGE CALDERAS
            {'name': 'Yellowstone', 'lat': 44.43, 'lon': -110.67, 'elevation': 2805, 'status': 'dormant', 'last_eruption': -70000, 'vei': 8},
            {'name': 'Valles Caldera', 'lat': 35.87, 'lon': -106.57, 'elevation': 3430, 'status': 'dormant', 'last_eruption': -50000, 'vei': 6},
            {'name': 'Campi Flegrei', 'lat': 40.83, 'lon': 14.14, 'elevation': 458, 'status': 'active', 'last_eruption': 1538, 'vei': 7},

            # AFRICA - East African Rift
            {'name': 'Kilimanjaro', 'lat': -3.07, 'lon': 37.35, 'elevation': 5895, 'status': 'dormant', 'last_eruption': -360000, 'vei': 4},
            {'name': 'Ol Doinyo Lengai', 'lat': -2.76, 'lon': 35.91, 'elevation': 2962, 'status': 'active', 'last_eruption': 2013, 'vei': 2},
            {'name': 'Erta Ale', 'lat': 13.60, 'lon': 40.67, 'elevation': 613, 'status': 'active', 'last_eruption': 2023, 'vei': 2},

            # MEXICO & GUATEMALA - Trans-Mexican Volcanic Belt
            {'name': 'Popocatépetl', 'lat': 19.02, 'lon': -98.62, 'elevation': 5426, 'status': 'active', 'last_eruption': 2024, 'vei': 3},
            {'name': 'Colima', 'lat': 19.51, 'lon': -103.62, 'elevation': 3850, 'status': 'active', 'last_eruption': 2017, 'vei': 3},
            {'name': 'Pico de Orizaba', 'lat': 19.03, 'lon': -97.27, 'elevation': 5636, 'status': 'dormant', 'last_eruption': 1687, 'vei': 2},
            {'name': 'Fuego', 'lat': 14.47, 'lon': -90.88, 'elevation': 3763, 'status': 'active', 'last_eruption': 2024, 'vei': 4},

            # CARIBBEAN - Lesser Antilles Arc
            {'name': 'Soufrière Hills', 'lat': 16.72, 'lon': -62.18, 'elevation': 915, 'status': 'active', 'last_eruption': 2013, 'vei': 3},
            {'name': 'Mount Pelée', 'lat': 14.82, 'lon': -61.17, 'elevation': 1397, 'status': 'active', 'last_eruption': 1932, 'vei': 4},
            {'name': 'La Soufrière (St. Vincent)', 'lat': 13.33, 'lon': -61.18, 'elevation': 1234, 'status': 'active', 'last_eruption': 2021, 'vei': 4}
        ]
        return pd.DataFrame(volcanoes)

    def calculate_plate_boundary_distance(self, lat, lon):
        """Calculate minimum distance to nearest plate boundary"""
        min_distance = float('inf')
        nearest_plate = None
        boundary_type = None
        plate_activity = 0

        for plate_name, plate_data in self.tectonic_plates.items():
            for boundary in plate_data['boundaries']:
                distance = geodesic((lat, lon), (boundary['lat'], boundary['lon'])).kilometers
                if distance < min_distance:
                    min_distance = distance
                    nearest_plate = plate_name
                    boundary_type = boundary['type']
                    plate_activity = boundary['activity']

        return min_distance, nearest_plate, boundary_type, plate_activity

    def calculate_volcanic_influence(self, lat, lon):
        """Calculate volcanic influence on earthquake risk"""
        volcanic_risk = 0
        nearest_volcano_distance = float('inf')
        active_volcanoes_nearby = 0

        for _, volcano in self.volcanoes.iterrows():
            distance = geodesic((lat, lon), (volcano['lat'], volcano['lon'])).kilometers

            if distance < nearest_volcano_distance:
                nearest_volcano_distance = distance

            # Calculate influence based on distance and volcanic characteristics
            if distance < 500:  # Within 500km
                if volcano['status'] == 'active':
                    active_volcanoes_nearby += 1
                    # Recent eruption increases risk
                    years_since_eruption = 2024 - volcano['last_eruption']
                    if years_since_eruption < 50:
                        volcanic_risk += (volcano['vei'] / 10) * (500 - distance) / 500
                elif volcano['status'] == 'dormant':
                    volcanic_risk += (volcano['vei'] / 20) * (500 - distance) / 500

        return volcanic_risk, nearest_volcano_distance, active_volcanoes_nearby

    def predict_plate_movement(self, lat, lon):
        """Predict tectonic plate movement effects"""
        min_dist, plate_name, boundary_type, activity = self.calculate_plate_boundary_distance(lat, lon)

        if plate_name:
            plate_data = self.tectonic_plates[plate_name]
            movement_rate = plate_data['movement_rate']

            # Calculate stress accumulation based on movement rate and boundary type
            stress_multiplier = {
                'convergent': 1.5,
                'transform': 1.2,
                'divergent': 0.8
            }

            plate_stress = (movement_rate * stress_multiplier.get(boundary_type, 1.0) *
                          activity * (1000 / max(min_dist, 1)))

            return plate_stress, movement_rate, boundary_type

        return 0, 0, 'none'

    def generate_enhanced_data(self, n_samples=1000):
        """Generate enhanced earthquake data with geological features"""
        np.random.seed(42)

        # Basic features
        data = {
            'magnitude': np.random.normal(4.5, 1.5, n_samples),
            'depth': np.random.exponential(20, n_samples),
            'latitude': np.random.uniform(-90, 90, n_samples),
            'longitude': np.random.uniform(-180, 180, n_samples),
            'previous_activity': np.random.poisson(3, n_samples),
            'fault_distance': np.random.exponential(50, n_samples),
            'rock_density': np.random.normal(2.7, 0.3, n_samples),
            'stress_accumulation': np.random.exponential(10, n_samples),
            'groundwater_level': np.random.normal(100, 20, n_samples),
            'tidal_force': np.random.uniform(-1, 1, n_samples)
        }

        df = pd.DataFrame(data)

        # Add enhanced geological features
        enhanced_features = []
        for idx, row in df.iterrows():
            lat, lon = row['latitude'], row['longitude']

            # Plate boundary analysis
            plate_stress, movement_rate, boundary_type = self.predict_plate_movement(lat, lon)

            # Volcanic influence
            volcanic_risk, volcano_dist, active_nearby = self.calculate_volcanic_influence(lat, lon)

            enhanced_features.append({
                'plate_boundary_distance': self.calculate_plate_boundary_distance(lat, lon)[0],
                'plate_stress': plate_stress,
                'plate_movement_rate': movement_rate,
                'boundary_type_convergent': 1 if boundary_type == 'convergent' else 0,
                'boundary_type_transform': 1 if boundary_type == 'transform' else 0,
                'boundary_type_divergent': 1 if boundary_type == 'divergent' else 0,
                'volcanic_risk_index': volcanic_risk,
                'nearest_volcano_distance': volcano_dist,
                'active_volcanoes_nearby': active_nearby
            })

        enhanced_df = pd.DataFrame(enhanced_features)
        df = pd.concat([df, enhanced_df], axis=1)

        # Enhanced risk calculation
        risk_probability = (
            (df['magnitude'] - 3) / 5 * 0.3 +
            (30 - df['depth']) / 50 * 0.2 +
            df['previous_activity'] / 10 * 0.15 +
            df['plate_stress'] / 100 * 0.2 +
            df['volcanic_risk_index'] / 10 * 0.1 +
            (500 - df['plate_boundary_distance']) / 500 * 0.05
        )

        df['earthquake_risk'] = (np.random.random(n_samples) < np.clip(risk_probability, 0, 1)).astype(int)

        return df

    def create_interactive_map(self, df_sample=None):
        """Create an interactive map showing geological features"""
        # Center map on global view
        m = folium.Map(location=[20, 0], zoom_start=2)

        # Add tectonic plate boundaries
        for plate_name, plate_data in self.tectonic_plates.items():
            coords = [(b['lat'], b['lon']) for b in plate_data['boundaries']]

            color_map = {'convergent': 'red', 'transform': 'blue', 'divergent': 'green'}

            for i, boundary in enumerate(plate_data['boundaries']):
                folium.CircleMarker(
                    location=[boundary['lat'], boundary['lon']],
                    radius=8,
                    popup=f"{plate_name}<br>Type: {boundary['type']}<br>Activity: {boundary['activity']}",
                    color=color_map.get(boundary['type'], 'gray'),
                    fill=True,
                    weight=2
                ).add_to(m)

        # Add volcanoes
        for _, volcano in self.volcanoes.iterrows():
            color = 'red' if volcano['status'] == 'active' else 'orange' if volcano['status'] == 'dormant' else 'gray'

            folium.Marker(
                location=[volcano['lat'], volcano['lon']],
                popup=f"{volcano['name']}<br>Status: {volcano['status']}<br>VEI: {volcano['vei']}<br>Last Eruption: {volcano['last_eruption']}",
                icon=folium.Icon(color=color, icon='fire')
            ).add_to(m)

        # Add sample earthquake data if provided
        if df_sample is not None:
            for _, row in df_sample.head(50).iterrows():  # Show first 50 points
                color = 'red' if row['earthquake_risk'] == 1 else 'blue'
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=row['magnitude'],
                    popup=f"Magnitude: {row['magnitude']:.1f}<br>Risk: {'High' if row['earthquake_risk'] else 'Low'}",
                    color=color,
                    fill=True,
                    opacity=0.6
                ).add_to(m)

        # Add legend
        legend_html = '''
        <div style="position: fixed;
                    bottom: 50px; left: 50px; width: 150px; height: 90px;
                    background-color: white; border:2px solid grey; z-index:9999;
                    font-size:14px; padding: 10px">
        <b>Legend</b><br>
        🔴 Active Volcano<br>
        🟠 Dormant Volcano<br>
        🔵 Transform Boundary<br>
        🔴 Convergent Boundary<br>
        🟢 Divergent Boundary
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))

        return m

    def prepare_enhanced_data(self, df):
        """Prepare enhanced data for training"""
        # Define all feature columns
        feature_columns = [
            'magnitude', 'depth', 'latitude', 'longitude', 'previous_activity',
            'fault_distance', 'rock_density', 'stress_accumulation',
            'groundwater_level', 'tidal_force', 'plate_boundary_distance',
            'plate_stress', 'plate_movement_rate', 'boundary_type_convergent',
            'boundary_type_transform', 'boundary_type_divergent',
            'volcanic_risk_index', 'nearest_volcano_distance', 'active_volcanoes_nearby'
        ]

        # Ensure all columns exist
        for col in feature_columns:
            if col not in df.columns:
                print(f"Warning: Missing column {col}, setting to 0")
                df[col] = 0

        X = df[feature_columns]
        y = df['earthquake_risk']

        return X, y, feature_columns

    def train_enhanced_models(self, X, y):
        """Train models with enhanced features"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        models = {
            'Enhanced Random Forest': RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42),
            'Enhanced Gradient Boosting': GradientBoostingClassifier(n_estimators=150, max_depth=8, random_state=42),
            'Enhanced Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
        }

        results = {}
        for name, model in models.items():
            if 'Logistic' in name:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'predictions': y_pred,
                'y_test': y_test
            }

            print(f"\n{name} Results:")
            print(f"Accuracy: {accuracy:.3f}")
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))

        self.models = {name: result['model'] for name, result in results.items()}
        self.is_trained = True

        return results

    def enhanced_risk_assessment(self, lat, lon, magnitude, depth, **kwargs):
        """Comprehensive risk assessment for a specific location"""
        print(f"\n{'='*80}")
        print("ADVANCED EARTHQUAKE RISK ASSESSMENT")
        print(f"{'='*80}")
        print(f"Location: {lat:.4f}°N, {lon:.4f}°E")
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Geological analysis
        print(f"\n{'GEOLOGICAL ANALYSIS'}")
        print(f"{'-'*40}")

        plate_stress, movement_rate, boundary_type = self.predict_plate_movement(lat, lon)
        plate_dist, plate_name, _, plate_activity = self.calculate_plate_boundary_distance(lat, lon)
        volcanic_risk, volcano_dist, active_nearby = self.calculate_volcanic_influence(lat, lon)

        print(f"Nearest Plate Boundary: {plate_name}")
        print(f"Distance to Plate Boundary: {plate_dist:.1f} km")
        print(f"Boundary Type: {boundary_type}")
        print(f"Plate Movement Rate: {movement_rate:.1f} cm/year")
        print(f"Tectonic Stress Index: {plate_stress:.2f}")
        print(f"Plate Activity Level: {plate_activity:.2f}")

        print(f"\n{'VOLCANIC ANALYSIS'}")
        print(f"{'-'*40}")
        print(f"Volcanic Risk Index: {volcanic_risk:.2f}")
        print(f"Nearest Volcano Distance: {volcano_dist:.1f} km")
        print(f"Active Volcanoes Nearby: {active_nearby}")

        # Risk level determination
        risk_factors = {
            'Magnitude': magnitude / 10,
            'Shallow Depth': max(0, (50 - depth) / 50),
            'Plate Boundary Proximity': max(0, (500 - plate_dist) / 500),
            'Tectonic Stress': min(1, plate_stress / 50),
            'Volcanic Activity': min(1, volcanic_risk / 5)
        }

        overall_risk = sum(risk_factors.values()) / len(risk_factors)

        print(f"\n{'RISK FACTOR BREAKDOWN'}")
        print(f"{'-'*40}")
        for factor, value in risk_factors.items():
            print(f"{factor}: {value:.3f}")

        print(f"\n{'OVERALL ASSESSMENT'}")
        print(f"{'-'*40}")
        if overall_risk > 0.7:
            risk_level = "VERY HIGH"
            color = "🔴"
        elif overall_risk > 0.5:
            risk_level = "HIGH"
            color = "🟠"
        elif overall_risk > 0.3:
            risk_level = "MODERATE"
            color = "🟡"
        else:
            risk_level = "LOW"
            color = "🟢"

        print(f"Risk Level: {color} {risk_level}")
        print(f"Risk Score: {overall_risk:.3f}")

        return overall_risk, risk_level

    def estimate_location_parameters(self, lat, lon):
        """Estimate realistic earthquake parameters based on location's geological context"""
        # Get geological context
        plate_dist, plate_name, boundary_type, plate_activity = self.calculate_plate_boundary_distance(lat, lon)
        volcanic_risk, volcano_dist, active_nearby = self.calculate_volcanic_influence(lat, lon)
        
        # Estimate magnitude based on geological factors
        if plate_dist < 100:  # Very close to plate boundary
            base_magnitude = 6.5 + (plate_activity * 1.5)
        elif plate_dist < 300:  # Moderate distance
            base_magnitude = 5.5 + (plate_activity * 1.0)
        else:  # Far from boundaries
            base_magnitude = 4.5 + (plate_activity * 0.5)
            
        # Adjust for volcanic activity
        if active_nearby > 0:
            base_magnitude += 0.3 * min(active_nearby, 3)
            
        # Estimate depth based on boundary type
        if boundary_type == 'convergent':
            estimated_depth = np.random.normal(25, 10)  # Deeper for convergent
        elif boundary_type == 'transform':
            estimated_depth = np.random.normal(15, 5)   # Moderate depth
        else:  # divergent or none
            estimated_depth = np.random.normal(10, 5)   # Shallower
            
        return {
            'magnitude': max(3.0, min(8.5, base_magnitude)),
            'depth': max(1, min(100, estimated_depth)),
            'geological_context': {
                'plate_distance': plate_dist,
                'plate_name': plate_name,
                'boundary_type': boundary_type,
                'volcanic_activity': active_nearby
            }
        }


def main():
    """Main function for advanced earthquake prediction"""
    print("🌋 Advanced Earthquake Prediction System")
    print("Incorporating Tectonic Plates & Volcanic Activity")
    print("="*60)

    predictor = AdvancedEarthquakePredictor()

    print("Generating enhanced geological dataset...")
    df = predictor.generate_enhanced_data(2000)

    print(f"Dataset shape: {df.shape}")
    print(f"Enhanced features added: {df.columns.tolist()[-9:]}")

    # Train enhanced models
    print("\nTraining enhanced prediction models...")
    X, y, feature_columns = predictor.prepare_enhanced_data(df)
    results = predictor.train_enhanced_models(X, y)

    # Create interactive map
    print("\nCreating interactive geological map...")
    interactive_map = predictor.create_interactive_map(df.sample(100))
    interactive_map.save('geological_analysis_map.html')
    print("Map saved as 'geological_analysis_map.html'")

    # Interactive location analysis
    print("\n🌍 LOCATION RISK ANALYSIS")
    print("="*50)
    
    # Option 1: User input
    print("Choose analysis mode:")
    print("1. Analyze your custom location")
    print("2. Analyze sample high-risk locations")
    print("3. Skip location analysis")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            # Custom location input
            print("\n📍 Enter your location details:")
            lat = float(input("Latitude (-90 to 90): "))
            lon = float(input("Longitude (-180 to 180): "))
            location_name = input("Location name (optional): ") or f"{lat:.2f}°N, {lon:.2f}°E"
            
            # Estimate realistic parameters based on location
            mag = float(input("Expected magnitude (3.0-8.0) or press Enter for auto: ") or "6.0")
            depth = float(input("Expected depth in km (1-100) or press Enter for auto: ") or "15")
            
            print(f"\nAnalyzing {location_name}...")
            risk_score, risk_level = predictor.enhanced_risk_assessment(lat, lon, mag, depth)
            print(f"\n🎯 {location_name}: {risk_level} (Score: {risk_score:.3f})")
            
        elif choice == "2":
            # Sample high-risk locations for demonstration
            sample_locations = [
                {"name": "San Francisco, CA", "lat": 37.7749, "lon": -122.4194, "mag": 6.0, "depth": 12},
                {"name": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503, "mag": 7.2, "depth": 25},
                {"name": "Istanbul, Turkey", "lat": 41.0082, "lon": 28.9784, "mag": 6.8, "depth": 18},
                {"name": "Los Angeles, CA", "lat": 34.0522, "lon": -118.2437, "mag": 6.5, "depth": 15},
                {"name": "Reykjavik, Iceland", "lat": 64.1466, "lon": -21.9426, "mag": 5.5, "depth": 8}
            ]
            
            print("\nAnalyzing sample high-risk locations...")
            for location in sample_locations:
                risk_score, risk_level = predictor.enhanced_risk_assessment(
                    location["lat"], location["lon"],
                    location["mag"], location["depth"]
                )
                print(f"\n{location['name']}: {risk_level} (Score: {risk_score:.3f})")
        
        else:
            print("Skipping location analysis.")
            
    except (ValueError, KeyboardInterrupt):
        print("\nUsing default sample locations for demonstration...")
        # Fallback to a few key examples
        sample_locations = [
            {"name": "Los Angeles, CA", "lat": 34.0522, "lon": -118.2437, "mag": 6.5, "depth": 15},
            {"name": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503, "mag": 7.2, "depth": 25}
        ]
        
        for location in sample_locations:
            risk_score, risk_level = predictor.enhanced_risk_assessment(
                location["lat"], location["lon"],
                location["mag"], location["depth"]
            )
            print(f"\n{location['name']}: {risk_level} (Score: {risk_score:.3f})")

    print("\n🎯 Advanced analysis completed!")
    print("Check 'geological_analysis_map.html' for interactive visualization.")


if __name__ == "__main__":
    main()
