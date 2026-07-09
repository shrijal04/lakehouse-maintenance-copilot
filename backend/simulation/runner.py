import subprocess
import threading
import time
import os
import sys


BASE_DIR = os.path.dirname(__file__)

SESSION_A = os.path.join(BASE_DIR, "session_a.py")
SESSION_B = os.path.join(BASE_DIR, "session_b.py")


# ---------------------------------------------------
# Ignore noisy Spark messages
# ---------------------------------------------------

IGNORE_PATTERNS = [

    "Missing Python executable",
    "WARNING: Using incubator modules",
    ":: loading settings ::",
    "Ivy Default Cache",
    "The jars for the packages",
    "org.apache.iceberg",
    ":: resolving dependencies ::",
    ":: resolution report ::",
    ":: retrieving ::",
    "Using Spark's default",
    "Setting default log level",
    "WARN Utils",
    "WARN SparkEnv",
    "ERROR ShutdownHookManager",
    "ERROR ReplaceDataExec",
    "Spark temp dir",
    "Service 'SparkUI'",
    "ShutdownHook",
    "SUCCESS: The process",
    "java.io.IOException",
    "at org.",
    "Suppressed:",
    "Py4JJavaError",
    "Traceback",
    "File \"",
    "raise ",
    "return ",
    "answer,",
    "format(",
    "confs:",
    "modules in use",
    "artifacts",
    "---------------------------------------------------------------------",
    "[Stage",
]


def should_ignore(line: str) -> bool:
    """
    Returns True if the line is Spark noise.
    """

    if not line.strip():
        return True

    for pattern in IGNORE_PATTERNS:
        if pattern in line:
            return True

    return False


def capture_process(process, logs):
    """
    Reads process output while filtering Spark logs.
    """

    while True:

        line = process.stdout.readline()

        if not line:
            break

        line = line.strip()

        if should_ignore(line):
            continue

        logs.append(line)


def run_occ_simulation():

    logs = []

    session_a_result = "Not Started"
    session_b_result = "Not Started"

    try:

        python = sys.executable

        # -----------------------------
        # Start Session A
        # -----------------------------

        process_a = subprocess.Popen(
            [python, SESSION_A],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        thread_a = threading.Thread(
            target=capture_process,
            args=(process_a, logs)
        )

        thread_a.start()

        # Allow Session A to read the snapshot
        time.sleep(3)

        # -----------------------------
        # Start Session B
        # -----------------------------

        process_b = subprocess.Popen(
            [python, SESSION_B],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        thread_b = threading.Thread(
            target=capture_process,
            args=(process_b, logs)
        )

        thread_b.start()

        # -----------------------------
        # Wait for both sessions
        # -----------------------------

        process_a.wait()
        process_b.wait()

        thread_a.join()
        thread_b.join()

        # -----------------------------
        # Final status
        # -----------------------------

        session_a_result = (
            "Committed"
            if process_a.returncode == 0
            else "Failed"
        )

        session_b_result = (
            "Committed"
            if process_b.returncode == 0
            else "Failed"
        )

        conflict = (
            session_a_result == "Failed"
            or
            session_b_result == "Failed"
        )

        return {

            "status": "completed",

            "conflict": conflict,

            "message": (
                "Optimistic Concurrency Conflict Detected"
                if conflict
                else "Simulation completed successfully"
            ),

            "logs": logs,

            "sessionA": session_a_result,

            "sessionB": session_b_result

        }

    except Exception as e:

        return {

            "status": "failed",

            "conflict": False,

            "message": str(e),

            "logs": [str(e)],

            "sessionA": session_a_result,

            "sessionB": session_b_result

        }