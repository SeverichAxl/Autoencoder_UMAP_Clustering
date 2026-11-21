"""
Experimento reproducible: Reducción de dimensionalidad (PCA vs. UMAP 2D) y
clustering con K-means sobre el dataset Wine (aprendizaje no supervisado).

Materia: SIS-351 Machine Learning — Grupo 3
Semilla global fija: 42
Regla de rigor: Las etiquetas reales de Wine NO se utilizan para escalar,
proyectar ni elegir k. Solo se calculan métricas externas (ARI/NMI) al final
como comparación externa declarada explícitamente.
"""

from __future__ import annotations

import os
import platform
import random
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
import umap
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler

# ==============================================================================
# 1. CONFIGURACIÓN GLOBAL Y REPRODUCIBILIDAD
# ==============================================================================

RANDOM_STATE = 42
K_CLUSTERS = 3
KMEANS_N_INIT = 20
UMAP_N_NEIGHBORS = 15
UMAP_MIN_DIST = 0.1

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTADOS_DIR = BASE_DIR / "resultados"


def fijar_semillas(semilla: int = RANDOM_STATE) -> None:
    """Fija las semillas globales para reproducibilidad."""
    os.environ["PYTHONHASHSEED"] = str(semilla)
    random.seed(semilla)
    np.random.seed(semilla)


# ==============================================================================
# 2. CARGA Y ESCALADO DE DATOS (SIN ETIQUETAS EN EL AJUSTE)
# ==============================================================================


def cargar_y_escalar_wine():
    """
    Carga el dataset Wine de scikit-learn y escala las 13 variables
    fisicoquímicas mediante StandardScaler (media 0, desviación estándar 1).
    """
    dataset = load_wine(as_frame=True)
    X = dataset.data
    y_externa = dataset.target  # Solo para referencia externa post-hoc
    nombres_clases_externas = list(dataset.target_names)

    scaler = StandardScaler()
    X_escalado = scaler.fit_transform(X)

    resumen = {
        "dataset": "Wine (scikit-learn)",
        "muestras_totales": int(X.shape[0]),
        "caracteristicas": int(X.shape[1]),
        "escalado": "StandardScaler (media=0, std=1)",
        "clases_externas_referencia": ", ".join(nombres_clases_externas),
        "random_state": RANDOM_STATE,
    }
    return X, X_escalado, y_externa, resumen


# ==============================================================================
# 3. JUSTIFICACIÓN NO SUPERVISADA DE k (MÉTODO DEL CODO + SILHOUETTE)
# ==============================================================================


def evaluar_rango_k(X_escalado: np.ndarray, k_min: int = 2, k_max: int = 6) -> pd.DataFrame:
    """
    Evalúa k en [k_min, k_max] usando únicamente X_escalado (sin etiquetas reales)
    para justificar la elección de k mediante inercia y Silhouette Score.
    """
    registros = []
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, n_init=KMEANS_N_INIT, random_state=RANDOM_STATE)
        etiquetas = km.fit_predict(X_escalado)
        sil = silhouette_score(X_escalado, etiquetas)
        registros.append(
            {
                "k": k,
                "Inercia": round(float(km.inertia_), 4),
                "Silhouette_Espacio_Escalado": round(float(sil), 4),
            }
        )
    return pd.DataFrame(registros)


# ==============================================================================
# 4. REPRESENTACIONES 2D (PCA Y UMAP) + CLUSTERING K-MEANS
# ==============================================================================


def ejecutar_representaciones_y_clustering(
    X_escalado: np.ndarray, y_externa: pd.Series
) -> tuple[np.ndarray, np.ndarray, KMeans, KMeans, pd.DataFrame, dict]:
    """
    Obtiene las proyecciones 2D con PCA y UMAP, aplica K-means con el mismo k=3
    en cada espacio, y calcula Silhouette Score (y ARI/NMI como comparación externa).
    """
    # 1) PCA 2D
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    Z_pca = pca.fit_transform(X_escalado)
    varianza_pca = pca.explained_variance_ratio_

    # 2) UMAP 2D
    reductor_umap = umap.UMAP(
        n_components=2,
        n_neighbors=UMAP_N_NEIGHBORS,
        min_dist=UMAP_MIN_DIST,
        random_state=RANDOM_STATE,
    )
    Z_umap = reductor_umap.fit_transform(X_escalado)

    # 3) K-means con el mismo k en cada representación 2D
    km_pca = KMeans(
        n_clusters=K_CLUSTERS, n_init=KMEANS_N_INIT, random_state=RANDOM_STATE
    )
    labels_pca = km_pca.fit_predict(Z_pca)

    km_umap = KMeans(
        n_clusters=K_CLUSTERS, n_init=KMEANS_N_INIT, random_state=RANDOM_STATE
    )
    labels_umap = km_umap.fit_predict(Z_umap)

    # 4) Métricas internas (no supervisadas) y comparación externa declarada
    sil_pca = silhouette_score(Z_pca, labels_pca)
    sil_umap = silhouette_score(Z_umap, labels_umap)

    ari_pca = adjusted_rand_score(y_externa, labels_pca)
    ari_umap = adjusted_rand_score(y_externa, labels_umap)

    nmi_pca = normalized_mutual_info_score(y_externa, labels_pca)
    nmi_umap = normalized_mutual_info_score(y_externa, labels_umap)

    df_metricas = pd.DataFrame(
        [
            {
                "Representacion": "PCA 2D (Lineal)",
                "k": K_CLUSTERS,
                "Silhouette_Score": round(float(sil_pca), 4),
                "Inercia_2D": round(float(km_pca.inertia_), 4),
                "ARI_Comparacion_Externa": round(float(ari_pca), 4),
                "NMI_Comparacion_Externa": round(float(nmi_pca), 4),
            },
            {
                "Representacion": "UMAP 2D (No lineal)",
                "k": K_CLUSTERS,
                "Silhouette_Score": round(float(sil_umap), 4),
                "Inercia_2D": round(float(km_umap.inertia_), 4),
                "ARI_Comparacion_Externa": round(float(ari_umap), 4),
                "NMI_Comparacion_Externa": round(float(nmi_umap), 4),
            },
        ]
    )

    info_pca = {
        "pc1_var": round(float(varianza_pca[0]) * 100, 2),
        "pc2_var": round(float(varianza_pca[1]) * 100, 2),
        "total_var": round(float(varianza_pca.sum()) * 100, 2),
    }

    return Z_pca, Z_umap, km_pca, km_umap, df_metricas, info_pca


# ==============================================================================
# 5. VISUALIZACIONES Y TRAZABILIDAD
# ==============================================================================


def graficar_seleccion_k(df_k: pd.DataFrame, ruta_salida: Path) -> None:
    """Genera gráfico de Codo (Inercia) y Silhouette para justificar k=3 sin etiquetas."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))

    axes[0].plot(df_k["k"], df_k["Inercia"], marker="o", linewidth=2, color="#1d4ed8")
    axes[0].axvline(K_CLUSTERS, color="#ef4444", linestyle="--", alpha=0.7, label=f"k elegido = {K_CLUSTERS}")
    axes[0].set_title("Método del Codo (Espacio Escalado)", fontsize=11.5, fontweight="bold")
    axes[0].set_xlabel("Número de clusters (k)")
    axes[0].set_ylabel("Inercia (SSE)")
    axes[0].set_xticks(df_k["k"])
    axes[0].legend()
    axes[0].grid(alpha=0.25)

    axes[1].plot(
        df_k["k"],
        df_k["Silhouette_Espacio_Escalado"],
        marker="s",
        linewidth=2,
        color="#059669",
    )
    axes[1].axvline(K_CLUSTERS, color="#ef4444", linestyle="--", alpha=0.7, label=f"k elegido = {K_CLUSTERS}")
    axes[1].set_title("Silhouette Score por k (Sin Etiquetas)", fontsize=11.5, fontweight="bold")
    axes[1].set_xlabel("Número de clusters (k)")
    axes[1].set_ylabel("Silhouette Score")
    axes[1].set_xticks(df_k["k"])
    axes[1].legend()
    axes[1].grid(alpha=0.25)

    plt.suptitle("Justificación No Supervisada de k — Dataset Wine", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
    plt.close(fig)


def graficar_clusters_lado_a_lado(
    Z_pca: np.ndarray,
    Z_umap: np.ndarray,
    km_pca: KMeans,
    km_umap: KMeans,
    df_metricas: pd.DataFrame,
    info_pca: dict,
    ruta_salida: Path,
) -> None:
    """Genera los gráficos obligatorios de clusters en PCA 2D y UMAP 2D lado a lado."""
    sil_pca = df_metricas.loc[0, "Silhouette_Score"]
    sil_umap = df_metricas.loc[1, "Silhouette_Score"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.0))
    paleta = ["#2563eb", "#10b981", "#f59e0b"]

    # PCA 2D
    for cid in range(K_CLUSTERS):
        mask = km_pca.labels_ == cid
        axes[0].scatter(
            Z_pca[mask, 0],
            Z_pca[mask, 1],
            s=48,
            alpha=0.85,
            color=paleta[cid],
            label=f"Cluster {cid}",
        )
    axes[0].scatter(
        km_pca.cluster_centers_[:, 0],
        km_pca.cluster_centers_[:, 1],
        s=180,
        c="#0f172a",
        marker="X",
        label="Centroides",
    )
    axes[0].set_title(
        f"K-means (k={K_CLUSTERS}) en PCA 2D\nSilhouette = {sil_pca:.4f} | Var. explicada = {info_pca['total_var']}%",
        fontsize=11.5,
        fontweight="bold",
    )
    axes[0].set_xlabel(f"PC1 ({info_pca['pc1_var']}%)")
    axes[0].set_ylabel(f"PC2 ({info_pca['pc2_var']}%)")
    axes[0].legend(loc="best", fontsize=9)
    axes[0].grid(alpha=0.2)

    # UMAP 2D
    for cid in range(K_CLUSTERS):
        mask = km_umap.labels_ == cid
        axes[1].scatter(
            Z_umap[mask, 0],
            Z_umap[mask, 1],
            s=48,
            alpha=0.85,
            color=paleta[cid],
            label=f"Cluster {cid}",
        )
    axes[1].scatter(
        km_umap.cluster_centers_[:, 0],
        km_umap.cluster_centers_[:, 1],
        s=180,
        c="#0f172a",
        marker="X",
        label="Centroides",
    )
    axes[1].set_title(
        f"K-means (k={K_CLUSTERS}) en UMAP 2D\nSilhouette = {sil_umap:.4f} (n_neighbors={UMAP_N_NEIGHBORS}, min_dist={UMAP_MIN_DIST})",
        fontsize=11.5,
        fontweight="bold",
    )
    axes[1].set_xlabel("UMAP 1")
    axes[1].set_ylabel("UMAP 2")
    axes[1].legend(loc="best", fontsize=9)
    axes[1].grid(alpha=0.2)

    plt.suptitle(
        "Comparación de Clusters en Representaciones 2D — Wine (StandardScaler, n=178)",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
    plt.close(fig)


def graficar_comparacion_silhouette(df_metricas: pd.DataFrame, ruta_salida: Path) -> None:
    """Genera gráfico de barras comparando el Silhouette Score en PCA vs. UMAP."""
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    colores = ["#3b82f6", "#10b981"]
    bars = ax.bar(
        df_metricas["Representacion"],
        df_metricas["Silhouette_Score"],
        color=colores,
        width=0.5,
    )
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Silhouette Score")
    ax.set_title(
        f"Silhouette Score por Representación 2D (K-means, k={K_CLUSTERS})",
        fontsize=12,
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.25)

    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.02,
            f"{h:.4f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)


def guardar_trazabilidad_entorno(ruta_salida: Path, info_pca: dict) -> None:
    """Documenta versiones, semillas e hiperparámetros exactos para reproducibilidad."""
    lineas = [
        "=== REGISTRO DE TRAZABILIDAD DEL ENTORNO (GRUPO 3) ===",
        f"Sistema Operativo : {platform.system()} {platform.release()}",
        f"Python            : {sys.version.split()[0]}",
        f"scikit-learn      : {sklearn.__version__}",
        f"umap-learn        : {umap.__version__}",
        f"NumPy             : {np.__version__}",
        f"Pandas            : {pd.__version__}",
        f"Semilla global    : {RANDOM_STATE}",
        f"Dataset           : Wine (178 muestras, 13 variables, StandardScaler)",
        f"K-means           : k={K_CLUSTERS}, n_init={KMEANS_N_INIT}, random_state={RANDOM_STATE}",
        f"PCA 2D            : var_PC1={info_pca['pc1_var']}%, var_PC2={info_pca['pc2_var']}%, total={info_pca['total_var']}%",
        f"UMAP 2D           : n_neighbors={UMAP_N_NEIGHBORS}, min_dist={UMAP_MIN_DIST}, random_state={RANDOM_STATE}",
    ]
    ruta_salida.write_text("\n".join(lineas), encoding="utf-8")


# ==============================================================================
# 6. PUNTO DE ENTRADA PRINCIPAL
# ==============================================================================


def main() -> None:
    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
    fijar_semillas(RANDOM_STATE)

    print("1. Cargando y escalando el dataset Wine (StandardScaler)...")
    _, X_escalado, y_externa, resumen = cargar_y_escalar_wine()
    pd.DataFrame([resumen]).to_csv(RESULTADOS_DIR / "resumen_dataset.csv", index=False)

    print("2. Evaluando rango k=2..6 sin usar etiquetas reales para justificar k...")
    df_k = evaluar_rango_k(X_escalado, k_min=2, k_max=6)
    df_k.to_csv(RESULTADOS_DIR / "seleccion_k.csv", index=False)

    print("3. Calculando PCA 2D, UMAP 2D y aplicando K-means (k=3)...")
    Z_pca, Z_umap, km_pca, km_umap, df_metricas, info_pca = (
        ejecutar_representaciones_y_clustering(X_escalado, y_externa)
    )
    df_metricas.to_csv(RESULTADOS_DIR / "tabla_metricas_comparativas.csv", index=False)

    print("4. Exportando gráficos y trazabilidad a /resultados...")
    graficar_seleccion_k(df_k, RESULTADOS_DIR / "seleccion_k.png")
    graficar_clusters_lado_a_lado(
        Z_pca,
        Z_umap,
        km_pca,
        km_umap,
        df_metricas,
        info_pca,
        RESULTADOS_DIR / "clusters_pca_umap.png",
    )
    graficar_comparacion_silhouette(
        df_metricas, RESULTADOS_DIR / "comparacion_silhouette.png"
    )
    guardar_trazabilidad_entorno(RESULTADOS_DIR / "entorno.txt", info_pca)

    print("\n=== SELECCIÓN DE k (SIN ETIQUETAS) ===")
    print(df_k.to_string(index=False))

    print("\n=== RESULTADOS COMPARATIVOS PCA 2D vs. UMAP 2D ===")
    print(df_metricas.to_string(index=False))
    print(f"\nEvidencias guardadas exitosamente en: {RESULTADOS_DIR}")


if __name__ == "__main__":
    main()
