import json
import pandas as pd

# 1. Lecture
df = pd.read_csv("data/logs_reseau.csv")
print("Avant nettoyage :", len(df), "lignes")

# 2. Nettoyage
df = df.drop_duplicates()
df["protocol"] = df["protocol"].str.upper()
mediane = df["bytes_sent"].median()
df["bytes_sent"] = df["bytes_sent"].fillna(mediane)
print("Après nettoyage :", len(df), "lignes")

# 3. Résultats
resultats = {
    "nb_lignes_apres_nettoyage": int(len(df)),
    "top_port": int(df["dst_port"].value_counts().idxmax()),
    "taux_deny_pct": round(float((df["action"] == "DENY").mean() * 100), 2),
    "ip_scanner": str(df.groupby("src_ip")["dst_port"].nunique().idxmax()),
    "ip_exfiltration": str(df.groupby("src_ip")["bytes_sent"].sum().idxmax()),
}

with open("resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

print(resultats)
import os
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

# Figure 1 : top 10 des ports
top = df["dst_port"].value_counts().head(10)
plt.figure(figsize=(8, 5))
plt.bar(top.index.astype(str), top.values, color="steelblue")
plt.title("Top 10 des ports de destination")
plt.xlabel("Port de destination")
plt.ylabel("Nombre de connexions")
plt.tight_layout()
plt.savefig("figures/top_ports.png", dpi=120)
plt.close()

# Figure 2 : répartition ALLOW / DENY
rep = df["action"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(rep.values, labels=rep.index, autopct="%1.1f%%", colors=["seagreen", "crimson"])
plt.title("Répartition ALLOW / DENY")
plt.tight_layout()
plt.savefig("figures/allow_deny.png", dpi=120)
plt.close()

# Figure 3 : octets envoyés par type d'appareil
vol = df.groupby("device_type")["bytes_sent"].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
plt.bar(vol.index, vol.values, color="darkorange")
plt.title("Volume total d'octets envoyés par type d'appareil")
plt.xlabel("Type d'appareil")
plt.ylabel("Octets envoyés")
plt.tight_layout()
plt.savefig("figures/octets_par_appareil.png", dpi=120)
plt.close()

# Figure 4 : ports distincts contactés par IP (preuve du scan)
ports = df.groupby("src_ip")["dst_port"].nunique().sort_values(ascending=False).head(10)
plt.figure(figsize=(9, 5))
plt.barh(ports.index[::-1], ports.values[::-1], color="purple")
plt.title("Top 10 des IP par nombre de ports distincts contactés")
plt.xlabel("Ports distincts")
plt.ylabel("IP source")
plt.tight_layout()
plt.savefig("figures/ports_distincts_par_ip.png", dpi=120)
plt.close()

# Figure 5 : octets envoyés par IP (preuve de l'exfiltration)
octets = df.groupby("src_ip")["bytes_sent"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(9, 5))
plt.barh(octets.index[::-1], octets.values[::-1], color="firebrick")
plt.title("Top 10 des IP par total d'octets envoyés")
plt.xlabel("Octets envoyés")
plt.ylabel("IP source")
plt.tight_layout()
plt.savefig("figures/octets_par_ip.png", dpi=120)
plt.close()