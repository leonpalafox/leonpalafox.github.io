"""Mini LLM: ¿cuántos tokens por segundo entrena tu CPU y tu GPU?

Uso:  python mini_llm.py            (prueba CPU y, si existe, GPU)
Los tokens son aleatorios: solo se mide velocidad, el modelo no aprende lenguaje.
"""
import os, time, torch, torch.nn as nn, torch.nn.functional as F

VOCAB, DIM, CAPAS, CABEZAS = 50_257, 384, 6, 6
LOTE, LARGO = 16, 256                      # 16 textos de 256 tokens


class MiniLLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok = nn.Embedding(VOCAB, DIM)
        self.pos = nn.Embedding(LARGO, DIM)
        capa = nn.TransformerEncoderLayer(DIM, CABEZAS, 4 * DIM, dropout=0.0,
                                          activation="gelu", batch_first=True, norm_first=True)
        self.capas = nn.TransformerEncoder(capa, CAPAS, enable_nested_tensor=False)
        self.fin = nn.LayerNorm(DIM)
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)

    def forward(self, x):
        mascara = nn.Transformer.generate_square_subsequent_mask(x.size(1), device=x.device)
        h = self.tok(x) + self.pos(torch.arange(x.size(1), device=x.device))
        h = self.capas(h, mask=mascara, is_causal=True)   # cada token solo ve los anteriores
        return self.fin(h) @ self.tok.weight.T            # un puntaje por palabra posible


def sincroniza(equipo):
    if equipo == "cuda": torch.cuda.synchronize()
    if equipo == "mps": torch.mps.synchronize()


def mide(equipo, pasos=10, calentamiento=3):
    torch.manual_seed(0)
    modelo = MiniLLM().to(equipo)
    opt = torch.optim.AdamW(modelo.parameters(), lr=3e-4)
    datos = torch.randint(VOCAB, (LOTE, LARGO + 1), device=equipo)
    x, y = datos[:, :-1], datos[:, 1:]                    # adivinar el siguiente token
    for paso in range(calentamiento + pasos):
        if paso == calentamiento:
            sincroniza(equipo); inicio = time.perf_counter()
        opt.zero_grad(set_to_none=True)
        perdida = F.cross_entropy(modelo(x).flatten(0, 1), y.flatten())
        perdida.backward()
        opt.step()
    sincroniza(equipo)
    segundos = (time.perf_counter() - inicio) / pasos
    n = sum(p.numel() for p in modelo.parameters())
    print(f"{equipo:5s} | {n / 1e6:.1f} M parámetros | {segundos:.3f} s por paso | "
          f"{LOTE * LARGO / segundos:,.0f} tokens/s", flush=True)
    return LOTE * LARGO / segundos


if __name__ == "__main__":
    torch.set_num_threads(os.cpu_count())                # la CPU usa todos sus núcleos
    equipos = ["cpu"]
    if torch.cuda.is_available(): equipos.append("cuda")
    elif torch.backends.mps.is_available(): equipos.append("mps")
    r = {e: mide(e) for e in equipos}
    if len(r) == 2:
        print(f"La GPU fue {r[equipos[1]] / r['cpu']:.1f} veces más rápida que la CPU.")
