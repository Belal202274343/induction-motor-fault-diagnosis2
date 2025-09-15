"""Data preprocessing module for motor fault diagnosis.

This module handles all data preprocessing steps including:
- Data loading and validation
- Cleaning and normalization
- Feature engineering
- Train/test splitting
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """Load and validate motor data from CSV file."""
    df = pd.read_csv(file_path)
    
    # Validate required columns
    required_columns = [
        'timestamp', 'motor_id', 'temperature', 'vibration_amplitude',
        'current', 'voltage', 'speed_rpm', 'noise_level', 'fault_type'
    ]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the motor data."""
    df = df.copy()
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Handle missing values
    numeric_cols = ['temperature', 'vibration_amplitude', 'current', 'voltage', 
                   'speed_rpm', 'noise_level']
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Add engineered features
    df['power'] = df['current'] * df['voltage']
    df['efficiency'] = df['speed_rpm'] / df['power']
    
    return df

def normalize_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, StandardScaler]:
    """Normalize numerical features using StandardScaler."""
    numeric_cols = ['temperature', 'vibration_amplitude', 'current', 'voltage', 
                   'speed_rpm', 'noise_level', 'power', 'efficiency']
    
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    return df_scaled, scaler

def split_data(df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split data into training and testing sets."""
    # Separate features and target
    X = df.drop(['fault_type', 'timestamp', 'motor_id'], axis=1)
    y = df['fault_type']
    
    # Perform the split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    return X_train, X_test, y_train, y_test
