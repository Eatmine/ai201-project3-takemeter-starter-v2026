import pandas as pd

df = pd.read_csv("data/staff_posts.csv")
keys = {"a": "analysis", "h": "hot_take", "r": "reaction"}
labels = []

for i, row in df.iterrows():
    print(f"\n[{i+1}/30] {row['id']}\n{row['text']}")
    choice = ""
    while choice not in keys:
        choice = input("a = analysis, h = hot_take, r = reaction: ").strip().lower()
    labels.append(keys[choice])

df["label"] = labels
df.to_csv("my_staff_labels.csv", index=False)
print("\nSaved my_staff_labels.csv")
print(df["label"].value_counts())
