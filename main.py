import csv
from datetime import datetime
from pathlib import Path

import numpy as np
import tensorflow as tf
from bentoml import BentoService, api, artifacts, env
from bentoml.adapters import JsonInput

HERE = Path(__file__).parent.resolve()


@artifacts([])
@env(requirements_txt_file="requirements/staging.txt")
class NewsService(BentoService):
    def __init__(self):
        super().__init__()
        self.index = tf.saved_model.load("recommender")
        self.topk_recommend = 3

    @api(input=JsonInput(), batch=False)
    def recommend(self, j_in):
        """
        input
            {
                "user_id": str 使用者 id
            }
        output
            {
                "news": List[str] 前三名推薦新聞標題,
            }
        """
        user_id = j_in.get("user_id")

        _, titles = self.index(np.array([str(user_id)]))
        return titles[0, : self.topk_recommend]

    @api(input=JsonInput(), btach=False)
    def record(self, j_in):
        """
        input
            {
                "user_id": str,
                "title": str
            }
        output
            {
                "timestamp": datetime,
                "user_id": str,
                "title": str,
            }
        """
        if not ("user_id" in j_in and "title" in j_in):
            return {"errors": "user_id and title required"}

        csv_path = HERE / "user_clicks.csv"
        with open(csv_path, "a") as fout:
            headers = ["timestamp", "user_id", "title"]
            writer = csv.DictWriter(fout, headers)
            with open(csv_path, "r") as fr:
                line = fr.readline()
            if "\n" not in line:
                writer.writeheader()
            row = {
                "timestamp": datetime.now().isoformat(),
                "user_id": j_in["user_id"],
                "title": j_in["title"],
            }
            writer.writerow(row)
        return row
