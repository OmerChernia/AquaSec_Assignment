"""
Abstract base repository for data access patterns.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class BaseRepository(ABC):
    """Abstract base class for repositories."""
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        """Get all entities."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def create(self, entity: Any) -> Any:
        """Create new entity."""
        pass
    