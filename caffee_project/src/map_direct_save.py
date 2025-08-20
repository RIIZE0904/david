import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
import os
from caffee_map import load_and_analyze_data

def find_shortest_path(full_map_df, start, goal, obstacles):
    """
    BFS로 최단 경로 탐색
    """
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    # BFS 탐색
    while queue:
        current, path = queue.popleft()
        x, y = current
        if current == goal:
            return path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in obstacles and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return None


def save_path_csv(path, output_path, filename='home_to_cafe.csv'):
    """
    최단 경로를 CSV로 저장
    """
    df = pd.DataFrame(path, columns=['x', 'y'])
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(os.path.join(output_path, filename), index=False)
    print(f'최단 경로 CSV 저장 완료: {os.path.join(output_path, filename)}')


def draw_final_map(full_map_df, path, output_path, filename='map_final.png'):
    """
    최단 경로를 포함한 지도 시각화 및 이미지 저장
    """
    plt.figure(figsize=(10, 8))

    for _, row in full_map_df.iterrows():
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

    # 최단 경로(빨간 선) 그리기
    x_coords, y_coords = zip(*path)
    plt.plot(x_coords, y_coords, c='red', linewidth=2, label='Shortest Path', zorder=6)

    # 범례 중복 제거
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('Final Map with Shortest Path')
    os.makedirs(output_path, exist_ok=True)
    plt.savefig(os.path.join(output_path, filename))
    print(f'최종 지도 시각화 완료: {os.path.join(output_path, filename)}')


if __name__ == '__main__':
    df = load_and_analyze_data()
    start = tuple(df[df['struct'] == 'MyHome'][['x', 'y']].values[0])
    goal = tuple(df[df['struct'] == 'BandalgomCoffee'][['x', 'y']].values[0])
    obstacles = set(map(tuple, df[df['ConstructionSite'] == 1][['x', 'y']].values))

    path = find_shortest_path(df, start, goal, obstacles)

    if path:
        save_path_csv(path, output_path='../output')
        draw_final_map(df, path, output_path='../output')
    else:
        print('최단 경로를 찾을 수 없습니다.')
