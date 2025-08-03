from typing import Any

import torch
from torch import nn
import torch.nn.functional as F
import pytorch_lightning as pl


class FootTrafficModel(pl.LightningModule):
    """Simple feed-forward network for regression tasks."""

    def __init__(self, input_dim: int = 10, hidden_dim: int = 64, lr: float = 1e-3):
        super().__init__()
        self.save_hyperparameters()

        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        return self.model(x)

    def training_step(self, batch: Any, batch_idx: int) -> torch.Tensor:  # type: ignore[override]
        x, y = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch: Any, batch_idx: int) -> torch.Tensor:  # type: ignore[override]
        x, y = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)
        self.log("val_loss", loss, prog_bar=True)
        return loss

    def configure_optimizers(self):  # type: ignore[override]
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)
