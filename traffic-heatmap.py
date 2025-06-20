import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# === CONFIGURATION (replace these!) ===
API_KEY     = "<YOUR_API_KEY>"
ORIGIN      = "<ORIGIN_ADDRESS>"
DESTINATION = "<DESTINATION_ADDRESS>"

# === DATE & SLOT SETUP ===
today = datetime.date.today()
# next 7 calendar days, then filter out weekends
dates = [today + datetime.timedelta(days=i) for i in range(7)]
weekdays = [d for d in dates if d.weekday() < 5]  # Mon=0 … Fri=4

# build 15-min slots from 08:00 to 11:00
slot_times = []
t = datetime.time(8, 0)
while t <= datetime.time(11, 0):
    slot_times.append(t)
    # advance 15 min
    dummy = datetime.datetime.combine(today, t) + datetime.timedelta(minutes=15)
    t = dummy.time()

# === DATA COLLECTION ===
records = []
for d in weekdays:
    # fetch 10:30 baseline for ROI
    baseline_dt = datetime.datetime.combine(d, datetime.time(10, 30))
    bl_params = {
        "origins":        ORIGIN,
        "destinations":   DESTINATION,
        "departure_time": int(baseline_dt.timestamp()),
        "key":            API_KEY
    }
    bl_resp = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json",
        params=bl_params
    ).json()
    bl_elem = bl_resp["rows"][0]["elements"][0]
    bl_minutes = bl_elem["duration_in_traffic"]["value"] / 60

    for slot in slot_times:
        dt_slot = datetime.datetime.combine(d, slot)
        params = {
            "origins":        ORIGIN,
            "destinations":   DESTINATION,
            "departure_time": int(dt_slot.timestamp()),
            "key":            API_KEY
        }
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            params=params
        ).json()
        elem   = resp["rows"][0]["elements"][0]
        travel = elem.get("duration_in_traffic", elem["duration"])["value"] / 60

        # compute ROI vs. 10:30
        minutes_earlier = (10*60 + 30) - (slot.hour*60 + slot.minute)
        roi = (bl_minutes - travel) / minutes_earlier if minutes_earlier > 0 else 0

        records.append({
            "date":    d.isoformat(),
            "slot":    slot.strftime("%H:%M"),
            "travel":  round(travel, 1),
            "roi":     round(roi, 3)
        })

        # be kind to the API
        time.sleep(1)

# === SAVE RESULTS ===
df = pd.DataFrame(records)
csv_file = "weekly_commute_trends.csv"
df.to_csv(csv_file, index=False)
print(f"Saved raw data to {csv_file}")

# === PIVOT & VISUALIZE ===
# fix pivot bug with keyword args
pivot_time = df.pivot(index="date", columns="slot", values="travel")
pivot_roi  = df.pivot(index="date", columns="slot", values="roi")

# 1) Travel Time Heatmap
plt.figure(figsize=(10, 6))
plt.title("Commute Travel Time (mins) — Next Weekdays, 8–11 AM")
plt.xlabel("Departure Time")
plt.ylabel("Date")
plt.imshow(pivot_time, aspect="auto")
plt.colorbar(label="Minutes")
plt.xticks(range(len(pivot_time.columns)), pivot_time.columns, rotation=45)
plt.yticks(range(len(pivot_time.index)), pivot_time.index)
plt.tight_layout()

# 2) ROI Heatmap
plt.figure(figsize=(10, 6))
plt.title("ROI: Minutes Saved per Minute Earlier")
plt.xlabel("Departure Time")
plt.ylabel("Date")
plt.imshow(pivot_roi, aspect="auto")
plt.colorbar(label="ROI")
plt.xticks(range(len(pivot_roi.columns)), pivot_roi.columns, rotation=45)
plt.yticks(range(len(pivot_roi.index)), pivot_roi.index)
plt.tight_layout()

plt.show()
