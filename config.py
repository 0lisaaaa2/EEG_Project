# Default settings for data processing and analysis.

from collections.abc import Callable, Sequence
from typing import Annotated, Any, Literal

from annotated_types import Ge, Interval, Len, MinLen
from mne import Covariance
from mne_bids import BIDSPath

#from mne_bids_pipeline.typing import (
#     ArbitraryContrast,
#     DigMontageType,
#     FloatArrayLike,
#     PathLike,
#)

bids_root = "ds005841-download"
deriv_root = "output/ds005841"