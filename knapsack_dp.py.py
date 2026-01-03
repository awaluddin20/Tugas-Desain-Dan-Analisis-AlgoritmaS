# ==========================================================
# 0/1 Knapsack - Complex Version
# - DP Table + Backtracking
# - Item ratio (value/weight) info
# - Compare with Brute Force (concept + exact)
# ==========================================================

from itertools import combinations
import time

items = [
    ("K1", "Beras Premium 5 kg", 1, 7),
    ("K2", "Gula Pasir Kemasan", 4, 24),
    ("K3", "Minyak Goreng 1 L", 2, 13),
    ("K4", "Tepung Terigu Protein", 6, 36),
    ("K5", "Kopi Bubuk UMKM", 5, 29),
    ("K6", "Teh Celup Lokal", 3, 19),
    ("K7", "Susu Bubuk", 7, 40),
    ("K8", "Garam Dapur", 2, 11),
    ("K9", "Kacang Tanah Kupas", 4, 27),
    ("K10", "Mie Kering Produksi UMKM", 6, 34),
]

W = 15
n = len(items)

def solve_dp(items, W):
    n = len(items)
    dp = [[0]*(W+1) for _ in range(n+1)]
    take = [[False]*(W+1) for _ in range(n+1)]

    for i in range(1, n+1):
        code, name, wt, val = items[i-1]
        for cap in range(W+1):
            dp[i][cap] = dp[i-1][cap]
            if wt <= cap:
                cand = dp[i-1][cap-wt] + val
                if cand > dp[i][cap]:
                    dp[i][cap] = cand
                    take[i][cap] = True

    # backtracking
    cap = W
    chosen = []
    trace = []
    for i in range(n, 0, -1):
        if take[i][cap]:
            code, name, wt, val = items[i-1]
            chosen.append(items[i-1])
            trace.append(f"Ambil {code} (w={wt}, v={val}) -> sisa kapasitas {cap-wt}")
            cap -= wt
        else:
            code, name, wt, val = items[i-1]
            trace.append(f"Skip  {code} (w={wt}, v={val}) -> kapasitas tetap {cap}")

    chosen.reverse()
    trace.reverse()
    return dp, chosen, trace

def solve_bruteforce(items, W):
    best_val = 0
    best_set = []
    n = len(items)
    # cek semua subset
    for r in range(n+1):
        for comb in combinations(items, r):
            total_w = sum(x[2] for x in comb)
            total_v = sum(x[3] for x in comb)
            if total_w <= W and total_v > best_val:
                best_val = total_v
                best_set = list(comb)
    return best_val, best_set

def print_items_table(items):
    print("DAFTAR ITEM (dengan rasio profit/berat):")
    print("-"*90)
    print(f"{'Kode':<5} {'Nama':<30} {'Berat':>5} {'Profit':>7} {'Rasio(v/w)':>12}")
    print("-"*90)
    for code, name, wt, val in items:
        ratio = val / wt
        print(f"{code:<5} {name:<30} {wt:>5} {val:>7} {ratio:>12.2f}")
    print("-"*90)

def print_dp_preview(dp, max_rows=6, max_cols=16):
    # tampilkan pratinjau dp (biar tidak kepanjangan)
    rows = min(len(dp), max_rows)
    cols = min(len(dp[0]), max_cols)
    print("\nPREVIEW TABEL DP (baris=item, kolom=kapasitas):")
    print("(dipotong agar ringkas)")
    header = "cap | " + " ".join(f"{c:>3}" for c in range(cols))
    print(header)
    print("-"*len(header))
    for i in range(rows):
        row = f"{i:>3} | " + " ".join(f"{dp[i][c]:>3}" for c in range(cols))
        print(row)
    if len(dp) > rows or len(dp[0]) > cols:
        print("... (tabel dp lengkap tidak ditampilkan)")

print("   0/1 KNAPSACK")
print(f"Kapasitas Gudang (W) = {W} kg\n")

print_items_table(items)

# DP Solve
t0 = time.time()
dp, chosen, trace = solve_dp(items, W)
t1 = time.time()

max_profit = dp[len(items)][W]
total_weight = sum(x[2] for x in chosen)

print("\nHASIL (DYNAMIC PROGRAMMING):")
print("-"*90)
print(f"Nilai Maksimum  : {max_profit}")
print(f"Total Berat     : {total_weight} kg")
print("Item Terpilih   :")
for code, name, wt, val in chosen:
    print(f"  - {code} | {name} | w={wt} | v={val}")
print(f"Waktu DP        : {(t1-t0)*1000:.3f} ms")
print("-"*90)

# Backtracking trace
print("\nTRACE REKONSTRUKSI (BACKTRACKING):")
for line in trace:
    print("  " + line)

# DP Table Preview
print_dp_preview(dp)

# Brute Force compare (still feasible for n=10)
t2 = time.time()
bf_val, bf_set = solve_bruteforce(items, W)
t3 = time.time()

bf_weight = sum(x[2] for x in bf_set)

print("\nPERBANDINGAN DENGAN BRUTE FORCE:")
print("-"*90)
print(f"Brute Force Nilai Maks : {bf_val}")
print(f"Brute Force Total Berat: {bf_weight} kg")
print("Item (Brute Force)     :")
for code, name, wt, val in bf_set:
    print(f"  - {code} | {name} | w={wt} | v={val}")
print(f"Jumlah kombinasi dicek : {2**len(items)} (2^n)")
print(f"Waktu Brute Force      : {(t3-t2)*1000:.3f} ms")
print("-"*90)

# Validasi hasil sama
print("\nVALIDASI:")
if bf_val == max_profit:
    print("✅ DP = Brute Force (hasil optimal terverifikasi).")
else:
    print("⚠️ DP != Brute Force (cek kembali implementasi).")
