class Dataset:
    """Represents a dataset in the Data Science domain."""

    def __init__(self, dataset_id: int, name: str, source: str, category: str, size: int):
        self.__dataset_id = dataset_id
        self.__name = name
        self.__source = source
        self.__category = category
        self.__size = size  # stored as bytes (or whatever your DB uses)

    # ---- Getters ----
    def get_id(self) -> int:
        return self.__dataset_id

    def get_name(self) -> str:
        return self.__name

    def get_source(self) -> str:
        return self.__source

    def get_category(self) -> str:
        return self.__category

    def get_size(self) -> int:
        return self.__size

    # ---- Helper methods ----
    def size_kb(self) -> float:
        """Return dataset size in KB (rough conversion)."""
        return round(self.__size / 1024, 2)

    def size_mb(self) -> float:
        """Return dataset size in MB (rough conversion)."""
        return round(self.__size / (1024 * 1024), 2)

    def to_dict(self) -> dict:
        """Useful for converting objects into a dataframe."""
        return {
            "id": self.__dataset_id,
            "name": self.__name,
            "source": self.__source,
            "category": self.__category,
            "size": self.__size,
        }

    def __str__(self) -> str:
        return (
            f"Dataset(id={self.__dataset_id}, name={self.__name}, "
            f"category={self.__category}, size={self.__size})"
        )
