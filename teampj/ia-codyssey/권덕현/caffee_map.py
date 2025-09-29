import pandas as pd
import os

# 현재 파일 경로 기준으로 상대경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_and_clean_csv(file_name):
    file_path = os.path.join(BASE_DIR, file_name)
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # 열 이름 공백 제거
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()  # 문자열 데이터 공백 제거
    return df

# 파일 불러오기
map_df = load_and_clean_csv('area_map.csv')
struct_df = load_and_clean_csv('area_struct.csv')
category_df = load_and_clean_csv('area_category.csv')

# 구조물 ID를 이름으로 변환 (category → struct)
struct_df = struct_df.merge(category_df, how='left', on='category')

# 데이터 병합: 지도 정보와 구조물 정보 합치기
merged_df = struct_df.merge(map_df, how='left', on=['x', 'y'])

# area 기준 정렬
merged_df = merged_df.sort_values(by=['area', 'x', 'y'])

# area 1 데이터만 필터링
area1_df = merged_df[merged_df['area'] == 1].copy()

# 결과 출력
print('--- Area 1 데이터 ---')
print(area1_df.head())

# 구조물 종류별 통계 출력 (보너스)
summary = area1_df['struct'].value_counts()
print('\n--- 구조물 종류별 개수 ---')
print(summary)

# 결과 저장 (선택)
# area1_df.to_csv('area1_structures.csv', index=False)
# summary.to_csv('area1_summary.csv')