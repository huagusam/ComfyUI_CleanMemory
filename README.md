
### 🛡️ Core Mechanism: Input Protection Logic

This is the plugin's most critical intelligent feature, solving the pain point of "accidentally deleting in-use data during memory cleanup."

1.  **Recursive Collection**:
    *   When you connect data (such as `Model`, `Image`, `Latent`) to a node's input port (`anything`, `data0`, etc.), the code immediately triggers the `_collect_protected_ids` function.
    *   It doesn't just record the ID of the directly connected object—it **recursively traverses** into the object's internals. For example, if you pass in a model, it automatically locates the model's internal weights (Parameters), buffers (Buffers), and sub-modules, adding all their memory address IDs to a "whitelist."
    *   *Code reference*: The `nn.Module` traversal logic inside the `_collect_protected_ids` function.

2.  **Establishing a Safe Zone (Safe List)**:
    *   All collected IDs are stored in a set (`collected set`). These objects are marked as "in use" and must never be touched.

3.  **Global Sweep (Global Purge)**:
    *   The system iterates through all objects in Python's garbage collector (`gc.get_objects()`).
    *   **Comparison**: If an object's ID is **NOT** in the whitelist → **Execute cleanup** (zero out data or release references).
    *   **Skip**: If an object's ID **IS** in the whitelist → **Preserve as-is**.

4.  **Result**:
    *   Unreferenced garbage memory is released.
    *   Your critical data connected to the node inputs remains intact and can be passed to downstream nodes.

---

### 🧹 Node Overview

Nodes are categorized into two types based on whether they preserve and output data:

#### 1. Terminal Nodes (No output, for workflow endpoints or standalone steps)
*   **🧹 Purge VRAM**:
    *   **Function**: Cleans GPU VRAM only. Calls `torch.cuda.empty_cache()` and ComfyUI's model unloading logic.
    *   **Use Case**: After generating a large image, release VRAM for other applications, or prevent VRAM accumulation leading to OOM errors.
*   **🧹 Purge RAM (Protected)**:
    *   **Function**: Conservative CPU memory cleanup. **Only clears CPU tensors** and releases references of unprotected models.
    *   **Use Case**: Routine cleanup with low risk; won't interfere with CUDA context.
*   **🧹 Purge ALL**:
    *   **Function**: Aggressive cleanup. Attempts to zero out tensor data on all devices (including CUDA) and forcefully releases model references.
    *   **Use Case**: When encountering severe memory leaks or when maximum resource release is needed. *Note: Unprotected models cleaned by this node become "zombie" objects and cannot be reused.*

#### 2. Passthrough Nodes (With output, for mid-workflow use)
*   **🧹 Purge & Pass**:
    *   **Function**: Receives one input, executes cleanup logic (protecting that input), then outputs the input unchanged.
    *   **Use Case**: Place between two heavy nodes. Example: `Load Model` → `Purge & Pass` → `Sampler`. Ensures temporary garbage from model loading is cleaned while the model itself is preserved for the sampler.
    *   **Mode**: Selectable `VRAM` (clean VRAM only) or `RAM` (clean both RAM and VRAM).
*   **🧹 Purge & Pass Multi / Purge RAM Multi**:
    *   **Function**: Supports up to 4 simultaneous inputs (`data0` - `data3`). Protects all non-empty inputs while cleaning unrelated memory.
    *   **Use Case**: Complex workflows where you need to preserve multiple items simultaneously (e.g., Model, VAE, and ControlNet weights) while cleaning other miscellaneous data.

---

### 📝 Typical Usage Scenarios

#### Scenario A: Batch Processing
*   **Connection**: `Image` → `Processing Node` → **`Purge & Pass`** → `Save/Next Iteration`
*   **Purpose**: When processing large batches of images, prevent accumulation of intermediate temporary Tensors. `Purge & Pass` ensures the current image data passes through while cleaning up garbage left from the previous iteration.

#### Scenario B: End of Workflow
*   **Connection**: `Final Output` → **`Purge VRAM`**
*   **Purpose**: After task completion, thoroughly release GPU VRAM to restore system performance for other gaming or rendering tasks.

#### Scenario C: Loading Heavy Models
*   **Connection**: `Checkpoint Loader` → **`Purge RAM (Protected)`** → `KSampler`
*   **Purpose**: Loading large models generates significant temporary memory fragmentation. This node ensures model weights are protected (because they're connected as input) while cleaning useless caches generated during loading, freeing maximum memory for subsequent sampling steps.

---

### ⚠️ Important Notes

*   **"Zombie" Models**: When using `Purge ALL` or `Purge RAM` **without** connecting a model to the input, models in memory will have their internal parameters zeroed out. If downstream nodes attempt to use these unprotected models afterward, errors or incorrect results may occur. **Always connect models you need to preserve to the node's input port!**
*   **Thread Safety**: The code is optimized for ComfyUI's single-threaded execution model. However, in extreme multi-threaded custom node environments, minor discrepancies may exist between the two GC snapshots taken during cleanup.
