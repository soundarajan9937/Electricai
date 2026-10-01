import os
import gc
import psutil
import time

from ai.meter_detection import (
    detect_meter,
    unload_model
)


# ============================================================
# PROCESS MEMORY
# ============================================================

process = psutil.Process(os.getpid())


def show_memory(label):
    memory_mb = (
        process.memory_info().rss
        / (1024 * 1024)
    )

    print(
        f"{label}: {memory_mb:.2f} MB"
    )

    return memory_mb


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TEST_IMAGE = os.path.join(
    BASE_DIR,
    "uploads",
    "meter.jpg"
)


# ============================================================
# START TEST
# ============================================================

print("=" * 70)
print("ONNX YOLO MEMORY TEST")
print("=" * 70)

print("Test image:")
print(TEST_IMAGE)

print()


# ============================================================
# CHECK IMAGE
# ============================================================

if not os.path.exists(TEST_IMAGE):

    print("❌ Test image does not exist:")
    print(TEST_IMAGE)

    raise SystemExit


file_size = os.path.getsize(
    TEST_IMAGE
)

print(
    f"Test image size: {file_size / 1024:.2f} KB"
)

print()


# ============================================================
# INITIAL MEMORY
# ============================================================

gc.collect()

initial_memory = show_memory(
    "Initial memory"
)


# ============================================================
# START ONNX DETECTION
# ============================================================

print()

print("=" * 70)
print("STARTING ONNX DETECTION")
print("=" * 70)

print()

start_time = time.perf_counter()


try:

    found, crop_path = detect_meter(
        TEST_IMAGE
    )

except Exception as e:

    print()
    print("=" * 70)
    print("❌ TEST ERROR")
    print("=" * 70)

    print("Error:")
    print(e)

    found = False
    crop_path = None


end_time = time.perf_counter()


# ============================================================
# MEMORY AFTER DETECTION
# ============================================================

after_detection_memory = show_memory(
    "After ONNX detection"
)


# ============================================================
# RESULTS
# ============================================================

print()

print(
    "Meter detected:",
    found
)

print(
    "Crop path:",
    crop_path
)

print(
    "Inference time:",
    round(
        end_time - start_time,
        3
    ),
    "seconds"
)


# ============================================================
# UNLOAD ONNX
# ============================================================

print()

print("=" * 70)
print("UNLOADING ONNX")
print("=" * 70)

print()

unload_model()

gc.collect()

time.sleep(1)


# ============================================================
# MEMORY AFTER UNLOAD
# ============================================================

after_unload_memory = show_memory(
    "After ONNX unload"
)


# ============================================================
# MEMORY SUMMARY
# ============================================================

print()

print("=" * 70)
print("MEMORY SUMMARY")
print("=" * 70)

print()

print(
    f"Initial memory:       {initial_memory:.2f} MB"
)

print(
    f"After detection:      {after_detection_memory:.2f} MB"
)

print(
    f"After ONNX unload:    {after_unload_memory:.2f} MB"
)

print()

peak_increase = (
    after_detection_memory
    - initial_memory
)

print(
    f"Peak increase:        {peak_increase:.2f} MB"
)


# ============================================================
# FINAL STATUS
# ============================================================

print()

print("=" * 70)
print("ONNX MEMORY TEST FINISHED")
print("=" * 70)

print()

if found:

    print(
        "✅ Meter detection completed successfully."
    )

else:

    print(
        "⚠️ Meter was not detected."
    )

print()