import os
from typing import Optional

import torch
from torch.utils.data import DataLoader, TensorDataset
import pytorch_lightning as pl


class FootTrafficDataModule(pl.LightningDataModule):
    """Simple ``LightningDataModule`` for foot traffic datasets.

    Expects datasets saved as ``torch`` tensors via ``torch.save`` containing a
    tuple of ``(features, targets)``. Each path should point to a ``.pt`` file.
    """

    def __init__(self, train_path: str, val_path: Optional[str] = None,
                 test_path: Optional[str] = None, batch_size: int = 32) -> None:
        super().__init__()
        self.train_path = train_path
        self.val_path = val_path
        self.test_path = test_path
        self.batch_size = batch_size

        self.train_dataset: Optional[TensorDataset] = None
        self.val_dataset: Optional[TensorDataset] = None
        self.test_dataset: Optional[TensorDataset] = None

    def _load_dataset(self, path: str) -> TensorDataset:
        """Load a dataset from ``path`` expecting ``torch.save`` format."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found: {path}")
        data = torch.load(path)
        if isinstance(data, tuple) and len(data) == 2:
            x, y = data
            return TensorDataset(x, y)
        raise ValueError("Dataset file must contain a tuple of (features, targets)")

    def setup(self, stage: Optional[str] = None) -> None:  # type: ignore[override]
        if stage == 'fit' or stage is None:
            self.train_dataset = self._load_dataset(self.train_path)
            if self.val_path:
                self.val_dataset = self._load_dataset(self.val_path)
        if stage == 'test' or stage is None:
            if self.test_path:
                self.test_dataset = self._load_dataset(self.test_path)

    def train_dataloader(self) -> DataLoader:  # type: ignore[override]
        if self.train_dataset is None:
            raise RuntimeError("DataModule not setup. Call setup('fit') first.")
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self) -> Optional[DataLoader]:  # type: ignore[override]
        if self.val_dataset is None:
            return None
        return DataLoader(self.val_dataset, batch_size=self.batch_size)

    def test_dataloader(self) -> Optional[DataLoader]:  # type: ignore[override]
        if self.test_dataset is None:
            return None
        return DataLoader(self.test_dataset, batch_size=self.batch_size)
