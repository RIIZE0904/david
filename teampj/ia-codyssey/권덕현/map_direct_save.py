import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import deque

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_and_clean_csv(file_name):
    path = os.path.join(BASE_DIR, file_name)
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

# Load data
map_df = load_and_clean_csv('area_map.csv')
struct_df = load_and_clean_csv('area_struct.csv')
category_df = load_and_clean_csv('area_category.csv')

# Merge structure name
struct_df = struct_df.merge(category_df, how='left', on='category')
merged_df = struct_df.merge(map_df, how='left', on=['x', 'y'])

# Create map grid
grid = {}
home = None
cafe_candidates = []
for _, row in merged_df.iterrows():
    x, y = int(row['x']), int(row['y'])
    key = (x, y)
    grid[key] = {
        'walkable': row['ConstructionSite'] != 1,
        'type': row['struct']
    }
    if row['struct'] == 'MyHome':
        home = (x, y)
    elif row['struct'] == 'BandalgomCoffee':
        cafe_candidates.append((x, y))

# BFS implementation
def bfs(start, goal, grid):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)

        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if neighbor in grid and grid[neighbor]['walkable'] and neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return []

# Find shortest path among multiple cafes
shortest_path = []
for cafe in cafe_candidates:
    path = bfs(home, cafe, grid)
    if path and (not shortest_path or len(path) < len(shortest_path)):
        shortest_path = path

# Save path to CSV
path_df = pd.DataFrame(shortest_path, columns=['x', 'y'])
path_df.to_csv(os.path.join(BASE_DIR, 'home_to_cafe.csv'), index=False)

# Draw map with path
max_x = merged_df['x'].max() + 1
max_y = merged_df['y'].max() + 1

fig, ax = plt.subplots(figsize=(12, 12))

# Area background
area_colors = {0: '#fff8dc', 1: '#e6f2ff', 2: '#e6ffe6', 3: '#ffe6cc'}
for _, row in merged_df.iterrows():
    x, y, area = row['x'], row['y'], row['area']
    ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=area_colors.get(area, '#ffffff'), zorder=0))

# Construction sites
for (x, y), info in grid.items():
    if not info['walkable']:
        ax.add_patch(plt.Rectangle((x - 0.35, y - 0.35), 0.7, 0.7, color='gray', zorder=1))

# Structures
for (x, y), info in grid.items():
    if not info['walkable']:
        continue
    struct = info['type']
    if struct == 'BandalgomCoffee':
        ax.add_patch(plt.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color='green', zorder=2))
    elif struct == 'MyHome':
        ax.plot(x, y, marker='^', color='green', markersize=12, zorder=2)
    elif struct == 'Apartment':
        ax.plot(x, y, 'o', color='saddlebrown', markersize=10, zorder=2)
    elif struct == 'Building':
        ax.plot(x, y, 'o', color='saddlebrown', markersize=10, zorder=2)

# Path drawing
if shortest_path:
    px, py = zip(*shortest_path)
    ax.plot(px, py, color='red', linewidth=2, zorder=3)

# Grid lines
for x in range(1, max_x + 1):
    ax.axvline(x, color='lightgray', linewidth=0.5, zorder=4)
for y in range(1, max_y + 1):
    ax.axhline(y, color='lightgray', linewidth=0.5, zorder=4)

# Final settings
ax.set_xlim(0.5, max_x + 0.5)
ax.set_ylim(0.5, max_y + 0.5)
ax.set_xticks(range(1, max_x + 1))
ax.set_yticks(range(1, max_y + 1))
ax.set_aspect('equal')
ax.invert_yaxis()
ax.set_title('Bandalgom Coffee - Shortest Path')

plt.savefig(os.path.join(BASE_DIR, 'map_final.png'))
plt.show()