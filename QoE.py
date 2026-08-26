import glob
import os
import numpy as np
import pandas as pd

VALID_ROWS_REQUIRED = 3000
SAMPLES_PER_SECOND = 10


def calculate(fname):
    try:
        df = pd.read_csv(fname)

        # Convert required columns to numeric
        df[['videoBufferLength', 'videoBitrate']] = df[
            ['videoBufferLength', 'videoBitrate']
        ].apply(pd.to_numeric, errors='coerce')

        df = df.dropna(subset=['videoBufferLength', 'videoBitrate']).copy()

        if df.empty:
            return [os.path.basename(fname), 0, 0, 0, 0, 0]

        # Remove initial zero-buffer rows
        df = df[~(df.videoBufferLength == 0).cumprod().astype(bool)].copy()

        if df.empty:
            return [os.path.basename(fname), 0, 0, 0, 0, 0]

        # Adjust buffer values
        arr = df.videoBufferLength.to_numpy().copy()

        for i in range(1, len(arr)):
            if arr[i] == 0 and arr[i - 1] >= 0.1:
                arr[i] = arr[i - 1] - 0.1

        df['videoBufferLength'] = arr

        # Find first 3000 valid rows
        valid_df = df[df.videoBufferLength != 0]
        take = min(VALID_ROWS_REQUIRED, len(valid_df))

        if take == 0:
            return [os.path.basename(fname), 0, 0, 0, 0, 0]

        # Find the original index of the 3000th valid row
        last_index = valid_df.index[take - 1]

        # Common boundary:
        # QoE uses valid rows, while bitrate switching uses ALL rows.
        analysis_df = df.loc[:last_index]

        # Stalling time
        buffTime = (analysis_df.videoBufferLength == 0).sum() / SAMPLES_PER_SECOND

        # =========================================================
        # QoE calculation: only valid rows
        # =========================================================

        qoe_df = analysis_df[
            (analysis_df.videoBufferLength != 0) &
            (analysis_df.videoBitrate > 0)
        ]

        f_df = analysis_df[
            (analysis_df.videoBufferLength > 0) &
            (analysis_df.videoBitrate > 0)
        ]

        if len(f_df) == 0 or len(qoe_df) < 2:
            return [os.path.basename(fname), buffTime, 0, 0, 0, 0]

        bitRate = f_df.videoBitrate.mean()

        log_f = np.log10(f_df.videoBitrate / 200)
        log_all = np.log10(qoe_df.videoBitrate.values)

        diff = np.abs(np.diff(log_all)).sum()

        QoE = log_f.sum() - 2.66 * buffTime - diff

        # =========================================================
        # Bitrate switching: ALL rows up to the same boundary
        # =========================================================

        bitrate_values = analysis_df.loc[
            analysis_df.videoBitrate > 0, 'videoBitrate'
        ].values

        bitrate_switches = (
            int(np.sum(np.diff(bitrate_values) != 0))
            if len(bitrate_values) > 1 else 0
        )

        print(
            f"\nFile: {os.path.basename(fname)}"
            f"\nTotal rows: {len(df)}"
            f"\nValid rows: {len(valid_df)}"
            f"\nRows used for QoE: {take}"
            f"\nRows within boundary: {len(analysis_df)}"
            f"\nStalling time: {buffTime:.2f} seconds"
            f"\nAverage bitrate: {bitRate:.2f}"
            f"\nQoE: {QoE:.2f}"
            f"\nDiff: {diff:.2f}"
            f"\nBitrate switches: {bitrate_switches}"
        )

        return [os.path.basename(fname),buffTime,bitRate,QoE,diff,bitrate_switches]

    except Exception as e:
        print(f"Error in file {fname}: {e}")
        return [os.path.basename(fname), 0, 0, 0, 0, 0]


# ============================================================
# Process files
# ============================================================

files = glob.glob("/home/lalan/Desktop/WorkingD/AdHoc-R/Loss-state/Reno/Bola/5%/*")

stat = [calculate(f) for f in files]

# ============================================================
# Create result DataFrame
# ============================================================

columns = [
    'fname',
    'buffTime',
    'bitRate',
    'QoE',
    'Diff',
    'Bitrate_Switches'
]

df_stat = pd.DataFrame(stat, columns=columns)

# ============================================================
# Add average row
# ============================================================

numeric_columns = columns[1:]

average_row = pd.DataFrame(
    [['Average', *df_stat[numeric_columns].mean().values]],
    columns=columns
)

df_stat = pd.concat([df_stat, average_row], ignore_index=True)

# ============================================================
# Save results
# ============================================================

df_stat.to_csv('QoE_Results_5min.csv', index=False)

print("\nFinal Results:")
print(df_stat)

print("\nAverage Values:")
print(df_stat.iloc[:-1][numeric_columns].mean())

print("\nOutput: QoE_Results_5min.csv")