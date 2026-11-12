# Sensor Dataset Pipeline

Turns recorded IMU sessions (CSV plus JSON metadata from the [sensor stream receiver](../embedded-tools/sensor-receiver)) into a versioned, ready-to-train features dataset. One command rebuilds everything from the raw files.

```
python build-dataset.py --raw raw --out dataset --sensor "LSM6DSOX"
```

This is Project A2 of my Edge AI roadmap: the step between "I can record data" and "I can train a model on it".

## What it does

1. **Loads** every session in `raw/` (a CSV of samples and a JSON with the label and measured rate).
2. **Windows** each session separately (default 250 samples = 2.5 s at 100 Hz, 50% overlap). A window never crosses a session boundary, and windows that contain a timestamp gap are dropped.
3. **Extracts 54 features** per window: 9 per channel (mean, std, rms, peak-to-peak, zero-crossing rate, dominant frequency, spectral centroid, energy in two bands), computed with a Hann window.
4. **Splits whole sessions** into train, validation and test, balanced per class. A check stops the run if any session appears in two splits.
5. **Normalises** each feature with a z-score using **training windows only**, and saves the numbers to `scaler.json` so the same scaling can be applied on the device.
6. **Writes** `train.csv`, `val.csv`, `test.csv`, `scaler.json`, `manifest.json` and a generated `DATASET.md` to the output folder.

## Layout

```
dataset-pipeline/
├── build-dataset.py       the one command
├── loader.py              load one session (CSV + JSON)
├── features.py            window features
├── splits.py              session-wise split and overlap check
├── make-fake-sessions.py  synthetic sessions for testing the pipeline
├── raw/                   real recordings (not in git)
└── dataset/               output (not in git)
```

## Usage

```
python build_dataset.py --raw raw --out dataset
```

| Option     | Default       | Meaning                                    |
|------------|---------------|--------------------------------------------|
| `--raw`    | `raw`         | folder with session CSV and JSON files     |
| `--out`    | `dataset`     | output folder                              |
| `--fs`     | `100`         | sample rate in Hz                          |
| `--win`    | `250`         | window length in samples                   |
| `--hop`    | `125`         | step between windows (125 = 50% overlap)   |
| `--seed`   | `0`           | seed for assigning sessions to splits      |
| `--sensor` | `not specified` | sensor name written to `DATASET.md`      |

### Testing without real data

```
python make_fake_sessions.py
python build_dataset.py --raw raw_fake --out dataset_fake --sensor "none (synthetic)"
```

`make_fake_sessions.py` writes 3 classes (sitting, walking, jumping) with 3 sessions each into `raw_fake/`. These are synthetic. Their JSON contains `"synthetic": true`, and `DATASET.md` carries a warning when any session is synthetic.

## Design decisions

- **Split by session, not by window.** Overlapping windows from one recording share samples. If one went to training and its neighbour to testing, the test score would be falsely high. Each class needs at least 3 sessions; with fewer, the pipeline stops with an error instead of making a bad split.
- **Split first, then normalise.** The mean and std come from training windows only, so no information from validation or test data shapes the scaling.
- **A deterministic dataset id.** `manifest.json` holds a 12-character hash of the raw files and the settings. The same input gives the same id, and any change to data or settings gives a new one, so a model result can be traced to the exact dataset.
- **Timestamp gaps are skipped, not repaired.** A window containing a gap larger than 1.5 times the typical step is dropped.

## Results

| Check                                         | Result                                          |
|-----------------------------------------------|-------------------------------------------------|
| Synthetic test set (3 classes, 9 sessions)    | 423 windows, 47 per session, 54 features each   |
| Split                                         | 1 session per class in each of train, val, test |
| Rebuild with the same input                   | same dataset id (`eb42aaac6382`)                |
| Different seed                                | different id, sessions assigned differently     |
| Class with fewer than 3 sessions              | stops with a clear error                        |
| Real IMU recordings                           | not yet recorded                                |

## Known limitations

- Tested only on synthetic sessions and on one firmware test-pattern recording. No real IMU is connected yet, so no real activity data exists.
- The sample rate is a setting (`--fs`), not read per session. All sessions are assumed to be at the same rate.
- The feature set and the two frequency bands (0 to 2 Hz and 2 to 10 Hz) are fixed in code. The dominant frequency is not meaningful for windows with no real motion.
- Only the session-level split is checked. There is no check yet that people or sensor placements are spread across splits.

## What I would change

- Record real data: at least five activity classes, several sessions each, with different people and sensor placements, then split by person as well as by session
- Choose the frequency bands from the spectra of real recordings
- Read the sample rate from each session's metadata and resample if sessions differ
- Add a quick plot of the features per class to the generated `DATASET.md`
