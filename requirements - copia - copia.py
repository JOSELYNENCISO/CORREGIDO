import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Levantamiento de alturas")

archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo is not None:

    df = pd.read_excel(archivo)

    df["Altura"] = pd.to_numeric(df["Altura"], errors='coerce')

    def clasificar(h):
        if pd.isna(h):
            return "Sin dato"
        elif h >= 14:
            return "Óptimo"
        elif h >= 10:
            return "Corto"
        elif h >= 6:
            return "Crítico"
        else:
            return "Tapado"

    df["Categoria"] = df["Altura"].apply(clasificar)

    n_puntos = len(df)

    # ===== TAMAÑOS =====
    if n_puntos > 120:
        size_punto = 18
        size_texto = 4
    elif n_puntos > 80:
        size_punto = 35
        size_texto = 6
    elif n_puntos > 40:
        size_punto = 70
        size_texto = 8
    else:
        size_punto = 110
        size_texto = 10

    colores = {
        "Óptimo": "green",
        "Corto": "yellow",
        "Crítico": "orange",
        "Tapado": "red",
        "Sin dato": "black"
    }

    nombres = {
        "Óptimo": "Óptimo (>=14 m)",
        "Corto": "Corto (10–14 m)",
        "Crítico": "Crítico (6–10 m)",
        "Tapado": "Tapado (<6 m)",
        "Sin dato": "Sin dato (-)"
    }

    if st.button("🔘 Generar gráfico"):

        # ===== DETECTAR FORMA REAL =====
        rango_x = df["X"].max() - df["X"].min()
        rango_y = df["Y"].max() - df["Y"].min()

        proporcion = rango_x / rango_y

        ancho = 18
        alto = max(8, ancho / proporcion)

        fig, ax = plt.subplots(figsize=(ancho, alto))

        # ===== PUNTOS =====
        for cat in colores:
            sub = df[df["Categoria"] == cat]
            cantidad = len(sub)

            ax.scatter(
                sub["X"],
                sub["Y"],
                c=colores[cat],
                label=f"{nombres[cat]} - {cantidad}",
                s=size_punto,
                edgecolors='none'
            )

        # ===== OFFSET =====
        offset = rango_y * 0.012

        # ===== IDs =====
        for _, row in df.iterrows():
            ax.text(
                row["X"],
                row["Y"] + offset,
                str(row["ID"]),
                fontsize=size_texto,
                ha='center',
                va='bottom',
                fontweight='bold',
                rotation=35
            )

        ax.set_title(
            "Plano de Taladros",
            fontsize=18,
            fontweight='bold'
        )

        ax.set_xticks([])
        ax.set_yticks([])

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(False)

        margen_x = rango_x * 0.05
        margen_y = rango_y * 0.08

        ax.set_xlim(
            df["X"].min() - margen_x,
            df["X"].max() + margen_x
        )

        ax.set_ylim(
            df["Y"].min() - margen_y,
            df["Y"].max() + margen_y
        )

        ax.set_aspect('equal')

        ax.legend(
            loc='upper left',
            bbox_to_anchor=(1.01, 1),
            frameon=False
        )

        plt.tight_layout()

        st.pyplot(fig)

        fig.savefig(
            "grafico.png",
            dpi=600,
            bbox_inches='tight'
        )

        with open("grafico.png", "rb") as file:
            st.download_button(
                "⬇️ Descargar imagen",
                file,
                "grafico_taladros.png"
            )