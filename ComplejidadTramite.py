import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("Effor_index_MASTER.csv")

mapa_fijo = {
    "nivel 1": 1,
    "nivel 2": 2,
    "nivel 3.1": 3,
    "nivel 3.2": 4,
    "nivel 3.3": 5,
    "nivel 3.4": 6,
    "nivel 3.5": 7,
    "nivel 3.6": 8,
    "nivel 3.7": 9,
    "nivel 3.8": 10,
    "nivel 3.9": 11,
    "nivel 4.1": 12,
    "nivel 4.2": 13,
    "nivel 4.3": 14
}

df["nivel_digitalizacion_numT"] = (
    df["nivel_digitalizacion"]
    .str.lower()
    .str.strip()
    .map(mapa_fijo)
)

df["nivel_digitalizacion_num"] = df["nivel_digitalizacion_numT"].fillna(0)
df["Tiempo_en_minutos"] = df["Tiempo_en_minutos"].fillna(0)

# Crear nueva columna con la suma
df["suma_N"] = df["N_FORMATOS_FINAL"] + df["CONTEO_NETO"]

# Columna de existencia de costo
df["costo"] = df["TraCosto"].map({"VERDADERO": 1, "FALSO": 0})

# Crear gráfico 3D
# fig = px.scatter_3d(
#    df,
#    x="nivel_digitalizacion_num",
#    y="suma_N",
#    z="Tiempo_en_minutos",
#    color="nivel_digitalizacion_num",  # opcional
#    title="Relación 3D entre nivel, suma y tiempo"
#)

# Guardar como HTML interactivo
#fig.write_html("grafico_3d_interactivo.html")

# Mostrar en notebook (opcional)
#fig.show()

corr = df[["nivel_digitalizacion_num", "suma_N", "Tiempo_en_minutos","costo"]].corr(method="spearman")
print(corr.to_string())

#plt.scatter(df["Tiempo_en_minutos"], df["suma_N"])
#plt.xlabel("Nivel")
#plt.ylabel("Tiempo")

#plt.savefig("grafico3.png")

#X = df[[
 #   "suma_N",
  #  "Tiempo_en_minutos",
   # "nivel_digitalizacion_num"
#]].dropna()

#from sklearn.preprocessing import StandardScaler

#scaler = StandardScaler()
#X_scaled = scaler.fit_transform(X)

#from sklearn.decomposition import PCA

#pca = PCA(n_components=1)
#complejidad = pca.fit_transform(X_scaled)

#df.loc[X.index, "Complejidad_PCA"] = complejidad
#print("--------------------------")
#print(pca.components_)

#print(pca.explained_variance_ratio_)

def agrupar_nivel(x):
    if x <= 2:
        return x
    elif 3 <= x <= 11:
        return 3
    else:
        return 4

df["nivel_dig_grupo"] = df["nivel_digitalizacion_num"].apply(agrupar_nivel)

X = df[[
    "suma_N",
    "Tiempo_en_minutos",
    "nivel_digitalizacion_num",
    "costo"
]].dropna()

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

from sklearn.decomposition import PCA

#pca = PCA(n_components=1)
#complejidad = pca.fit_transform(X_scaled)

#df.loc[X.index, "Complejidad_PCA"] = complejidad
#print("--------------------------")
#print(pca.components_)

#print(pca.explained_variance_ratio_)
#print("--------------------------")

#df["Complejidad_PCA_norm"] = (
 #   (df["Complejidad_PCA"] - df["Complejidad_PCA"].min()) /
  #  (df["Complejidad_PCA"].max() - df["Complejidad_PCA"].min())
#)

#df[["Complejidad_PCA_norm", "Tiempo_en_minutos", "suma_N"]].sort_values("Complejidad_PCA_norm")

#df[["Complejidad_PCA_norm"]].to_csv("complejidad.csv", index=False)

#fig = px.scatter_3d(
 #   df,
  #  x="suma_N",
   # y="Tiempo_en_minutos",
    #z="nivel_dig_grupo",
    #color="Complejidad_PCA_norm"
#)

#fig.show()

#corrC = df[["Complejidad_PCA_norm","nivel_dig_grupo", "suma_N", "Tiempo_en_minutos","costo"]].corr(method="spearman")
#print(corrC.to_string())

pca = PCA(n_components=4)
pca.fit(X_scaled)
print(pca.explained_variance_ratio_)

print(pca.components_)

components = pca.fit_transform(X_scaled)

df.loc[X.index, "PC1"] = components[:, 0]
df.loc[X.index, "PC2"] = components[:, 1]
df.loc[X.index, "PC3"] = components[:, 2]

df["Complejidad_total"] = (
    0.324 * df["PC1"] +
    0.253 * df["PC2"] +
    0.230 * df["PC3"]
)

min_val = df["Complejidad_total"].min()
max_val = df["Complejidad_total"].max()

df["Complejidad_norm"] = (
    df["Complejidad_total"] - min_val
) / (max_val - min_val)

fig = px.scatter_3d(
    df,
    x="suma_N",
    y="Tiempo_en_minutos",
    z="nivel_digitalizacion_num",
    color="Complejidad_norm"
)

fig.show()

CorrC3 = df[["Complejidad_norm","nivel_digitalizacion_num", "suma_N", "Tiempo_en_minutos","costo"]].corr(method="spearman")
print(CorrC3.to_string())

CorrC3P = df[["Complejidad_norm","nivel_digitalizacion_num", "suma_N", "Tiempo_en_minutos","costo"]].corr(method="pearson")
print(CorrC3P.to_string())

print(df[["nivel_digitalizacion_num", "Tiempo_en_minutos"]].corr())

df[["Complejidad_norm"]].to_csv("complejidad3.csv", index=False)

fig = px.scatter_3d(
    df,
    x=df["PC1"],
    y=df["PC2"],
    z=df["PC3"]
)

fig.show()

#plt.scatter(df["PC1"], df["PC2"], alpha=0.6)
#plt.xlabel("Complejidad operativa (PC1)")
#plt.ylabel("Complejidad administrativa (PC2)")
#plt.zlabel("Complejidad")

#plt.savefig("grafico_pca.png", dpi=300)