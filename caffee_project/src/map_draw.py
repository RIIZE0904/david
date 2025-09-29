import matplotlib.pyplot as plt
import os
from caffee_map import load_and_analyze_data

def draw_map(full_map_df, output_path, filename='map.png'):
    """
    지도 시각화 및 이미지 저장
    """
    plt.figure(figsize=(10, 8))

    # 각 좌표에 대해 구조물 시각화
    for _, row in full_map_df.iterrows():
        # scatter 함수 파라미터 설명
        # marker: 마커 모양, s: 마커 크기, color: 마커 색상, label: 범례 이름, zorder: 레이어 순서
        # 건설현장이 우선시 되어야 하면 zorder를 높게 설정
        if row['ConstructionSite'] == 1:
            plt.scatter(row['x'], row['y'], c='gray', marker='s', s=400, label='Construction Site', zorder=3)
        elif row['struct'] == 'Apartment':
            plt.scatter(row['x'], row['y'], c='brown', marker='o', s=300, label='Apartment', zorder=2)
        elif row['struct'] == 'Building':
            plt.scatter(row['x'], row['y'], c='brown', marker='o', s=300, label='Building', zorder=2)
        elif row['struct'] == 'BandalgomCoffee':
            plt.scatter(row['x'], row['y'], c='green', marker='s', s=400, label='Bandalgom Coffee', zorder=4)
        elif row['struct'] == 'MyHome':
            plt.scatter(row['x'], row['y'], c='green', marker='^', s=400, label='My Home', zorder=5)

    # 그리드 라인 추가
    x_min, x_max = full_map_df['x'].min(), full_map_df['x'].max()
    y_min, y_max = full_map_df['y'].min(), full_map_df['y'].max()
    for x in range(int(x_min), int(x_max) + 1):
        plt.axvline(x=x, color='lightgray', linestyle='--', linewidth=0.5, zorder=0)
    for y in range(int(y_max), int(y_min) - 1, -1):
        plt.axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5, zorder=0)

    # 범례 중복 제거
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')

    # 축 설정 및 저장
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('Area Map Visualization')
    os.makedirs(output_path, exist_ok=True)
    plt.savefig(os.path.join(output_path, filename))
    print(f'지도 시각화 완료: {os.path.join(output_path, filename)}')


if __name__ == '__main__':
    # 데이터 로드
    df = load_and_analyze_data()
    draw_map(df, output_path='../output')
