<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <!-- 背景网格图案 -->
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#2a2a2a" stroke-width="0.5"/>
    </pattern>
    
    <!-- 渐变 -->
    <linearGradient id="nodeGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3a3a3a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2a2a2a;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- 背景 -->
  <rect width="1200" height="800" fill="#1a1a1a"/>
  <rect width="1200" height="800" fill="url(#grid)"/>
  
  <!-- 连接线 -->
  <!-- 蓝色线 -->
  <path d="M 150 120 Q 200 120 230 120" fill="none" stroke="#4a9eff" stroke-width="2"/>
  
  <!-- 橙色线 -->
  <path d="M 150 160 Q 180 160 230 160" fill="none" stroke="#ff9500" stroke-width="2"/>
  <path d="M 100 280 Q 150 280 230 280" fill="none" stroke="#ff9500" stroke-width="2"/>
  <path d="M 100 320 Q 180 320 230 320" fill="none" stroke="#ff9500" stroke-width="2"/>
  <path d="M 50 450 Q 150 450 230 450" fill="none" stroke="#ff9500" stroke-width="2"/>
  <path d="M 600 360 Q 650 360 700 360" fill="none" stroke="#ff9500" stroke-width="2"/>
  <path d="M 600 560 Q 650 560 700 560" fill="none" stroke="#ff9500" stroke-width="2"/>
  
  <!-- 绿色线 -->
  <path d="M 550 140 Q 650 140 750 140" fill="none" stroke="#4ade80" stroke-width="2"/>
  <path d="M 550 180 Q 650 180 750 180" fill="none" stroke="#4ade80" stroke-width="2"/>
  <path d="M 550 720 Q 650 720 750 760" fill="none" stroke="#4ade80" stroke-width="2"/>
  
  <!-- 节点框 1: Purge & Pass Multi -->
  <g id="node1">
    <rect x="230" y="70" width="320" height="180" rx="8" fill="url(#nodeGradient)" stroke="#4a4a4a" stroke-width="1"/>
    <text x="390" y="55" fill="#4ade80" font-family="Arial" font-size="12" text-anchor="middle">CleanMemory</text>
    <text x="250" y="95" fill="#ff9500" font-family="Arial" font-size="13">🔧 Purge &amp; Pass Multi</text>
    
    <!-- 输入端口 -->
    <circle cx="240" cy="120" r="5" fill="#4ade80"/>
    <text x="255" y="124" fill="#aaa" font-family="Arial" font-size="12">data0</text>
    <text x="530" y="124" fill="#888" font-family="Arial" font-size="12" text-anchor="end">*</text>
    <circle cx="540" cy="120" r="5" fill="#4ade80"/>
    
    <circle cx="240" cy="150" r="5" fill="#4ade80"/>
    <text x="255" y="154" fill="#aaa" font-family="Arial" font-size="12">data1</text>
    <text x="530" y="154" fill="#888" font-family="Arial" font-size="12" text-anchor="end">*</text>
    <circle cx="540" cy="150" r="5" fill="#4ade80"/>
    
    <circle cx="240" cy="180" r="5" fill="#555"/>
    <text x="255" y="184" fill="#888" font-family="Arial" font-size="12">data2</text>
    <text x="530" y="184" fill="#888" font-family="Arial" font-size="12" text-anchor="end">*</text>
    <circle cx="540" cy="180" r="5" fill="#555"/>
    
    <circle cx="240" cy="210" r="5" fill="#555"/>
    <text x="255" y="214" fill="#888" font-family="Arial" font-size="12">data3</text>
    <text x="530" y="214" fill="#888" font-family="Arial" font-size="12" text-anchor="end">*</text>
    <circle cx="540" cy="210" r="5" fill="#555"/>
    
    <!-- mode 滑块 -->
    <rect x="250" y="225" width="260" height="20" rx="3" fill="#2a2a2a"/>
    <text x="265" y="239" fill="#fff" font-family="Arial" font-size="11">◄ mode</text>
    <text x="490" y="239" fill="#fff" font-family="Arial" font-size="11">RAM ►</text>
  </g>
  
  <!-- 节点框 2: Purge VRAM -->
  <g id="node2">
    <rect x="230" y="300" width="320" height="110" rx="8" fill="url(#nodeGradient)" stroke="#4a4a4a" stroke-width="1"/>
    <text x="390" y="285" fill="#4ade80" font-family="Arial" font-size="12" text-anchor="middle">CleanMemory</text>
    <text x="250" y="325" fill="#ff9500" font-family="Arial" font-size="13">🔧 Purge VRAM</text>
    
    <circle cx="240" cy="355" r="5" fill="#555"/>
    <text x="255" y="359" fill="#aaa" font-family="Arial" font-size="12">anything</text>
  </g>
  
  <!-- 节点框 3: Purge ALL -->
  <g id="node3">
    <rect x="230" y="480" width="320" height="90" rx="8" fill="url(#nodeGradient)" stroke="#4a4a4a" stroke-width="1"/>
    <text x="250" y="470" fill="#888" font-family="Arial" font-size="11">0.491秒</text>
    <text x="390" y="465" fill="#4ade80" font-family="Arial" font-size="12" text-anchor="middle">CleanMemory</text>
    <text x="250" y="505" fill="#ff9500" font-family="Arial" font-size="13">🔧 Purge ALL</text>
    
    <circle cx="240" cy="535" r="5" fill="#555"/>
    <text x="255" y="539" fill="#aaa" font-family="Arial" font-size="12">anything</text>
  </g>
  
  <!-- 节点框 4: Purge &amp; Pass -->
  <g id="node4">
    <rect x="230" y="640" width="320" height="100" rx="8" fill="url(#nodeGradient)" stroke="#4a4a4a" stroke-width="1"/>
    <text x="390" y="625" fill="#4ade80" font-family="Arial" font-size="12" text-anchor="middle">CleanMemory</text>
    <text x="250" y="665" fill="#ff9500" font-family="Arial" font-size="13">🔧 Purge &amp; Pass</text>
    
    <circle cx="240" cy="695" r="5" fill="#4ade80"/>
    <text x="255" y="699" fill="#aaa" font-family="Arial" font-size="12">data</text>
    <text x="530" y="699" fill="#888" font-family="Arial" font-size="12" text-anchor="end">*</text>
    <circle cx="540" cy="695" r="5" fill="#4ade80"/>
    
    <rect x="250" y="710" width="260" height="20" rx="3" fill="#2a2a2a"/>
    <text x="265" y="724" fill="#fff" font-family="Arial" font-size="11">◄ mode</text>
    <text x="480" y="724" fill="#fff" font-family="Arial" font-size="11">VRAM ►</text>
  </g>
  
  <!-- 节点框 5: Purge RAM (Protected) -->
  <g id="node5">
    <rect x="700" y="300" width="280" height="90" rx="8" fill="url(#nodeGradient)" stroke="#4a4a4a" stroke-width="1"/>
    <text x="840" y="285" fill="#4ade80" font-family="Arial" font-size="12" text-anchor="middle">CleanMemory</text>
    <text x="720" y="325" fill="#ff9500" font-family="Arial" font-size="13">🔧 Purge RAM (Protected)</text>
    
    <circle cx="710" cy="355" r="5" fill="#4ade80"/>
    <text x="725" y="359" fill="#aaa" font-family="Arial" font-size="12">anything</text>
  </g>
  
  <!-- 节点框 6: Purge RAM Multi -->
  <g id="node6">
    <rect x="700" y="480" width="280" height="140" rx="8" fill="url(#nodeGradient)" stroke="#4a4a4a" stroke-width="1"/>
    <text x="840" y="465" fill="#4ade80" font-family="Arial" font-size="12" text-anchor="middle">CleanMemory</text>
    <text x="720" y="505" fill="#ff9500" font-family="Arial" font-size="13">🔧 Purge RAM Multi</text>
    
    <circle cx="710" cy="535" r="5" fill="#4ade80"/>
    <text x="725" y="539" fill="#aaa" font-family="Arial" font-size="12">data0</text>
    
    <circle cx="710" cy="565" r="5" fill="#555"/>
    <text x="725" y="569" fill="#888" font-family="Arial" font-size="12">data1</text>
    
    <circle cx="710" cy="595" r="5" fill="#555"/>
    <text x="725" y="599" fill="#888" font-family="Arial" font-size="12">data2</text>
    
    <circle cx="710" cy="625" r="5" fill="#555"/>
    <text x="725" y="629" fill="#888" font-family="Arial" font-size="12">data3</text>
  </g>
  
  <!-- 连接点 -->
  <circle cx="750" cy="140" r="4" fill="#888"/>
  <circle cx="850" cy="140" r="4" fill="#888"/>
  <circle cx="750" cy="180" r="4" fill="#888"/>
  <circle cx="850" cy="180" r="4" fill="#888"/>
  <circle cx="750" cy="760" r="4" fill="#888"/>
</svg>
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
