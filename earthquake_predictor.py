#!/usr/bin/env python3
"""
Enhanced Earthquake Prediction Application
This application provides multiple machine learning models for earthquake prediction.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import requests
import warnings
warnings.filterwarnings('ignore')

class EarthquakePredictor:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_synthetic_data(self, n_samples=1000):
        """
        Generate synthetic earthquake data for demonstration.
        In a real application, this would load actual seismic data.
        """
        np.random.seed(42)
        
        # Features: magnitude, depth, latitude, longitude, previous_activity, etc.
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
        
        # Create target variable (1 for earthquake likely, 0 for unlikely)
        # Higher magnitude, shallower depth, more previous activity = higher probability
        probability = (
            (df['magnitude'] - 3) / 5 +
            (30 - df['depth']) / 50 +
            df['previous_activity'] / 10 +
            df['stress_accumulation'] / 20
        ) / 4
        
        df['earthquake_risk'] = (np.random.random(n_samples) < probability).astype(int)
        
        return df
    
    def fetch_real_earthquake_data(self, days_back=30):
        """
        Fetch real earthquake data from USGS API.
        This is a simplified version - in practice, you'd need more comprehensive data.
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            url = f"https://earthquake.usgs.gov/fdsnws/event/1/query"
            params = {
                'format': 'geojson',
                'starttime': start_date.strftime('%Y-%m-%d'),
                'endtime': end_date.strftime('%Y-%m-%d'),
                'minmagnitude': 2.0
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                earthquakes = []
                
                for feature in data['features']:
                    props = feature['properties']
                    coords = feature['geometry']['coordinates']
                    
                    earthquakes.append({
                        'magnitude': props.get('mag', 0),
                        'depth': coords[2] if len(coords) > 2 else 0,
                        'latitude': coords[1],
                        'longitude': coords[0],
                        'time': props.get('time', 0)
                    })
                
                df = pd.DataFrame(earthquakes)
                print(f"Fetched {len(df)} real earthquake records")
                return df
            else:
                print("Failed to fetch real data, using synthetic data")
                return None
                
        except Exception as e:
            print(f"Error fetching real data: {e}")
            return None
    
    def prepare_data(self, df):
        """Prepare data for training"""
        # Define expected feature columns in order
        self.feature_columns = ['magnitude', 'depth', 'latitude', 'longitude', 
                               'previous_activity', 'fault_distance', 'rock_density',
                               'stress_accumulation', 'groundwater_level', 'tidal_force']
        
        # Ensure all required columns exist
        for col in self.feature_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Select only the expected features in the correct order
        X = df[self.feature_columns]
        y = df['earthquake_risk']
        
        return X, y
    
    def train_models(self, X, y):
        """Train multiple models"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Initialize models
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42)
        }
        
        # Train and evaluate models
        results = {}
        for name, model in models.items():
            if name == 'Logistic Regression':
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
    
    def predict(self, features, model_name='Random Forest'):
        """Make predictions using specified model"""
        if not self.is_trained:
            raise ValueError("Models not trained yet. Call train_models first.")
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not available")
        
        model = self.models[model_name]
        
        if model_name == 'Logistic Regression':
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            prediction = model.predict(features_scaled)
            probability = model.predict_proba(features_scaled)[0]
        else:
            prediction = model.predict(features.reshape(1, -1))
            probability = model.predict_proba(features.reshape(1, -1))[0]
        
        return prediction[0], probability
    
    def visualize_data(self, df):
        """Create visualizations of the earthquake data"""
        plt.figure(figsize=(15, 10))
        
        # Magnitude distribution
        plt.subplot(2, 3, 1)
        plt.hist(df['magnitude'], bins=30, alpha=0.7, color='skyblue')
        plt.xlabel('Magnitude')
        plt.ylabel('Frequency')
        plt.title('Earthquake Magnitude Distribution')
        
        # Depth vs Magnitude
        plt.subplot(2, 3, 2)
        scatter = plt.scatter(df['depth'], df['magnitude'], 
                            c=df['earthquake_risk'], cmap='viridis', alpha=0.6)
        plt.xlabel('Depth (km)')
        plt.ylabel('Magnitude')
        plt.title('Depth vs Magnitude (colored by risk)')
        plt.colorbar(scatter)
        
        # Risk distribution
        plt.subplot(2, 3, 3)
        risk_counts = df['earthquake_risk'].value_counts()
        plt.pie(risk_counts.values, labels=['Low Risk', 'High Risk'], 
                autopct='%1.1f%%', colors=['lightcoral', 'gold'])
        plt.title('Earthquake Risk Distribution')
        
        # Feature correlation heatmap
        plt.subplot(2, 3, 4)
        correlation = df.corr()
        sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
        plt.title('Feature Correlation Matrix')
        
        # Geographic distribution
        plt.subplot(2, 3, 5)
        plt.scatter(df['longitude'], df['latitude'], 
                   c=df['earthquake_risk'], cmap='Reds', alpha=0.6)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Geographic Distribution')
        plt.colorbar()
        
        # Previous activity vs risk
        plt.subplot(2, 3, 6)
        risk_by_activity = df.groupby('previous_activity')['earthquake_risk'].mean()
        plt.plot(risk_by_activity.index, risk_by_activity.values, 'o-')
        plt.xlabel('Previous Activity Count')
        plt.ylabel('Average Risk')
        plt.title('Previous Activity vs Risk')
        
        plt.tight_layout()
        plt.savefig('earthquake_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_risk_report(self, sample_features):
        """Generate a comprehensive risk report"""
        print("\n" + "="*60)
        print("EARTHQUAKE RISK ASSESSMENT REPORT")
        print("="*60)
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        feature_names = ['magnitude', 'depth', 'latitude', 'longitude', 
                        'previous_activity', 'fault_distance', 'rock_density',
                        'stress_accumulation', 'groundwater_level', 'tidal_force']
        
        print("INPUT PARAMETERS:")
        print("-" * 20)
        for i, (name, value) in enumerate(zip(feature_names, sample_features)):
            print(f"{name.replace('_', ' ').title()}: {value:.2f}")
        
        print("\nPREDICTION RESULTS:")
        print("-" * 20)
        
        for model_name in self.models.keys():
            try:
                prediction, probability = self.predict(sample_features, model_name)
                risk_level = "HIGH" if prediction == 1 else "LOW"
                confidence = max(probability) * 100
                
                print(f"{model_name}:")
                print(f"  Risk Level: {risk_level}")
                print(f"  Confidence: {confidence:.1f}%")
                print(f"  Probabilities: Low={probability[0]:.3f}, High={probability[1]:.3f}")
                print()
            except Exception as e:
                print(f"Error with {model_name}: {e}")


def main():
    """Main function to run the earthquake prediction application"""
    print("🌍 Earthquake Prediction Application")
    print("====================================")
    
    # Initialize predictor
    predictor = EarthquakePredictor()
    
    # Try to fetch real data, fallback to synthetic
    print("Attempting to fetch real earthquake data...")
    real_data = predictor.fetch_real_earthquake_data(days_back=30)
    
    if real_data is not None and len(real_data) > 100:
        # Add synthetic features to real data for demonstration
        real_data['previous_activity'] = np.random.poisson(3, len(real_data))
        real_data['fault_distance'] = np.random.exponential(50, len(real_data))
        real_data['rock_density'] = np.random.normal(2.7, 0.3, len(real_data))
        real_data['stress_accumulation'] = np.random.exponential(10, len(real_data))
        real_data['groundwater_level'] = np.random.normal(100, 20, len(real_data))
        real_data['tidal_force'] = np.random.uniform(-1, 1, len(real_data))
        
        # Create risk labels based on magnitude and depth
        probability = (real_data['magnitude'] - 2) / 8 + (50 - real_data['depth']) / 100
        real_data['earthquake_risk'] = (np.random.random(len(real_data)) < probability).astype(int)
        df = real_data
    else:
        print("Using synthetic earthquake data for demonstration...")
        df = predictor.generate_synthetic_data(1000)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Risk distribution: {df['earthquake_risk'].value_counts().to_dict()}")
    
    # Prepare and train models
    print("\nPreparing data and training models...")
    X, y = predictor.prepare_data(df)
    results = predictor.train_models(X, y)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    predictor.visualize_data(df)
    
    # Generate sample prediction
    print("\nGenerating sample risk assessment...")
    sample_features = np.array([5.2, 15.0, 37.7749, -122.4194, 
                               5, 25.0, 2.8, 15.0, 95.0, 0.3])
    
    predictor.create_risk_report(sample_features)
    
    print("\n🎯 Application completed successfully!")
    print("Check 'earthquake_analysis.png' for visualizations.")


if __name__ == "__main__":
    main()
