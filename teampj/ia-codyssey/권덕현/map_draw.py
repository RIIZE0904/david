import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# 현재 파일 경로 기준으로 상대경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_and_clean_csv(file_name):
    path = os.path.join(BASE_DIR, file_name)
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

# 파일 불러오기
map_df = load_and_clean_csv('area_map.csv')
struct_df = load_and_clean_csv('area_struct.csv')
category_df = load_and_clean_csv('area_category.csv')

# 구조물 이름 병합
struct_df = struct_df.merge(category_df, how='left', on='category')

# 공사현장 정보 병합
merged_df = struct_df.merge(map_df, how='left', on=['x', 'y'])

# 좌표 범위 설정
max_x = merged_df['x'].max() + 1
max_y = merged_df['y'].max() + 1

# 시각화 시작
fig, ax = plt.subplots(figsize=(12, 12))

# Area 구간 배경색 칠하기
def get_area_color(area):
    colors = {0: '#fff8dc', 1: '#e6f2ff', 2: '#e6ffe6', 3: '#ffe6cc'}
    return colors.get(area, '#ffffff')

for _, row in merged_df.iterrows():
    x, y, area = row['x'], row['y'], row['area']
    ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=get_area_color(area), zorder=0))

# ConstructionSite만 추려서 따로 그림
construction_sites = merged_df[merged_df['ConstructionSite'] == 1][['x', 'y']]
construction_coords = set((row.x, row.y) for _, row in construction_sites.iterrows())

for (x, y) in construction_coords:
    ax.add_patch(plt.Rectangle((x - 0.35, y - 0.35), 0.7, 0.7, color='gray', zorder=1))

# 구조물 그리기 (단, ConstructionSite와 겹치면 무시)
for _, row in merged_df.iterrows():
    x, y = row['x'], row['y']
    if (x, y) in construction_coords:
        continue  # 건설 현장이 우선

    struct = row['struct']
    if struct == 'BandalgomCoffee':
        ax.add_patch(plt.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color='green', zorder=2))
    elif struct == 'MyHome':
        ax.plot(x, y, marker='^', color='green', markersize=12, zorder=2)
    elif struct == 'Apartment':
        ax.plot(x, y, 'o', color='saddlebrown', markersize=10, zorder=2)
    elif struct == 'Building':
        ax.plot(x, y, 'o', color='saddlebrown', markersize=10, zorder=2)

# 격자 그리기
for x in range(1, max_x + 1):
    ax.axvline(x, color='lightgray', linewidth=0.5, zorder=3)
for y in range(1, max_y + 1):
    ax.axhline(y, color='lightgray', linewidth=0.5, zorder=3)

# 범례 추가
legend_elements = [
    Patch(facecolor='gray', edgecolor='gray', label='ConstructionSite'),
    Patch(facecolor='green', edgecolor='green', label='BandalgomCoffee'),
    Line2D([0], [0], marker='^', color='w', label='MyHome', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Apartment', markerfacecolor='saddlebrown', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Building', markerfacecolor='saddlebrown', markersize=10)
]
ax.legend(handles=legend_elements, loc='upper left')

# 좌표 축 설정
ax.set_xlim(0.5, max_x + 0.5)
ax.set_ylim(0.5, max_y + 0.5)
ax.set_xticks(range(1, max_x + 1))
ax.set_yticks(range(1, max_y + 1))
ax.set_aspect('equal')
ax.invert_yaxis()
ax.set_title('Bandalgom Coffee Map')

# 이미지 저장
output_path = os.path.join(BASE_DIR, 'map.png')
plt.savefig(output_path)
plt.show()