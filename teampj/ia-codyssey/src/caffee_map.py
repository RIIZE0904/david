
import pandas as pd
import os

def load_and_analyze_data(area=1):
    """
    📄 데이터 로드 및 전처리
    - 3개의 CSV 파일을 불러오고 병합
    - area 기준 필터링
    - 구조물 통계 출력
    """
    # 1. CSV 파일 읽기
    # base_dir: 현재 파일의 디렉토리 경로
    # data_dir: 데이터 파일이 있는 디렉토리 경로
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '../data')

    area_map = pd.read_csv(os.path.join(data_dir, 'area_map.csv'))
    area_struct = pd.read_csv(os.path.join(data_dir, 'area_struct.csv'))
    area_category = pd.read_csv(os.path.join(data_dir, 'area_category.csv'))

    area_struct = area_struct.merge(area_category, how='left', on='category')
    merged = area_struct.merge(area_map, how='left', on=['x', 'y'])
    merged = merged.sort_values(by='area')
    filtered = merged[merged['area'] == area]

    print("\n=== area {} 구조물 종류별 통계 ===".format(area))
    print(filtered['struct'].value_counts())

    return filtered

if __name__ == '__main__':
    df = load_and_analyze_data()
    print("\n=== area 1 데이터 미리보기 ===")
    print(df.head())
