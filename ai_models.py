import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

class AIDecisionModel:
    def __init__(self):
        # In a real scenario, this would load a pre-trained model and scaler
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.scaler = StandardScaler()
        self._initialize_mock_model()
        
    def _initialize_mock_model(self):
        # Create some dummy training data to initialize the model
        # We predict if a transaction or event requires attention (1) or is safe (0)
        # based on incoming attributes like amount, frequency, and time_of_day.
        np.random.seed(42)
        X_dummy = pd.DataFrame({
            'amount': np.random.uniform(10, 1000, 100),
            'frequency': np.random.uniform(1, 50, 100),
            'time_of_day': np.random.uniform(0, 24, 100)
        })
        # Mock target: high amount and high frequency -> higher chance of requiring action
        y_dummy = ((X_dummy['amount'] > 500) & (X_dummy['frequency'] > 30)).astype(int)
        
        X_scaled = self.scaler.fit_transform(X_dummy)
        self.model.fit(X_scaled, y_dummy)
        
    def predict(self, data: dict) -> dict:
        """
        Takes incoming data dictionary, processes it, and returns a prediction.
        Expected keys: 'amount', 'frequency', 'time_of_day'
        """
        # Convert single dictionary to DataFrame
        df = pd.DataFrame([data])
        
        # Ensure correct columns and order
        expected_cols = ['amount', 'frequency', 'time_of_day']
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0.0 # Default fallback
                
        df = df[expected_cols]
        
        # Preprocess
        X_scaled = self.scaler.transform(df)
        
        # Predict
        prediction = self.model.predict(X_scaled)[0]
        probability = self.model.predict_proba(X_scaled)[0].max()
        
        return {
            "prediction": int(prediction),
            "confidence": float(probability),
            "action_required": bool(prediction == 1)
        }

# Singleton instance for easy import
decision_model = AIDecisionModel()
