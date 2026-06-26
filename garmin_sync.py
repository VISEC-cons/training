"""
Garmin Connect daily sync script.
Haalt slaap, HRV, rusthartslag en Body Battery op en pusht naar GitHub.
Draait dagelijks om 05:30 via Windows Task Scheduler.
"""

import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import garth

GARTH_DIR = Path.home() / ".garth"
REPO_DIR = Path(__file__).parent
OUTPUT_FILE = REPO_DIR / "garmin_daily.json"


def login():
    """Resume saved Garmin session."""
    try:
        garth.resume(str(GARTH_DIR))
    except Exception:
        print("Garmin sessie verlopen. Voer opnieuw uit:")
        print('  python -c "import garth; garth.login(EMAIL, WACHTWOORD); garth.save(str(Path.home() / \'.garth\'))"')
        sys.exit(1)


def get_sleep(day: str) -> dict:
    """Haal slaapdata op voor een specifieke datum."""
    try:
        data = garth.connectapi(f"/wellness-service/wellness/dailySleepData/{day}")
        return {
            "score": data.get("sleepScores", {}).get("overall", {}).get("value"),
            "total_min": round(data.get("sleepTimeInSeconds", 0) / 60),
            "deep_min": round(data.get("deepSleepSeconds", 0) / 60),
            "light_min": round(data.get("lightSleepSeconds", 0) / 60),
            "rem_min": round(data.get("remSleepSeconds", 0) / 60),
            "awake_min": round(data.get("awakeSleepSeconds", 0) / 60),
        }
    except Exception as e:
        print(f"Sleep data error: {e}")
        return {}


def get_hrv(day: str) -> dict:
    """Haal HRV data op."""
    try:
        data = garth.connectapi(f"/hrv-service/hrv/{day}")
        summary = data.get("hrvSummary", {})
        return {
            "weekly_avg_ms": summary.get("weeklyAvg"),
            "last_night_avg_ms": summary.get("lastNightAvg"),
            "last_night_5min_high_ms": summary.get("lastNight5MinHigh"),
            "status": summary.get("status"),
        }
    except Exception as e:
        print(f"HRV data error: {e}")
        return {}


def get_resting_hr(day: str) -> int | None:
    """Haal rusthartslag op."""
    try:
        data = garth.connectapi(
            f"/userstats-service/wellness/daily/{day}",
            params={"metricId": 60},
        )
        if data and len(data) > 0:
            return data[0].get("value")
    except Exception:
        pass
    # Fallback: via daily summary
    try:
        data = garth.connectapi(
            f"/usersummary-service/usersummary/daily/{day}"
        )
        return data.get("restingHeartRate")
    except Exception as e:
        print(f"RHR data error: {e}")
        return None


def get_body_battery(day: str) -> dict:
    """Haal Body Battery data op."""
    try:
        data = garth.connectapi(
            f"/usersummary-service/usersummary/daily/{day}"
        )
        return {
            "charged": data.get("bodyBatteryChargedValue"),
            "drained": data.get("bodyBatteryDrainedValue"),
            "highest": data.get("bodyBatteryHighestValue"),
            "lowest": data.get("bodyBatteryLowestValue"),
        }
    except Exception as e:
        print(f"Body Battery error: {e}")
        return {}


def get_daily_summary(day: str) -> dict:
    """Haal dagelijkse samenvatting op (stress, stappen, etc.)."""
    try:
        data = garth.connectapi(
            f"/usersummary-service/usersummary/daily/{day}"
        )
        return {
            "steps": data.get("totalSteps"),
            "stress_avg": data.get("averageStressLevel"),
            "spo2_avg": data.get("averageSpo2"),
            "calories_active": data.get("activeKilocalories"),
        }
    except Exception as e:
        print(f"Daily summary error: {e}")
        return {}


def git_push():
    """Stage, commit en push garmin_daily.json."""
    try:
        subprocess.run(
            ["git", "add", "garmin_daily.json"],
            cwd=REPO_DIR, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", f"Garmin data {date.today().isoformat()}"],
            cwd=REPO_DIR, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push"],
            cwd=REPO_DIR, check=True, capture_output=True,
        )
        print("Gepusht naar GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr.decode() if e.stderr else e}")


def main():
    login()

    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    # Slaap en HRV zijn van afgelopen nacht, BB/RHR van vandaag
    daily_data = {
        "date": today,
        "sleep": get_sleep(yesterday),
        "hrv": get_hrv(today),
        "resting_hr": get_resting_hr(today),
        "body_battery": get_body_battery(today),
        "daily_summary": get_daily_summary(yesterday),
    }

    OUTPUT_FILE.write_text(json.dumps(daily_data, indent=2, ensure_ascii=False))
    print(f"Data opgeslagen in {OUTPUT_FILE}")
    print(json.dumps(daily_data, indent=2, ensure_ascii=False))

    git_push()


if __name__ == "__main__":
    main()
