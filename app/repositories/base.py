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
    
    # Example Future methods:
    # @abstractmethod
    # def update(self, entity: Any) -> Any:
    #     """Update existing entity."""
    #     pass
    
    # @abstractmethod
    # def delete(self, entity_id: str) -> None:
    #     """Delete entity by ID."""
    #     pass
    
    