import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    from isfetphcalc import calc_ph
    return alt, calc_ph, mo, pd


@app.cell
def _(mo, pd):
    ph_df = pd.read_csv("data/ph_test.csv")
    ph_df['ts'] = pd.to_datetime(ph_df['pc_time'])
    ph_df.head(10)
    mo.ui.dataframe(ph_df)
    return (ph_df,)


@app.cell
def _(ph_df):
    ph_df_tris = ph_df
    ph_df_tris = ph_df_tris[ph_df_tris["ts"] > "2025-07-09T10:10"]
    ph_df_tris = ph_df_tris[ph_df_tris["ts"] < "2025-07-09T10:30"]
    ph_df_tris
    return (ph_df_tris,)


@app.cell
def _(alt, mo, ph_df_tris):
    chart = mo.ui.altair_chart(alt.Chart(ph_df_tris).mark_point().encode(
        x='ts',
        #y='vrse',
        y=alt.Y('vrse', scale=alt.Scale(zero=False))
    ))
    return (chart,)


@app.cell
def _(chart, mo):
    mo.vstack([chart, mo.ui.table(chart.value)])
    return


@app.cell
def _(ph_df_tris):
    # Calculate mean and standard deviation
    mean = ph_df_tris['vrse'].mean()
    std = ph_df_tris['vrse'].std()

    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std}")
    return (mean,)


@app.cell
def _(pd):
    temp_df = pd.read_csv("data/Tris_test_temperature_log.csv", skiprows=26)
    temp_df['ts'] = pd.to_datetime(temp_df['Time'])
    temp_df_tris = temp_df[temp_df["ts"] > "2025-07-09T10:10"]
    temp_df_tris = temp_df[temp_df["ts"] < "2025-07-09T10:30"]
    temp_df_tris
    temp_df_tris.columns
    return (temp_df_tris,)


@app.cell
def _(alt, mo, temp_df_tris):
    t_chart = mo.ui.altair_chart(alt.Chart(temp_df_tris).mark_point().encode(
        x='ts',
        y='Temp℃',
    ))
    return (t_chart,)


@app.cell
def _(mo, t_chart):
    mo.vstack([t_chart, mo.ui.table(t_chart.value)])
    return


@app.cell
def _(temp_df_tris):
    # Calculate mean and standard deviation
    t_mean = temp_df_tris['Temp℃'].mean()
    t_std = temp_df_tris['Temp℃'].std()

    print(f"Mean: {t_mean}")
    print(f"Standard Deviation: {t_std}")
    return


@app.cell
def _():
    sal = 33.7809
    return (sal,)


@app.cell
def _(calc_ph, mean, sal):
    ph_free, ph_total = calc_ph(mean, 0, 20.89, sal, -1.39469, -0.00107, 0)
    print(f"Calculated pH free: {ph_free}")
    print(f"Calculated pH total: {ph_total}")
    return


if __name__ == "__main__":
    app.run()
