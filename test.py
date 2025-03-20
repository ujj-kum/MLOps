import pandas as pd
import os

data = [
    {"name": "Alice", "age": 25, "city": "Bhopal"},
    {"name": "Bob", "age": 30, "city": "Indore"},
    {"name": "Charlie", "age": 35, "city": "Mumbai"},
    {"name": "David", "age": 40, "city": "Pune"},
    {"name": "Eve", "age": 45, "city": "Delhi"}
    ]

df = pd.DataFrame(data=data, columns=["name", "age", "city"])
os.makedirs("data", exist_ok=True)
df.to_csv("data/data.csv", index=False)
