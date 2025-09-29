import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import yfinance as yf

TICKER = "MBOT"
H1 = 21   # ~1 month trading days
H3 = 63   # ~3 months trading days

os.makedirs("charts", exist_ok=True)
os.makedirs("output", exist_ok=True)

def download_series(ticker: str) -> pd.Series:
    end = pd.Timestamp.today().normalize() + pd.Timedelta(days=1)
    start = end - pd.DateOffset(years=5)
    df = yf.download(ticker, start=str(start.date()), end=str(end.date()),
                 interval="1d", progress=False, auto_adjust=True)

    if df is None or df.empty:
        raise RuntimeError("Failed to download price history")
    s = df["Close"].dropna().astype(float)
    s.index = pd.to_datetime(s.index)
    return s

def snapshots(s: pd.Series) -> dict:
    ref = s.index[-1]

    def at_or_before(ts):
        idx = s.index.searchsorted(ts, side="right") - 1
        if idx >= 0:
            # Series -> 스칼라 안전 변환
            return float(s.iloc[idx].item())
        return np.nan

    return {
        "now": float(s.iloc[-1].item()),
        "1d": at_or_before(ref - pd.Timedelta(days=1)),
        "5d": at_or_before(ref - pd.Timedelta(days=5)),
        "1mo": at_or_before(ref - pd.DateOffset(months=1)),
        "1y": at_or_before(ref - pd.DateOffset(years=1)),
        "5y": at_or_before(ref - pd.DateOffset(years=5)),
    }


def fit_hw(s: pd.Series):
    s2 = s.asfreq("B").interpolate(method="time")
    train = s2.iloc[:-90] if len(s2) > 120 else s2.copy()
    hw = ExponentialSmoothing(train, trend="add", seasonal=None,
                              initialization_method="heuristic").fit(optimized=True, use_brute=True)
    f1 = hw.forecast(H1)
    f3 = hw.forecast(H3)
    resid = s2.loc[train.index[-90]:] - hw.fittedvalues.loc[train.index[-90]:]
    sigma = float(np.nanstd(resid))
    if not np.isfinite(sigma) or sigma == 0.0:
        sigma = float(s2.pct_change().std() * s2.iloc[-1] / 3)
    return s2, f1, f3, sigma

def build_scenarios(f1: pd.Series, f3: pd.Series, sigma: float):
    # Base
    base1, base3 = f1.copy(), f3.copy()
    # Bullish: +σ drift scaled over horizon
    t1 = np.linspace(0.33, 1.0, len(f1))
    t3 = np.linspace(0.33, 1.0, len(f3))
    bull1 = f1 + sigma * t1
    bull3 = f3 + sigma * t3
    # Bearish: -σ drift + initial -0.5σ shock
    bear1 = f1 - sigma * t1
    bear3 = f3 - sigma * t3
    if len(bear1) > 0: bear1.iloc[0] -= 0.5*sigma
    if len(bear3) > 0: bear3.iloc[0] -= 0.5*sigma
    return (base1, base3), (bull1, bull3), (bear1, bear3)

def plot_chart(s: pd.Series, base, bull, bear):
    fig, ax = plt.subplots()
    ax.plot(s.index, s.values, label="Close")  # default color only

    (b1, b3) = base
    (u1, u3) = bull
    (d1, d3) = bear

    ax.plot(b1.index, b1.values, label="Baseline 1M (HW)")
    ax.plot(b3.index, b3.values, label="Baseline 3M (HW)")
    ax.plot(u1.index, u1.values, label="Bullish 1M (+σ)")
    ax.plot(u3.index, u3.values, label="Bullish 3M (+σ)")
    ax.plot(d1.index, d1.values, label="Bearish 1M (−σ shock)")
    ax.plot(d3.index, d3.values, label="Bearish 3M (−σ shock)")

    ax.set_title("MBOT — History & 3-Scenario Forecast (1M / 3M)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig("charts/MBOT_forecast.png", dpi=150)
    plt.close(fig)

def main():
    s = download_series(TICKER)
    pd.DataFrame([snapshots(s)]).to_csv("output/mbot_snapshots.csv", index=False)
    s2, f1, f3, sigma = fit_hw(s)
    base, bull, bear = build_scenarios(f1, f3, sigma)
    plot_chart(s2, base, bull, bear)
    print("Saved charts/MBOT_forecast.png and output/mbot_snapshots.csv")

if __name__ == "__main__":
    main()
