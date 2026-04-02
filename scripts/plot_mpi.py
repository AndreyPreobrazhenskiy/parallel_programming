#!/usr/bin/env python3
"""
Comprehensive plotting for MPI benchmark results.
Generates multiple graphs for performance analysis.

Usage: python scripts/plot_mpi.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import FuncFormatter

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.makedirs('results/plots', exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.linewidth'] = 0.8

print("📊 Loading data from results/mpi_results.csv...")
df = pd.read_csv('results/mpi_results.csv')

df['Efficiency'] = df['Speedup'] / df['Procs'] * 100

print(f"✓ Loaded {len(df)} data points")
print(f"  Sizes: {sorted(df['N'].unique())}")
print(f"  Processes: {sorted(df['Procs'].unique())}")

print("\n📈 Plot 1: Speedup vs Processes...")
fig, ax = plt.subplots(figsize=(10, 6))

colors = plt.cm.viridis(np.linspace(0, 1, len(df['N'].unique())))
for i, n in enumerate(sorted(df['N'].unique())):
    subset = df[df['N'] == n].sort_values('Procs')
    ax.plot(subset['Procs'], subset['Speedup'], 
            marker='o', linewidth=2, label=f'N={n}', 
            color=colors[i], markersize=6)

max_procs = df['Procs'].max()
ax.plot([1, max_procs], [1, max_procs], 'k--', alpha=0.4, 
        label='Ideal linear speedup', linewidth=1.5)

ax.set_xlabel('Number of processes', fontsize=12, fontweight='bold')
ax.set_ylabel('Speedup', fontsize=12, fontweight='bold')
ax.set_title('Parallel Speedup by Matrix Size', fontsize=14, pad=20, fontweight='bold')
ax.set_xticks(sorted(df['Procs'].unique()))
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(title='Matrix size (N)', fontsize=9, title_fontsize=10, loc='lower right')
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('results/plots/01_speedup_linear.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: results/plots/01_speedup_linear.png")

print("📈 Plot 2: GFLOPS vs Processes...")
fig, ax = plt.subplots(figsize=(10, 6))

for i, n in enumerate(sorted(df['N'].unique())):
    subset = df[df['N'] == n].sort_values('Procs')
    ax.plot(subset['Procs'], subset['GFLOPS'], 
            marker='s', linewidth=2, label=f'N={n}',
            color=colors[i], markersize=6)

ax.set_xlabel('Number of processes', fontsize=12, fontweight='bold')
ax.set_ylabel('Performance (GFLOPS)', fontsize=12, fontweight='bold')
ax.set_title('Performance by Matrix Size and Process Count', fontsize=14, pad=20, fontweight='bold')
ax.set_xticks(sorted(df['Procs'].unique()))
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(title='Matrix size (N)', fontsize=9, title_fontsize=10, loc='upper left')
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('results/plots/02_gflops.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: results/plots/02_gflops.png")

print("📈 Plot 3: Time vs Matrix Size (log-log)...")
fig, ax = plt.subplots(figsize=(10, 6))

for i, p in enumerate(sorted(df['Procs'].unique())):
    subset = df[df['Procs'] == p].sort_values('N')
    ax.loglog(subset['N'], subset['Time'], 
              marker='^', linewidth=2, label=f'{p} proc',
              color=colors[i], markersize=6)

n_ref = np.array([200, 2000])
t_ref = df[(df['N'] == 200) & (df['Procs'] == 1)]['Time'].values[0]
t_curve = t_ref * (n_ref / 200)**3
ax.loglog(n_ref, t_curve, 'k:', linewidth=1.5, label='O(N³) reference')

ax.set_xlabel('Matrix size (N) [log scale]', fontsize=12, fontweight='bold')
ax.set_ylabel('Execution time (seconds) [log scale]', fontsize=12, fontweight='bold')
ax.set_title('Scaling with Matrix Size (Log-Log)', fontsize=14, pad=20, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--', which='both')
ax.legend(title='Processes', fontsize=9, title_fontsize=10, loc='upper left')

plt.tight_layout()
plt.savefig('results/plots/03_time_loglog.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: results/plots/03_time_loglog.png")

print("📈 Plot 4: Efficiency vs Processes...")
fig, ax = plt.subplots(figsize=(10, 6))

for i, n in enumerate(sorted(df['N'].unique())):
    subset = df[df['N'] == n].sort_values('Procs')
    ax.plot(subset['Procs'], subset['Efficiency'], 
            marker='d', linewidth=2, label=f'N={n}',
            color=colors[i], markersize=6)

ax.axhline(y=100, color='green', linestyle=':', alpha=0.5, label='100% efficiency')
ax.axhline(y=50, color='orange', linestyle=':', alpha=0.3)
ax.axhline(y=25, color='red', linestyle=':', alpha=0.3)

ax.set_xlabel('Number of processes', fontsize=12, fontweight='bold')
ax.set_ylabel('Efficiency (%)', fontsize=12, fontweight='bold')
ax.set_title('Parallel Efficiency by Matrix Size', fontsize=14, pad=20, fontweight='bold')
ax.set_xticks(sorted(df['Procs'].unique()))
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(title='Matrix size (N)', fontsize=9, title_fontsize=10, loc='upper right')
ax.set_ylim(0, 110)

plt.tight_layout()
plt.savefig('results/plots/04_efficiency.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: results/plots/04_efficiency.png")

print("📈 Plot 5: GFLOPS Heatmap...")
fig, ax = plt.subplots(figsize=(10, 7))

pivot_gflops = df.pivot_table(values='GFLOPS', index='N', columns='Procs', aggfunc='first')

im = ax.imshow(pivot_gflops.values, cmap='YlOrRd', aspect='auto')

ax.set_xticks(np.arange(len(pivot_gflops.columns)))
ax.set_yticks(np.arange(len(pivot_gflops.index)))
ax.set_xticklabels([f'{p} proc' for p in pivot_gflops.columns], fontsize=9)
ax.set_yticklabels([f'N={n}' for n in pivot_gflops.index], fontsize=9)

for i in range(len(pivot_gflops.index)):
    for j in range(len(pivot_gflops.columns)):
        val = pivot_gflops.values[i, j]
        color = 'black' if val < pivot_gflops.values.max() * 0.7 else 'white'
        ax.text(j, i, f'{val:.2f}', ha='center', va='center', 
                color=color, fontsize=8, fontweight='bold')

ax.set_xlabel('Number of processes', fontsize=12, fontweight='bold')
ax.set_ylabel('Matrix size (N)', fontsize=12, fontweight='bold')
ax.set_title('Performance Heatmap (GFLOPS)', fontsize=14, pad=20, fontweight='bold')

cbar = plt.colorbar(im, ax=ax, label='GFLOPS')
cbar.ax.tick_params(labelsize=9)

plt.tight_layout()
plt.savefig('results/plots/05_heatmap_gflops.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: results/plots/05_heatmap_gflops.png")

print("📈 Plot 6: Combined Time & GFLOPS (N=1000)...")
df_1000 = df[df['N'] == 1000].sort_values('Procs')

if len(df_1000) > 0:
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color_time = 'tab:blue'
    ax1.set_xlabel('Number of processes', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Time (seconds)', color=color_time, fontsize=12, fontweight='bold')
    ax1.plot(df_1000['Procs'], df_1000['Time'], 
             marker='o', color=color_time, linewidth=2, label='Time', markersize=8)
    ax1.tick_params(axis='y', labelcolor=color_time)
    ax1.grid(True, alpha=0.3, linestyle='--')

    ax2 = ax1.twinx()
    color_gflops = 'tab:green'
    ax2.set_ylabel('Performance (GFLOPS)', color=color_gflops, fontsize=12, fontweight='bold')
    ax2.plot(df_1000['Procs'], df_1000['GFLOPS'], 
             marker='s', color=color_gflops, linewidth=2, label='GFLOPS', markersize=8)
    ax2.tick_params(axis='y', labelcolor=color_gflops)
    
    ax1.set_title('Performance vs Processes (N=1000)', fontsize=14, pad=20, fontweight='bold')
    ax1.set_xticks(sorted(df['Procs'].unique()))

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('results/plots/06_combined_n1000.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: results/plots/06_combined_n1000.png")

print("📈 Plot 7: Strong Scaling Analysis...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for n in [500, 1000, 2000]:
    if n in df['N'].values:
        subset = df[df['N'] == n].sort_values('Procs')
        axes[0].plot(subset['Procs'], subset['Speedup'], 
                     marker='o', linewidth=2, label=f'N={n}')

axes[0].plot([1, 8], [1, 8], 'k--', alpha=0.3, label='Ideal')
axes[0].set_xlabel('Processes')
axes[0].set_ylabel('Speedup')
axes[0].set_title('Strong Scaling: Speedup')
axes[0].set_xticks(sorted(df['Procs'].unique()))
axes[0].grid(True, alpha=0.3)
axes[0].legend(fontsize=9)

for n in [500, 1000, 2000]:
    if n in df['N'].values:
        subset = df[df['N'] == n].sort_values('Procs')
        axes[1].plot(subset['Procs'], subset['Time'], 
                     marker='s', linewidth=2, label=f'N={n}')

axes[1].set_xlabel('Processes')
axes[1].set_ylabel('Time (seconds)')
axes[1].set_title('Strong Scaling: Execution Time')
axes[1].set_xticks(sorted(df['Procs'].unique()))
axes[1].grid(True, alpha=0.3)
axes[1].legend(fontsize=9)

plt.suptitle('Strong Scaling Analysis (Fixed Problem Size)', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/plots/07_strong_scaling.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: results/plots/07_strong_scaling.png")

print("📈 Plot 8: Summary Table...")
fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('tight')
ax.axis('off')

table_data = []
for n in sorted(df['N'].unique()):
    row = [f'N={n}']
    for p in sorted(df['Procs'].unique()):
        val = df[(df['N'] == n) & (df['Procs'] == p)]['Speedup'].values
        if len(val) > 0:
            row.append(f'{val[0]:.2f}×')
        else:
            row.append('-')
    table_data.append(row)

columns = ['Size'] + [f'{p} proc' for p in sorted(df['Procs'].unique())]

table = ax.table(cellText=table_data, colLabels=columns, 
                 cellLoc='center', loc='center', colColours=['#4CAF50']*len(columns))
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.5)

for i in range(len(columns)):
    table[(0, i)].set_facecolor('#4CAF50')
    table[(0, i)].set_text_props(weight='bold', color='white')

ax.set_title('Speedup Summary Table', fontsize=14, pad=20, fontweight='bold')
plt.tight_layout()
plt.savefig('results/plots/08_summary_table.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: results/plots/08_summary_table.png")

print("📈 Plot 9: Dashboard (4-in-1)...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for n in [500, 1000, 2000]:
    if n in df['N'].values:
        subset = df[df['N'] == n].sort_values('Procs')
        axes[0,0].plot(subset['Procs'], subset['Speedup'], 
                       marker='o', label=f'N={n}')
axes[0,0].plot([1,8], [1,8], 'k--', alpha=0.3)
axes[0,0].set_title('Speedup')
axes[0,0].set_xlabel('Processes')
axes[0,0].set_ylabel('Speedup')
axes[0,0].grid(True, alpha=0.3)
axes[0,0].legend(fontsize=8)

for n in [500, 1000, 2000]:
    if n in df['N'].values:
        subset = df[df['N'] == n].sort_values('Procs')
        axes[0,1].plot(subset['Procs'], subset['GFLOPS'], 
                       marker='s', label=f'N={n}')
axes[0,1].set_title('Performance (GFLOPS)')
axes[0,1].set_xlabel('Processes')
axes[0,1].set_ylabel('GFLOPS')
axes[0,1].grid(True, alpha=0.3)
axes[0,1].legend(fontsize=8)

for n in [500, 1000, 2000]:
    if n in df['N'].values:
        subset = df[df['N'] == n].sort_values('Procs')
        eff = subset['Speedup'] / subset['Procs'] * 100
        axes[1,0].plot(subset['Procs'], eff, 
                       marker='d', label=f'N={n}')
axes[1,0].axhline(100, color='green', linestyle=':', alpha=0.5)
axes[1,0].set_title('Efficiency (%)')
axes[1,0].set_xlabel('Processes')
axes[1,0].set_ylabel('Efficiency')
axes[1,0].grid(True, alpha=0.3)
axes[1,0].legend(fontsize=8)

for n in [500, 1000, 2000]:
    if n in df['N'].values:
        subset = df[df['N'] == n].sort_values('Procs')
        axes[1,1].plot(subset['Procs'], subset['Time'], 
                       marker='^', label=f'N={n}')
axes[1,1].set_title('Execution Time')
axes[1,1].set_xlabel('Processes')
axes[1,1].set_ylabel('Time (s)')
axes[1,1].grid(True, alpha=0.3)
axes[1,1].legend(fontsize=8)

plt.suptitle('MPI Performance Dashboard', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/plots/09_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: results/plots/09_dashboard.png")

print("\n" + "="*60)
print("📊 SUMMARY STATISTICS")
print("="*60)

for n in sorted(df['N'].unique()):
    subset = df[df['N'] == n]
    print(f"\n🔹 Matrix N={n}:")
    print(f"   Best GFLOPS: {subset['GFLOPS'].max():.2f} @ {subset.loc[subset['GFLOPS'].idxmax(), 'Procs']} procs")
    print(f"   Max Speedup: {subset['Speedup'].max():.2f}× @ {subset.loc[subset['Speedup'].idxmax(), 'Procs']} procs")
    print(f"   Best Efficiency: {subset['Efficiency'].max():.1f}%")

print("\n" + "="*60)
print("✅ All plots saved to results/plots/")
print("="*60)
print("\n📁 Generated files:")
for f in sorted(os.listdir('results/plots')):
    print(f"   📊 {f}")
