from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class BaseRepository(ABC):
    """Abstract base class for repositories."""
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        """Returns all items from the repository."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """Gets a single item by its ID."""
        pass
    
    @abstractmethod
    def create(self, entity: Any) -> Any:
        """Creates a new item."""
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
    
    