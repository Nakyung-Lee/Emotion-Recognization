import pandas as pd
import numpy as np

class Model:
    def __init__(self):
        '''
        __init__() : 초기화 함수
        '''

    ## 날짜와 시세 데이터 병합 함수 ##
    def merge_date_with_price(self):

        '''
        merge_date_with_price() : 날짜와 시세 데이터 병합 함수 
                label : ( 0: 시세 변동 없음, 1: 상승, -1: 하락, 휴장 )

                output : 날짜와 시세 데이터 병합 
        '''

        # 각 데이터 로드 
        closing_day = pd.read_csv('C:/Users/82102/OneDrive/문서/Nakyung-Emotion-Recognization/News_Crawling/NK/2021_closing_day.csv')

        price_labeling = pd.read_csv('C:/Users/82102/OneDrive/문서/Nakyung-Emotion-Recognization/News_Crawling/NK/price_crawling.csv')

        # 날짜에 맞춰 데이터 병합 
        merge_data = pd.merge(closing_day,price_labeling,how='outer')
        print(merge_data)

        merge_data.drop(columns=['day','close','open','high','low','volume'],axis=1,inplace=True)
        
        # NaN 값 -> NaN 이후 가까운 라벨 값으로 대체 
        # EX ) 토,일 -> 월 
        for idx in range(len(merge_data)):
            if np.isnan(merge_data['diff'][idx]) :
                merge_data['diff'][idx]=merge_data['diff'][idx-1]
            elif merge_data['diff'][idx]<0:
                merge_data['diff'][idx]=-1
            elif merge_data['diff'][idx]>0:
                merge_data['diff'][idx]=1
            else:
                merge_data['diff'][idx]=0
            
        merge_data = merge_data.rename(columns={'date':'date','closing':'closing','diff':'label'})

        # 최종 데이터 column 순서 정리 후, csv 파일로 저장
        merge_data = merge_data[['date','closing','label']]
        print(merge_data)

        merge_data['label'] = merge_data['label'].astype(int)
        merge_data.to_csv("C:/Users/82102/OneDrive/문서/Nakyung-Emotion-Recognization/News_Crawling/NK/[대한항공]label.csv",header=True,index=False)
        

if __name__ == "__main__":
    emotion_modeling = Model()
    emotion_modeling.merge_date_with_price()