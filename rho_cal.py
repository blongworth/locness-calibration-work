import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import polars as pl
    import numpy as np
    return alt, mo, np, pd


@app.cell
def _(mo):
    mo.md(
        r"""
    # Cross-Calibration

    Data from a flow-through test of several sensors. Rho conc was increased through the test by volumetrically adding rho stock solution.

    Sensor was not using a proper calibration for this test- use voltage and gain, not conc.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Load and process rhodamine""")
    return


@app.cell
def _(pd):
    df_rho = pd.read_csv("data/rho_cross_cal.csv")
    df_rho.columns
    df_rho['ts'] = pd.to_datetime(df_rho['timestamp'])
    return (df_rho,)


@app.cell
def _(df_rho):
    df_rho
    return


app._unparsable_cell(
    r"""
    df_rho_test = df_rho[df_rho['timestamp'] > ]
    """,
    name="_"
)


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


@app.cell
def _(pd):
    df_test_times = pd.read_excel("data/7_11_25_Test_Info.xlsx",
                                  skiprows= 10,
                                  skipfooter=11
                                 )

    df_test_times
    return (df_test_times,)


@app.cell
def _(df_test_times):
    df_exp_conc = df_test_times[['Timepoint (EDT)', 'Expected Concentration (ppb)']].rename(columns={'Timepoint (EDT)': 'ts', 'Expected Concentration (ppb)': 'exp_conc'})

    df_exp_conc
    return (df_exp_conc,)


@app.cell
def _(df_exp_conc, df_rho, pd):
    df = pd.merge_asof(
        df_rho, 
        df_exp_conc, 
        on='ts',
        direction='backward'
    ).dropna(subset=['exp_conc'])
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""trim groups""")
    return


@app.cell
def _(df, pd):
    def trim_first_last_minute(group):
        if len(group) <= 2:  # Handle groups with very few rows
            return group.iloc[0:0]  # Return empty dataframe with same structure

        # Sort by timestamp to ensure proper ordering
        group_sorted = group.sort_values('ts')

        # Get the time range
        start_time = group_sorted['ts'].min()
        end_time = group_sorted['ts'].max()

        # Filter out first and last minute
        trimmed = group_sorted[
            (group_sorted['ts'] > start_time + pd.Timedelta(minutes=1)) & 
            (group_sorted['ts'] < end_time - pd.Timedelta(minutes=1))
        ]

        return trimmed

    df_trimmed  = df.groupby('exp_conc').apply(trim_first_last_minute).reset_index(drop=True)
    return (df_trimmed,)


@app.cell
def _(alt, df_trimmed):
    alt.Chart(df_trimmed).mark_point().encode(
        y='concentration',
        x='exp_conc'
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    precision

    extract data for 5 ppb, plot, trim start, get statistics
    """
    )
    return


@app.cell
def _(df):
    df_5 = df[df['exp_conc'] == 5]
    return (df_5,)


@app.cell
def _(alt, df_5):
    alt.Chart(df_5).mark_point().encode(x='ts', y='concentration')
    return


@app.cell
def _(df_trimmed, np, pd):
    def summarize_group(group):
        values = group['voltage']  

        mean_val = values.mean()
        std_val = values.std()
        n = len(values)

        # Relative standard deviation (coefficient of variation)
        rel_sd = (std_val / mean_val) * 100 if mean_val != 0 else float('nan')

        # Relative standard error
        se = std_val / np.sqrt(n) if n > 0 else float('nan')
        rel_se = (se / mean_val) * 100 if mean_val != 0 else float('nan')

        return pd.Series({
            'concentration': group['concentration'].iloc[0],
            'n_observations': n,
            'mean': mean_val,
            'sd': std_val,
            'relative_sd': rel_sd,
            'relative_se': rel_se
        })

    df_sum = df_trimmed.groupby('exp_conc').apply(summarize_group).reset_index()
    df_sum.columns
    return (df_sum,)


@app.cell
def _(alt, df_sum):
    #alt.Chart(df_sum).
    #    mark_point().encode(x='exp_conc', y='relative_sd') +
    df_plot = df_sum[df_sum['exp_conc'] > 0]
    base = alt.Chart(df_plot).add_selection(
        alt.selection_interval()
    ).resolve_scale(
        x='shared',
        y='shared'
    )

    points = base.mark_point().encode(
        x=alt.X('exp_conc', scale=alt.Scale(type='log')),
        y='relative_sd'
    )

    line = base.mark_line(color='grey').transform_regression(
        'exp_conc', 'relative_sd',
    ).encode(
        x='exp_conc',
        y='relative_sd'
    )

    chart = points + line
    chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Pre-cruise Calibration and tests""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # Post-cruise tests

    Sensor was run in static and flow-through tests in blank and 50 ppb rhodamine solutions in ESL seawater.
    """
    )
    return


@app.cell
def _(pd):
    post = pd.read_csv("data/loc02_rho_post_cal.csv")
    post['ts'] = pd.to_datetime(post['timestamp'])
    post
    return (post,)


@app.cell
def _(alt, post):
    alt.Chart(post).mark_point().encode(
        x='ts',
        y='concentration'
    ).interactive()
    return


@app.cell
def _(mo):
    mo.md(r"""given a table of measurement periods, determine the mean for each measurement type""")
    return


@app.cell
def _(np, pd, post):
    post_meas = pd.read_csv("data/loc02_rho_post_cal_times.csv")
    post_meas["start"] = pd.to_datetime(post_meas["start"])
    post_meas["end"] = pd.to_datetime(post_meas["end"])

    def mean_sem_for_period(row, ts):
        mask = (ts["ts"] >= row["start"]) & (ts["ts"] < row["end"])
        values = ts.loc[mask, "concentration"].to_numpy()
        if len(values) == 0:
            return pd.Series([np.nan, np.nan], index=["mean_value", "sem_value"])
        mean = values.mean()
        sem = values.std(ddof=1) / np.sqrt(len(values)) if len(values) > 1 else np.nan
        return pd.Series([mean, sem], index=["mean_value", "sem_value"])

    # Apply to each period
    result = post_meas.join(
        post_meas.apply(lambda row: mean_sem_for_period(row, post), axis=1)
    )

    print(result[["expected", "flow", "mean_value", "sem_value"]])
    return


if __name__ == "__main__":
    app.run()
