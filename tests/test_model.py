import torch

from models.lightning.model import FootTrafficModel


def test_forward_output_shape():
    model = FootTrafficModel(input_dim=4, hidden_dim=8)
    x = torch.randn(3, 4)
    y = model(x)
    assert y.shape == (3, 1)


def test_training_step_returns_loss():
    model = FootTrafficModel(input_dim=4, hidden_dim=8)
    x = torch.randn(3, 4)
    y = torch.randn(3, 1)
    loss = model.training_step((x, y), 0)
    assert loss.dim() == 0  # scalar tensor
