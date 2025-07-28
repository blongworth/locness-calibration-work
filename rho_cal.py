import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    return alt, mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Load and process rhodamine""")
    return


@app.cell
def _(pd):
    df_rho = pd.read_csv("data/rho_cross_cal.csv")

    return (df_rho,)


@app.cell
def _(df_rho):
    df_rho.columns
    return


@app.cell
def _(df_rho):
    df_rho.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Calculating rho_ppb from voltage and gain

    Determine effective voltage and plot against std concentration

    Ve = V / gain
    """
    )
    return


@app.cell
def _(df_rho):
    df_rho["v_eff"] = df_rho['voltage'] / df_rho['gain']
    return


@app.cell
def _(alt, df_rho):
    alt.Chart(df_rho).mark_point().encode(
        y='concentration',
        x='v_eff'
    )
    return


@app.cell
def _(alt, df_rho):
    alt.Chart(df_rho).mark_point().encode(
        x='concentration',
        y='gain'
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Load and process test times""")
    return


app._unparsable_cell(
    r"""
    df_test_times = pd.read_excel(\"data/7_11_25_Test_Info.xlsx\",
                                  skiprows= 10,
                                  skipfooter=)
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
