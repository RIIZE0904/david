import pandas as pd
import os

def load_and_analyze_data(area=1):
    """
    데이터 로드 및 전처리
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

    # 병합 전에 모든 컬럼명 공백 제거
    area_struct.columns = area_struct.columns.str.strip()
    area_map.columns = area_map.columns.str.strip()
    area_category.columns = area_category.columns.str.strip()


    # 카테고리 이름 병합
    area_struct = area_struct.merge(area_category, how='left', on='category')

    # 좌표 기준 데이터 병합
    merged = area_struct.merge(area_map, how='left', on=['x', 'y'])
    merged = merged.sort_values(by='area')


    # area=1 데이터 필터링
    filtered = merged[merged['area'] == area]

    # 구조물 통계 출력
    if 'struct' in filtered.columns:
        print(f"\n=== area {area} 구조물 종류별 통계 ===")
        print(filtered['struct'].value_counts())
    else:
        print(f"\n[경고] area {area} 데이터에 'struct' 컬럼이 없습니다.")
        print("현재 컬럼 목록:", filtered.columns.tolist())

    return filtered

if __name__ == '__main__':
    df = load_and_analyze_data()
    print("\n=== area 1 데이터 미리보기 ===")
    print(df.head())
