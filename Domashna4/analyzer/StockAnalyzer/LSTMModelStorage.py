import os
import joblib
from tensorflow.keras.models import load_model
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Optional

# Singleton Pattern for ModelStorage
class ModelStorage:
    _instance = None

    def __new__(cls, base_path='models'):
        if cls._instance is None:
            cls._instance = super(ModelStorage, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, base_path='models'):
        if not self._initialized:
            self.base_path = base_path
            self._storage_strategy = FileSystemStorageStrategy()
            os.makedirs(base_path, exist_ok=True)
            self._initialized = True

    # Factory Method Pattern
    @staticmethod
    def create_storage(storage_type: str = 'filesystem', base_path: str = 'models') -> 'ModelStorage':
        storage = ModelStorage(base_path)
        if storage_type == 'filesystem':
            storage._storage_strategy = FileSystemStorageStrategy()
        # Can add more storage types here (e.g., cloud, database)
        return storage

    def save_model(self, model: Any, volume_scaler: Any, price_scaler: Any, 
                  binary_encoder: Any, model_name: str = 'stock_prediction',
                  additional_params: Optional[Dict] = None) -> None:
        """Maintains the same interface but delegates to strategy"""
        self._storage_strategy.save_model(
            self.base_path,
            model,
            volume_scaler,
            price_scaler,
            binary_encoder,
            model_name,
            additional_params
        )

    def load_model(self, model_name: str = 'stock_prediction') -> Tuple:
        """Maintains the same interface but delegates to strategy"""
        return self._storage_strategy.load_model(self.base_path, model_name)

    def list_saved_models(self) -> List[str]:
        """Maintains the same interface but delegates to strategy"""
        return self._storage_strategy.list_saved_models(self.base_path)

# Strategy Pattern
class StorageStrategy(ABC):
    @abstractmethod
    def save_model(self, base_path: str, model: Any, volume_scaler: Any,
                  price_scaler: Any, binary_encoder: Any, model_name: str,
                  additional_params: Optional[Dict]) -> None:
        pass

    @abstractmethod
    def load_model(self, base_path: str, model_name: str) -> Tuple:
        pass

    @abstractmethod
    def list_saved_models(self, base_path: str) -> List[str]:
        pass

class FileSystemStorageStrategy(StorageStrategy):
    def save_model(self, base_path: str, model: Any, volume_scaler: Any,
                  price_scaler: Any, binary_encoder: Any, model_name: str,
                  additional_params: Optional[Dict]) -> None:
        model_dir = os.path.join(base_path, model_name)
        os.makedirs(model_dir, exist_ok=True)

        # Save model
        model_path = os.path.join(model_dir, 'model.keras')
        model.save(model_path)

        # Save scalers and encoder
        joblib.dump(price_scaler, os.path.join(model_dir, 'price_scaler.pkl'))
        joblib.dump(volume_scaler, os.path.join(model_dir, 'volume_scaler.pkl'))
        joblib.dump(binary_encoder, os.path.join(model_dir, 'encoder.pkl'))

        # Save additional parameters
        if additional_params:
            params_path = os.path.join(model_dir, 'params.json')
            with open(params_path, 'w') as f:
                json.dump(additional_params, f)

    def load_model(self, base_path: str, model_name: str) -> Tuple:
        model_dir = os.path.join(base_path, model_name)
        
        # Load model
        model = load_model(os.path.join(model_dir, 'model.keras'))
        
        # Load scalers and encoder
        price_scaler = joblib.load(os.path.join(model_dir, 'price_scaler.pkl'))
        volume_scaler = joblib.load(os.path.join(model_dir, 'volume_scaler.pkl'))
        binary_encoder = joblib.load(os.path.join(model_dir, 'encoder.pkl'))
        
        # Load additional parameters
        additional_params = None
        params_path = os.path.join(model_dir, 'params.json')
        if os.path.exists(params_path):
            with open(params_path, 'r') as f:
                additional_params = json.load(f)
                
        return price_scaler, volume_scaler, binary_encoder, model, additional_params

    def list_saved_models(self, base_path: str) -> List[str]:
        if not os.path.exists(base_path):
            return []
        return [d for d in os.listdir(base_path)
                if os.path.isdir(os.path.join(base_path, d))]