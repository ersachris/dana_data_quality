import numpy as np

schema = {
    "business_id": np.str_,
    "name": np.str_,
    "address": np.str_,
    "city": np.str_,
    "state": np.str_,
    "postal_code": np.str_,
    "latitude": np.float32,
    "longitude": np.float32,
    "stars": np.float16,
    "review_count": np.uint32,
    "is_open": np.int8,
    "attributes": object,
    "categories": object,
    "hours": object
}