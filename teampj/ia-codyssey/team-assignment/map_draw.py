import matplotlib.pyplot as plt
import pandas as pd
import os

# 1. CSV 파일 읽기
# base_dir: 현재 파일의 디렉토리 경로
# data_dir: 데이터 파일이 있는 디렉토리 경로
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "dataFile")

area_map = pd.read_csv(os.path.join(data_dir, "area_map.csv"))
area_struct = pd.read_csv(os.path.join(data_dir, "area_struct.csv"))
area_category = pd.read_csv(os.path.join(data_dir, "area_category.csv"))

# 2. 구조물 ID를 이름으로 변환
area_struct = area_struct.merge(area_category, how='left', on='category')

# 3. 세 데이터 병합 (좌표 기준)
merged = area_struct.merge(area_map, how='left', on=['x', 'y'])

# 4. area 기준 정렬
merged = merged.sort_values(by='area')

# 6. 시각화
# 좌표 범위 계산
x_min, x_max = merged['x'].min(), merged['x'].max()
y_min, y_max = merged['y'].min(), merged['y'].max()

plt.figure(figsize=(10, 8))

# 그리드 라인


for x in range(int(x_min), int(x_max) + 1):
    plt.axvline(x=x, color='lightgray', linestyle='--', linewidth=0.5, zorder=0)
for y in range(int(y_min), int(y_max) + 1):
    plt.axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5, zorder=0)

# 건설 현장 먼저 그림 (겹칠 때 우선) (회색 사각형)
construction = merged[merged['ConstructionSite'] == 1]
# scatter 함수 파라미터 설명
# marker: 마커 모양, s: 마커 크기, color: 마커 색상, label: 범례 이름, zorder: 레이어 순서
# 건설현장이 우선시 되어야 하면 zorder를 높게 설정
plt.scatter(construction['x'], construction['y'], marker='s', s=400, color='gray', label='Construction Site', zorder=3)

# 아파트와 빌딩(갈색 원형)
for struct in ['Apartment', 'Building']:
    subset = merged[(merged['struct'] == struct) & (merged['ConstructionSite'] != 1)]
    if not subset.empty:
        plt.scatter(subset['x'], subset['y'], marker='o', s=300, color='brown', label=struct, zorder=2)

# 반달곰 커피(녹색 사각형)
cafe = merged[(merged['struct'] == 'BandalgomCoffee') & (merged['ConstructionSite'] != 1)]
plt.scatter(cafe['x'], cafe['y'], marker='s', s=400, color='green', label='Bandalgom Coffee', zorder=4)

# 내 집 (녹색 삼각형)
my_home = merged[(merged['struct'] == 'MyHome') & (merged['ConstructionSite'] != 1)]
plt.scatter(my_home['x'], my_home['y'], marker='^', s=300, color='green', label='My Home', zorder=5)

# 범례 (중복 방지)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='upper right')


# 축 설정
plt.xlim(x_min - 1, x_max + 1)
plt.ylim(y_min - 1, y_max + 1)
# gca(): 현재 Axes 객체를 가져옴
# set_aspect('equal')는 x축과 y축의 단위 길이를 동일하게 설정하여 비율을 유지
# adjustable='box'는 박스 형태로 유지
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Area 1 Map Visualization')

# tight_layout()는 레이아웃을 자동으로 조정하여 요소들이 겹치지 않도록 함
plt.tight_layout()

# Save image
plt.savefig(os.path.join(base_dir, 'map.png'), dpi=300, bbox_inches='tight')
plt.show()
