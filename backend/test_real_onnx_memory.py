import os
import gc
import time
import psutil
import cv2
import numpy as np
import onnxruntime as ort


# ============================================================
# PROCESS
# ============================================================

process = psutil.Process(os.getpid())


def memory(label):

    value = (
        process.memory_info().rss
        / (1024 * 1024)
    )

    print(
        f"{label}: {value:.2f} MB"
    )

    return value


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "best.onnx"
)

IMAGE_PATH = os.path.join(
    BASE_DIR,
    "uploads",
    "meter.jpg.jpeg"
)


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = 320


# ============================================================
# START
# ============================================================

print("=" * 70)
print("REAL ONNX YOLO MEMORY TEST")
print("=" * 70)

print("ONNX model:")
print(MODEL_PATH)

print()

print("Test image:")
print(IMAGE_PATH)

print()


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(MODEL_PATH):

    print("❌ best.onnx not found.")

    raise SystemExit


if not os.path.exists(IMAGE_PATH):

    print("❌ Test image not found.")

    raise SystemExit


# ============================================================
# INITIAL MEMORY
# ============================================================

gc.collect()

initial = memory(
    "Initial memory"
)


# ============================================================
# LOAD ONNX
# ============================================================

print()
print("=" * 70)
print("LOADING ONNX MODEL")
print("=" * 70)

options = ort.SessionOptions()

options.intra_op_num_threads = 1
options.inter_op_num_threads = 1

options.graph_optimization_level = (
    ort.GraphOptimizationLevel.ORT_ENABLE_ALL
)

session = ort.InferenceSession(
    MODEL_PATH,
    sess_options=options,
    providers=[
        "CPUExecutionProvider"
    ]
)

print()
print("✅ ONNX model loaded")

print(
    "Providers:",
    session.get_providers()
)

input_info = session.get_inputs()[0]

output_info = session.get_outputs()[0]

print(
    "Input name:",
    input_info.name
)

print(
    "Input shape:",
    input_info.shape
)

print(
    "Output name:",
    output_info.name
)

print(
    "Output shape:",
    output_info.shape
)


after_load = memory(
    "After ONNX model loaded"
)


# ============================================================
# LOAD IMAGE
# ============================================================

print()
print("=" * 70)
print("LOADING IMAGE")
print("=" * 70)

image = cv2.imread(
    IMAGE_PATH
)

if image is None:

    print("❌ Unable to read image.")

    del session

    raise SystemExit


print(
    "Image shape:",
    image.shape
)


# ============================================================
# PREPROCESS
# ============================================================

resized = cv2.resize(
    image,
    (
        IMAGE_SIZE,
        IMAGE_SIZE
    ),
    interpolation=cv2.INTER_LINEAR
)

resized = cv2.cvtColor(
    resized,
    cv2.COLOR_BGR2RGB
)

input_tensor = (
    resized
    .astype(np.float32)
    / 255.0
)

input_tensor = np.transpose(
    input_tensor,
    (2, 0, 1)
)

input_tensor = np.expand_dims(
    input_tensor,
    axis=0
)


print(
    "Input tensor:",
    input_tensor.shape
)


# ============================================================
# ONNX INFERENCE
# ============================================================

print()
print("=" * 70)
print("RUNNING REAL ONNX INFERENCE")
print("=" * 70)

start = time.perf_counter()

outputs = session.run(
    None,
    {
        input_info.name:
        input_tensor
    }
)

end = time.perf_counter()


print()
print("✅ ONNX inference completed")

print(
    "Inference time:",
    round(
        end - start,
        3
    ),
    "seconds"
)


# ============================================================
# OUTPUT
# ============================================================

for index, output in enumerate(outputs):

    print(
        f"Output {index}:",
        output.shape
    )


after_inference = memory(
    "After ONNX inference"
)


# ============================================================
# CLEAN TEMPORARY ARRAYS
# ============================================================

del outputs
del input_tensor
del resized
del image


gc.collect()


after_cleanup = memory(
    "After image/tensor cleanup"
)


# ============================================================
# UNLOAD ONNX
# ============================================================

print()
print("=" * 70)
print("UNLOADING ONNX")
print("=" * 70)

del session

gc.collect()

time.sleep(1)

after_unload = memory(
    "After ONNX unload"
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 70)
print("REAL ONNX MEMORY SUMMARY")
print("=" * 70)

print(
    f"Initial:              {initial:.2f} MB"
)

print(
    f"After model load:     {after_load:.2f} MB"
)

print(
    f"After inference:      {after_inference:.2f} MB"
)

print(
    f"After tensor cleanup: {after_cleanup:.2f} MB"
)

print(
    f"After ONNX unload:    {after_unload:.2f} MB"
)

print()

print(
    "ONNX model load increase:",
    f"{after_load - initial:.2f} MB"
)

print(
    "ONNX peak increase:",
    f"{after_inference - initial:.2f} MB"
)

print()
print("=" * 70)
print("REAL ONNX MEMORY TEST FINISHED")
print("=" * 70)