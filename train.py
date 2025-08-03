import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train foot traffic model")
    parser.add_argument("--train-path", type=str, required=True,
                        help="Path to training dataset (.pt)")
    parser.add_argument("--val-path", type=str, default=None,
                        help="Path to validation dataset (.pt)")
    parser.add_argument("--test-path", type=str, default=None,
                        help="Path to test dataset (.pt)")
    parser.add_argument("--batch-size", type=int, default=32,
                        help="Batch size for training")
    parser.add_argument("--max-epochs", type=int, default=10,
                        help="Number of epochs per trial")
    parser.add_argument("--n-trials", type=int, default=1,
                        help="Number of Optuna trials")
    parser.add_argument("--wandb-project", type=str, default="foot-traffic",
                        help="Weights & Biases project name")
    parser.add_argument("--wandb-offline", action="store_true",
                        help="Disable online W&B logging")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    import optuna
    import pytorch_lightning as pl
    from pytorch_lightning.loggers import WandbLogger

    from models.lightning.datamodule import FootTrafficDataModule
    from models.lightning.model import FootTrafficModel

    def objective(trial: optuna.trial.Trial) -> float:
        lr = trial.suggest_float("lr", 1e-4, 1e-1, log=True)
        hidden_dim = trial.suggest_int("hidden_dim", 32, 256)

        datamodule = FootTrafficDataModule(
            train_path=args.train_path,
            val_path=args.val_path,
            test_path=args.test_path,
            batch_size=args.batch_size,
        )

        model = FootTrafficModel(hidden_dim=hidden_dim, lr=lr)

        wandb_logger = WandbLogger(
            project=args.wandb_project,
            offline=args.wandb_offline,
            name=f"trial-{trial.number}",
            log_model=False,
        )

        trainer = pl.Trainer(max_epochs=args.max_epochs, logger=wandb_logger, enable_checkpointing=False)
        trainer.fit(model, datamodule=datamodule)

        metrics = trainer.callback_metrics
        val_loss = metrics.get("val_loss")
        if val_loss is None:
            return float("nan")
        return val_loss.item()

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=args.n_trials)

    best = study.best_trial
    print("Best trial:", best.number)
    print("Best parameters:", best.params)
    print("Best value:", best.value)


if __name__ == "__main__":
    main()
