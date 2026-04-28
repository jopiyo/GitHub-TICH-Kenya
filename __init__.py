"""
Data module for ClimateGuard.
This package handles raw sensor ingestion and feature engineering.
"""

from .make_dataset import preprocess_climate_data

__all__ = ["preprocess_climate_data"]
