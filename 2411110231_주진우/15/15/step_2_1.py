from pathlib import Path

import pandas as pd
from datakart import Ecos

from step_1_1 import OUT_DIR

ECOS_KEY = "GXV501YFI2LDZILCQJ29"

ecos = Ecos(ECOS_KEY)
resp = ecos.stat_search(
    stat_code="722Y001",
    freq="M",
    item_code1="0101000",
    start="201201",
    end="202506"
)

df_raw = pd.DataFrame(resp)
print(df_raw)
df_raw.to_csv(OUT_DIR / f"{Path(__file__).stem}.csv", index=False, encoding="utf-8-sig")