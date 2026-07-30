import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv(r"C:\Users\adity\Downloads\faym-agent\sql-analysis\dataset\transactions.csv")

# Plot histogram (Bell Curve approximation)
plt.figure(figsize=(8,5))
plt.hist(df["transaction_amt"], bins=30, density=True)

plt.title("Bell Curve of Transaction Amount")
plt.xlabel("Transaction Amount")
plt.ylabel("Density")

plt.grid(True)
plt.savefig(r"C:\Users\adity\Downloads\faym-agent\sql-analysis\charts\bell_curve.png")
plt.show()