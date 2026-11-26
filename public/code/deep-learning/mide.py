"""¿Cuánto tarda un all-reduce entre dos GPUs?

Uso:  torchrun --standalone --nproc-per-node=2 mide.py
"""
import os, time, torch, torch.distributed as dist

dist.init_process_group("nccl")
torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))

for mb in [2.1, 16.2, 114.1, 228.2]:
    x = torch.zeros(int(mb * 250_000), device="cuda")   # FP32: 4 bytes por valor
    for _ in range(5):                                  # calentamiento
        dist.all_reduce(x)
    torch.cuda.synchronize()
    inicio = time.perf_counter()
    for _ in range(20):
        dist.all_reduce(x)
    torch.cuda.synchronize()
    ms = (time.perf_counter() - inicio) / 20 * 1000
    if dist.get_rank() == 0:
        print(f"{mb:6.1f} MB: {ms:.2f} ms")

dist.destroy_process_group()
