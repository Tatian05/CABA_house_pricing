from ingesta import ingesta
from transformation import transformation
from normalization import normalization

raw_df = ingesta()
processed_df = transformation(raw_df)
normalization(processed_df)