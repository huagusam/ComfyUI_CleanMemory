import torch
import gc
import sys
import comfy.model_management as mm
import torch.nn as nn

try:
    import execution
except:
    execution = None

class AnyType(str):
    def __eq__(self, __value: object) -> bool:
        return True
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")


def _collect_protected_ids(data, collected=None, _visited=None):
    if collected is None:
        collected = set()
    if _visited is None:
        _visited = set()

    if data is None:
        return collected

    data_id = id(data)
    if data_id in _visited:
        return collected
    _visited.add(data_id)
    collected.add(data_id)

    if isinstance(data, nn.Module):
        standard_attrs = {'_modules', '_parameters', '_buffers'}
        
        if hasattr(data, '_modules'):
            for sub_module in data._modules.values():
                _collect_protected_ids(sub_module, collected, _visited)
        if hasattr(data, '_parameters'):
            for param in data._parameters.values():
                _collect_protected_ids(param, collected, _visited)
        if hasattr(data, '_buffers'):
            for buffer in data._buffers.values():
                _collect_protected_ids(buffer, collected, _visited)
        
        if hasattr(data, '__dict__'):
            for k, v in data.__dict__.items():
                if k not in standard_attrs:  
                    _collect_protected_ids(v, collected, _visited)
        return collected

    if torch.is_tensor(data):
        return collected

    if isinstance(data, (list, tuple)):
        for item in data:
            _collect_protected_ids(item, collected, _visited)
    elif isinstance(data, dict):
        for v in data.values():
            _collect_protected_ids(v, collected, _visited)
    elif hasattr(data, '__dict__'):
        for v in data.__dict__.values():
            _collect_protected_ids(v, collected, _visited)
    
    return collected


def _purge_vram():
    mm.unload_all_models()
    mm.soft_empty_cache()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()


def _zero_model_references(model):
    if hasattr(model, '_cleanmemory_cleared'):
        return
    
    model._cleanmemory_cleared = True
    
    try:
        if hasattr(model, '_modules'):
            model._modules.clear()
        if hasattr(model, '_parameters'):
            model._parameters.clear()
        if hasattr(model, '_buffers'):
            model._buffers.clear()
        
        hook_attrs = [
            '_forward_hooks', '_backward_hooks', '_forward_pre_hooks',
            '_state_dict_hooks', '_load_state_dict_pre_hooks',
            '_non_persistent_buffers_set'
        ]
        for attr in hook_attrs:
            if hasattr(model, attr):
                hook_obj = getattr(model, attr)
                if hasattr(hook_obj, 'clear'):
                    hook_obj.clear()

    except Exception as e:
        if execution is not None:
            print(f"[CleanMemory] Warning: Failed to zero model references: {e}")


def _purge_ram(protected_ids, include_models=True):
    for obj in gc.get_objects():
        obj_id = id(obj)
        if obj_id in protected_ids:
            continue
        try:
            if torch.is_tensor(obj):
                if obj.device.type == "cpu":
                    obj.data = torch.empty(0, dtype=obj.dtype, device=obj.device)
        except Exception as e:
            if execution is not None:
                print(f"[CleanMemory] Debug: Failed to clean CPU tensor: {e}")

    if include_models:
        for obj in gc.get_objects():
            obj_id = id(obj)
            if obj_id in protected_ids:
                continue
            try:
                if isinstance(obj, nn.Module):
                    _zero_model_references(obj)
            except Exception as e:
                if execution is not None:
                    print(f"[CleanMemory] Debug: Failed to clean model: {e}")

    gc.collect()


def _purge_ram_aggressive(protected_ids):
    for obj in gc.get_objects():
        obj_id = id(obj)
        if obj_id in protected_ids:
            continue

        try:
            if torch.is_tensor(obj):
                try:
                    obj.data = torch.empty(0, dtype=obj.dtype, device=obj.device)
                except Exception as e:
                    obj.data = torch.empty(0, dtype=obj.dtype, device='cpu')
                    if execution is not None:
                        print(f"[CleanMemory] Warning: Tensor clear fallback (CPU): {e}")
        except Exception as e:
            if execution is not None:
                print(f"[CleanMemory] Error cleaning tensor: {e}")

    for obj in gc.get_objects():
        obj_id = id(obj)
        if obj_id in protected_ids:
            continue

        try:
            if isinstance(obj, nn.Module):
                _zero_model_references(obj)
        except Exception as e:
            if execution is not None:
                print(f"[CleanMemory] Error cleaning model: {e}")

    gc.collect()


class PurgeVRAM:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"anything": (any_type, {})}}

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "purge"
    CATEGORY = "CleanMemory"

    def purge(self, anything):
        if anything is None:
            if execution is not None:
                print("[CleanMemory] Warning: Input is None, skip purge")
            return ()
        _purge_vram()

        return ()


class PurgeRAM:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"anything": (any_type, {})}}

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "purge"
    CATEGORY = "CleanMemory"

    def purge(self, anything):
        if anything is None:
            if execution is not None:
                print("[CleanMemory] Warning: Input is None, skip purge")
            return ()
        protected_ids = _collect_protected_ids(anything)
        _purge_vram()
        _purge_ram(protected_ids, include_models=True)
        return ()


class PurgeAll:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"anything": (any_type, {})}}

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "purge"
    CATEGORY = "CleanMemory"

    def purge(self, anything):
        if anything is None:
            if execution is not None:
                print("[CleanMemory] Warning: Input is None, skip purge")
            return ()
        _purge_vram()
        protected_ids = _collect_protected_ids(anything)
        _purge_ram_aggressive(protected_ids)
        return ()


class PurgePass:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "data": (any_type, {}),
                "mode": (["VRAM", "RAM"], {"default": "RAM"}),
            }
        }

    RETURN_TYPES = (any_type,)
    FUNCTION = "purge_and_pass"
    CATEGORY = "CleanMemory"

    def purge_and_pass(self, data, mode):
        if data is None:
            if execution is not None:
                print("[CleanMemory] Warning: Input is None, skip purge")
            return (data,)
        protected_ids = _collect_protected_ids(data)
        _purge_vram()

        if mode == "RAM":
            _purge_ram(protected_ids, include_models=True)

        return (data,)


class PurgeRAMProtectedMulti:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"data0": (any_type, {})},
            "optional": {
                "data1": (any_type, {}),
                "data2": (any_type, {}),
                "data3": (any_type, {}),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "purge"
    CATEGORY = "CleanMemory"

    def purge(self, data0, data1=None, data2=None, data3=None):
        if data0 is None:
            if execution is not None:
                print("[CleanMemory] Warning: Required input data0 is None, skip purge")
            return ()
        protected_ids = set()
        for d in [data0, data1, data2, data3]:
            if d is not None:
                _collect_protected_ids(d, protected_ids)

        _purge_vram()
        _purge_ram(protected_ids, include_models=True)
        return ()


class PurgePassMultiInput:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"data0": (any_type, {})},
            "optional": {
                "data1": (any_type, {}),
                "data2": (any_type, {}),
                "data3": (any_type, {}),
                "mode": (["VRAM", "RAM"], {"default": "RAM"}),
            }
        }

    RETURN_TYPES = (any_type, any_type, any_type, any_type)
    FUNCTION = "purge_and_pass"
    CATEGORY = "CleanMemory"

    def purge_and_pass(self, data0, data1=None, data2=None, data3=None, mode="RAM"):
        if data0 is None:
            if execution is not None:
                print("[CleanMemory] Warning: Required input data0 is None, skip purge")
            return (data0, data1, data2, data3)
        
        inputs = [data0, data1, data2, data3]
        protected_ids = set()
        for d in inputs:
            if d is not None:
                _collect_protected_ids(d, protected_ids)

        _purge_vram()
        if mode == "RAM":
            _purge_ram(protected_ids, include_models=True)
        return tuple(inputs)

NODE_KEY_VRAM = "CleanMemory_PurgeVRAM"
NODE_KEY_RAM = "CleanMemory_PurgeRAM"
NODE_KEY_ALL = "CleanMemory_PurgeAll"
NODE_KEY_PASS = "CleanMemory_PurgePass"
NODE_KEY_RAM_MULTI = "CleanMemory_PurgeRAMProtectedMulti"
NODE_KEY_PASS_MULTI = "CleanMemory_PurgePassMultiInput"

NODE_CLASS_MAPPINGS = {
    NODE_KEY_VRAM: PurgeVRAM,
    NODE_KEY_RAM: PurgeRAM,
    NODE_KEY_ALL: PurgeAll,
    NODE_KEY_PASS: PurgePass,
    NODE_KEY_RAM_MULTI: PurgeRAMProtectedMulti,
    NODE_KEY_PASS_MULTI: PurgePassMultiInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_KEY_VRAM: "🧹Purge VRAM",
    NODE_KEY_RAM: "🧹Purge RAM (Protected)",
    NODE_KEY_ALL: "🧹Purge ALL",
    NODE_KEY_PASS: "🧹Purge & Pass",
    NODE_KEY_RAM_MULTI: "🧹Purge RAM Multi",
    NODE_KEY_PASS_MULTI: "🧹Purge & Pass Multi",
}