from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\adity\Downloads\faym\sql\dataset\transactions.csv")

plt.figure(figsize=(6,5))
plt.boxplot(df["transaction_amt"], vert=True)

plt.title("Box Plot of Transaction Amount")
plt.ylabel("Transaction Amount")

plt.grid(True)
plt.savefig(r"C:\Users\adity\Downloads\faym-agent\sql-analysis\charts\box_plot.png")
plt.show()