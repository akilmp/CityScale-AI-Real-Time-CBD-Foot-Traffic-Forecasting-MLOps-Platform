import torch
import pytest

from models.lightning.datamodule import FootTrafficDataModule


def create_dataset(path, num_samples=10, num_features=4):
    x = torch.randn(num_samples, num_features)
    y = torch.randn(num_samples, 1)
    torch.save((x, y), path)


def test_train_dataloader(tmp_path):
    data_path = tmp_path / "train.pt"
    create_dataset(data_path)
    dm = FootTrafficDataModule(str(data_path), batch_size=2)
    dm.setup('fit')
    loader = dm.train_dataloader()
    batch = next(iter(loader))
    features, targets = batch
    assert features.shape[0] == 2
    assert targets.shape[0] == 2
