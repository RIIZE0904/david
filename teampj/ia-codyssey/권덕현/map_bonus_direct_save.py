import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import deque
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_and_clean_csv(file_name):
    """CSV 파일을 읽고 공백 제거"""
    path = os.path.join(BASE_DIR, file_name)
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

def bfs(start, goal, grid):
    """두 점 사이 최단 경로 탐색 (공사현장 피하기)"""
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
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if neighbor in grid and grid[neighbor]['walkable'] and neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return []

# 데이터 로드
map_df = load_and_clean_csv('area_map.csv')
struct_df = load_and_clean_csv('area_struct.csv')
category_df = load_and_clean_csv('area_category.csv')

merged_df = struct_df.merge(category_df, how='left', on='category').merge(map_df, how='left', on=['x', 'y'])

# 그리드 생성
grid = {}
home = None
cafe_locations = []
structure_coords = []

for _, row in merged_df.iterrows():
    x, y = int(row['x']), int(row['y'])
    key = (x, y)
    grid[key] = {
        'walkable': row['ConstructionSite'] != 1,
        'type': row['struct']
    }

    struct = row['struct']
    if struct == 'MyHome':
        home = (x, y)
    elif struct == 'BandalgomCoffee':
        cafe_locations.append((x, y))
    elif struct and struct not in ['MyHome', 'BandalgomCoffee']:
        structure_coords.append((x, y))

# 모든 구조물 방문 + 반달곰 커피점으로 종료
visited_points = set()
bonus_path = [home]
current = home

while len(visited_points) < len(structure_coords):
    # 방문하지 않은 구조물 중 가장 가까운 것 선택
    next_point = min(
        (p for p in structure_coords if p not in visited_points),
        key=lambda p: abs(p[0] - current[0]) + abs(p[1] - current[1])
    )
    sub_path = bfs(current, next_point, grid)
    bonus_path.extend(sub_path[1:])  # 중복 방지
    visited_points.add(next_point)
    current = next_point

# 마지막으로 가까운 반달곰 커피점으로 이동
final_cafe = min(cafe_locations, key=lambda p: abs(p[0] - current[0]) + abs(p[1] - current[1]))
final_path = bfs(current, final_cafe, grid)
bonus_path.extend(final_path[1:])

# CSV 저장
bonus_df = pd.DataFrame(bonus_path, columns=['x', 'y'])
bonus_df.to_csv(os.path.join(BASE_DIR, 'home_to_cafe_bonus.csv'), index=False)

# 지도 시각화
max_x, max_y = merged_df['x'].max() + 1, merged_df['y'].max() + 1
fig, ax = plt.subplots(figsize=(12, 12))

# Area 색상
area_colors = {0: '#fff8dc', 1: '#e6f2ff', 2: '#e6ffe6', 3: '#ffe6cc'}
for _, row in merged_df.iterrows():
    x, y, area = row['x'], row['y'], row['area']
    ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=area_colors.get(area, '#ffffff'), zorder=0))

# 공사현장
for (x, y), info in grid.items():
    if not info['walkable']:
        ax.add_patch(plt.Rectangle((x - 0.35, y - 0.35), 0.7, 0.7, color='gray', zorder=1))

# 구조물
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

# 보너스 경로 (파란 점선)
px, py = zip(*bonus_path)
ax.plot(px, py, color='blue', linestyle='--', linewidth=2, label='Bonus Path', zorder=3)

# 범례 추가
legend_elements = [
    Patch(facecolor='gray', edgecolor='gray', label='ConstructionSite'),
    Patch(facecolor='green', edgecolor='green', label='BandalgomCoffee'),
    Line2D([0], [0], marker='^', color='w', label='MyHome', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Apartment', markerfacecolor='saddlebrown', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Building', markerfacecolor='saddlebrown', markersize=10)
]
ax.legend(handles=legend_elements, loc='upper left')

# 그리드
for x in range(1, max_x + 1):
    ax.axvline(x, color='lightgray', linewidth=0.5, zorder=4)
for y in range(1, max_y + 1):
    ax.axhline(y, color='lightgray', linewidth=0.5, zorder=4)

# 설정
ax.set_xlim(0.5, max_x + 0.5)
ax.set_ylim(0.5, max_y + 0.5)
ax.set_aspect('equal')
ax.invert_yaxis()
ax.set_title('Bandalgom Coffee Map with Bonus Path')
ax.legend()

# 이미지 저장
plt.savefig(os.path.join(BASE_DIR, 'map_bonus_final.png'))
plt.show()
