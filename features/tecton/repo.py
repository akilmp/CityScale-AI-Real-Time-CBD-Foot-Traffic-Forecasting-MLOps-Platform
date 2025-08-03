"""Utilities for initializing the Tecton client."""

import os
from typing import Optional

try:
    from tecton import TectonClient
except Exception:  # pragma: no cover - tecton may not be installed in CI
    TectonClient = None  # type: ignore


def get_tecton_client(url: Optional[str] = None, api_key: Optional[str] = None) -> "TectonClient":
    """Return an initialized :class:`TectonClient` instance.

    Parameters
    ----------
    url:
        Optional Tecton workspace URL. Defaults to the ``TECTON_URL`` environment variable.
    api_key:
        Optional Tecton API key. Defaults to the ``TECTON_API_KEY`` environment variable.

    Returns
    -------
    TectonClient
        An initialized Tecton client.

    Notes
    -----
    This helper defers importing and instantiating the Tecton client until runtime so that
    importing this module does not require the Tecton dependency to be installed. This makes
    unit testing and static analysis of the repository possible without access to Tecton.
    """

    if TectonClient is None:  # pragma: no cover - handled by try/except above
        raise RuntimeError("Tecton SDK is not installed. Install tecton-sdk to use this helper.")

    url = url or os.environ.get("TECTON_URL")
    api_key = api_key or os.environ.get("TECTON_API_KEY")

    if not url or not api_key:
        raise ValueError("TECTON_URL and TECTON_API_KEY must be set to initialize the client")

    return TectonClient(url, api_key)
