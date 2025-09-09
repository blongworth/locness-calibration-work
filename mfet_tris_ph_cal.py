import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This notebook contains analysis of pre- and post- LOC02 calibration data for MBARI mFET005 in ESL seawater and TRIS buffer solution.""")
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import numpy as np
    from isfetphcalc import calc_ph
    import glob
    return alt, calc_ph, glob, mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Pre-LOC02 calibration""")
    return


@app.cell
def _(mo, pd):
    ph_df = pd.read_csv("data/ph_test.csv")
    ph_df["ts"] = pd.to_datetime(ph_df["pc_time"])
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
    def _():
        chart = mo.ui.altair_chart(
            alt.Chart(ph_df_tris)
            .mark_point()
            .encode(
                x="ts",
                # y='vrse',
                y=alt.Y("vrse", scale=alt.Scale(zero=False)),
            )
        )
        return chart


    _()
    return


@app.cell
def _(ph_df_tris):
    # Calculate mean and standard deviation
    mean = ph_df_tris["vrse"].mean()
    std = ph_df_tris["vrse"].std()

    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std}")
    return


@app.cell
def _(pd):
    temp_df = pd.read_csv("data/Tris_test_temperature_log.csv", skiprows=26)
    temp_df["ts"] = pd.to_datetime(temp_df["Time"])
    temp_df_tris = temp_df[temp_df["ts"] > "2025-07-09T10:10"]
    temp_df_tris = temp_df[temp_df["ts"] < "2025-07-09T10:30"]
    temp_df_tris
    temp_df_tris.columns
    return (temp_df_tris,)


@app.cell
def _(alt, temp_df_tris):
    t_chart = (
        alt.Chart(temp_df_tris)
        .mark_point()
        .encode(x="ts", y=alt.Y("Temp℃", scale=alt.Scale(zero=False)))
    )
    t_chart
    return


@app.cell
def _(mo):
    mo.md(r"""try plotting temp vs vrse""")
    return


@app.cell
def _(ph_df_tris, temp_df_tris):
    # Select 'ts' and 'Temp℃', rename to 'temp'
    temp_df_sel = temp_df_tris[["ts", "Temp℃"]].rename(columns={"Temp℃": "temp"})
    # Resample temp_df_sel to match ph_df_tris['ts']
    temp_df_sel = (
        temp_df_sel.set_index("ts")
        .reindex(ph_df_tris["ts"], method="nearest")
        .reset_index()
    )
    # Join with ph_df_tris on 'ts'
    df_tris_pre = ph_df_tris.merge(temp_df_sel, on="ts", how="left")
    df_tris_pre.head()
    return (df_tris_pre,)


@app.cell
def _(mo):
    mo.md(r"""need TRIS sal""")
    return


@app.cell
def _(temp_df_tris):
    # Calculate mean and standard deviation
    t_mean = temp_df_tris["Temp℃"].mean()
    t_std = temp_df_tris["Temp℃"].std()

    print(f"Mean: {t_mean}")
    print(f"Standard Deviation: {t_std}")
    return


@app.cell
def _():
    pre_sal = 33.7809
    k0 = -1.39469
    k02 = -1.39442868762104
    k2 = -0.00107
    return k0, k02, k2, pre_sal


@app.cell
def _(calc_ph, df_tris_pre, k0, k02, k2, pre_sal):
    df_tris_pre["ph_free_calc"], df_tris_pre["ph_total_calc"] = calc_ph(
        df_tris_pre["vrse"], 0, df_tris_pre["temp"], pre_sal, k0, k2, 0
    )
    df_tris_pre["ph_free_calc2"], df_tris_pre["ph_total_calc2"] = calc_ph(
        df_tris_pre["vrse"], 0, df_tris_pre["temp"], pre_sal, k02, k2, 0
    )
    print(f"Calculated pH free: {df_tris_pre['ph_free_calc'].mean()}")
    print(f"Calculated pH total: {df_tris_pre['ph_total_calc'].mean()}")
    print(f"Calculated pH total sd: {df_tris_pre['ph_total_calc'].std()}")
    print(f"Calculated pH total with new k0: {df_tris_pre['ph_total_calc2'].mean()}")
    print(
        f"pH difference due to k0: {df_tris_pre['ph_total_calc2'].mean() - df_tris_pre['ph_total_calc'].mean()}"
    )
    return


@app.cell
def _(alt, df_tris_pre):
    ph_chart = (
        alt.Chart(df_tris_pre)
        .mark_point()
        .encode(
            x="ts",
            y=alt.Y("ph_total_calc", scale=alt.Scale(zero=False)),
        )
    )

    ph_chart2 = (
        alt.Chart(df_tris_pre)
        .mark_point(color="lightgreen")
        .encode(
            x="ts",
            y=alt.Y("ph_total_calc2", scale=alt.Scale(zero=False)),
        )
    )

    # Horizontal line at y=50
    horizontal_line = (
        alt.Chart()
        .mark_rule(color="lightblue")
        .encode(
            y=alt.datum(8.0936)  # Sets y to constant value 50
        )
    )

    # Combine them
    ph_chart + ph_chart2 + horizontal_line
    return


@app.cell
def _(alt, df_tris_pre):
    alt.Chart(df_tris_pre).mark_point().encode(
        y=alt.Y("ph_total_calc", scale=alt.Scale(zero=False)),
        x=alt.X("temp", scale=alt.Scale(zero=False)),
    )
    return


@app.cell
def _(df_tris_pre, np):
    vrse = np.repeat(df_tris_pre["vrse"].mean(), 11)
    len(vrse)
    return (vrse,)


@app.cell
def _(df_tris_pre, np):
    temp = df_tris_pre["temp"].mean()
    salt = np.linspace(25, 35, 11)
    len(salt)
    return salt, temp


@app.cell
def _(alt, calc_ph, pd, salt, temp, vrse):
    ph_free, ph = calc_ph(vrse, 0, temp, salt, -1.39469, -0.00107, 0)

    alt.Chart(pd.DataFrame({"salinity": salt, "ph": ph})).mark_line().encode(
        x="salinity", y=alt.Y("ph", scale=alt.Scale(zero=False))
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Post-LOC02 Calibration""")
    return


@app.cell
def _(mo):
    mo.md(r"""## ESL seawater""")
    return


@app.cell
def _(calc_ph, glob, k0, k2, pd):
    # read serial dump of mFET data
    esl_post_df = pd.read_table(
        "data/loc02_post_cal_cond.txt", skiprows=list(range(96)) + list(range(372, 467))
    )
    esl_post_df.rename(columns={esl_post_df.columns[1]: "datetime_utc"}, inplace=True)
    esl_post_df["datetime_utc"] = pd.to_datetime(esl_post_df["datetime_utc"])
    esl_post_df.columns = esl_post_df.columns.str.strip()

    # Add temp and sal data from ctd
    # read CTD data
    ctd_post_files = glob.glob("data/CTD_FSW*.csv")
    dfs = [pd.read_csv(f, skiprows=1) for f in ctd_post_files]
    esl_post_ctd = pd.concat(dfs, ignore_index=True)
    esl_post_ctd["datetime_utc"] = pd.to_datetime(esl_post_ctd['Time'])
    esl_post_ctd.drop_duplicates(inplace=True)
    esl_post_ctd = (
        esl_post_ctd.set_index('datetime_utc')
    )

    # Join with esl_post_df
    esl_post = esl_post_df.merge(esl_post_ctd, on="datetime_utc", how="left")

    # add calculated pH
    esl_post["ph_total"] = calc_ph(esl_post["Vrse"], 0, esl_post['Temperature'], esl_post['Salinity'], k0, k2, 0)[1]

    # take a look
    esl_post
    return (esl_post,)


@app.cell
def _(alt, esl_post):
    chart = (
        alt.Chart(esl_post)
        .mark_point(size=8)  # trail allows gradient coloring
        .encode(
            x=alt.X("datetime_utc:T", title="Date / Time"),
            y=alt.Y("ph_total:Q", title="Total pH", scale=alt.Scale(zero=False)),
            color=alt.Color("Temperature", scale=alt.Scale(scheme="viridis")),
        )
        .interactive()
    )
    chart
    return


@app.cell
def _(esl_post, mo):
    # Dropdown widget (values are DataFrame columns you want to plot)
    y_var = mo.ui.dropdown(
        options=esl_post.columns, value="ph_total", label="Select Y-axis variable"
    )
    y_var
    return (y_var,)


@app.cell
def _(alt, esl_post, y_var):
    (alt.Chart(esl_post)
    .mark_point(size=8)  # trail allows gradient coloring
    .encode(
        x=alt.X("datetime_utc:T", title="Date / Time"),
        y=alt.Y(f"{y_var.value}:Q", title=y_var.value, scale=alt.Scale(zero=False)),
    )
    .interactive())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## TRIS Buffer""")
    return


@app.cell
def _(pd):
    tris_post = pd.read_csv("data/loc02_mFET_post_cal_tris.csv")
    tris_post["datetime_utc"] = pd.to_datetime(tris_post["datetime_utc"])#.dt.round('s')

    # read optode data for temp
    opt_df = pd.read_csv("data/post_tris_optode_temperature_data.csv")
    # Convert 'datetime' column to pandas datetime
    opt_df['datetime'] = pd.to_datetime(opt_df['datetime'])#.dt.round('s')

    # Select only 'datetime' and 'Temperature' columns
    _temp_df = opt_df[['datetime', 'Temperature']].rename(columns={'datetime': 'datetime_utc'})

    # merge to nearest time
    tris_post = pd.merge_asof(tris_post, _temp_df, on="datetime_utc", direction='nearest')
    return (tris_post,)


@app.cell
def _(calc_ph, k0, k2, tris_post):
    sal_tris_post = 33.7

    tris_post["ph_total_cal"] = calc_ph(tris_post["vrse"], 0, tris_post['Temperature'], sal_tris_post, k0, k2, 0)[1]
    return


@app.cell
def _(mo, tris_post):
    # Dropdown widget (values are DataFrame columns you want to plot)
    tris_y_var = mo.ui.dropdown(
        options=tris_post.columns, value="ph_total", label="Select Y-axis variable"
    )
    tris_y_var
    return (tris_y_var,)


@app.cell
def _(alt, tris_post, tris_y_var):
    (
        alt.Chart(tris_post)
        .mark_point(size=8)  # trail allows gradient coloring
        .encode(
            x=alt.X("datetime_utc:T", title="Date / Time"),
            y=alt.Y(f"{tris_y_var.value}:Q", title=tris_y_var.value, scale=alt.Scale(zero=False)),
        )
        .interactive()
    )

    return


@app.cell
def _(mo):
    mo.md(r"""TRIS buffer has a literature value of 8.094 -+ 0.006 @ 25C""")
    return


@app.cell
def _(np, pd, tris_post):
    _start_time = pd.Timestamp('2025-09-04 15:45:00')
    _end_time = pd.Timestamp('2025-09-04 19:00:00')
    filtered = tris_post[(tris_post['datetime_utc'] > _start_time) & (tris_post['datetime_utc'] < _end_time)]
    # Calculate mean and standard error of the mean (stderr) for 'value'
    mean_value = filtered['ph_total_cal'].mean()
    stderr_value = filtered['ph_total_cal'].std(ddof=1) / np.sqrt(filtered['ph_total_cal'].count())

    print(f"Mean: {mean_value:.5g}")
    print(f"Standard Error: {stderr_value:.2g}")

    return


if __name__ == "__main__":
    app.run()
