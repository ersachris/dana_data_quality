import numpy as np

schema = {
    "review_id": np.str_,
    "user_id": np.str_,
    "business_id": np.str_,
    "stars": np.float16,
    "date": np.str_,
    "text": np.str_,
    "useful": np.uint32,
    "funny": np.uint32,
    "cool": np.uint32,
}