import pandas as pd

sensorActionD = {1: "화장실 이용", 2: "냉장고 이용", 3: "식사 시간", 4: "외출 시간", 5: "방문 열림", 6: "약 복용 시간"}

dir = './data/inputNormalD12-1.csv'
rData = pd.read_csv(dir, header=None)

tmp = []
for i, log in rData.iterrows():
    h = log[0]
    m = log[1]
    s = log[2]
    '''
    time = log[1]
    sensor = log[2]
    h, m, _ = time.split(':')
    h = int(h)
    m = int(m) // 10
    '''
    log_ = [h, m, s]
    tmp.append(log_)
# print(tmp[:10])
sch = set(map(tuple, tmp))
sch_l = sorted(list(sch))

# 출력 부분 좀 더 정교하게?
for l in sch_l:
    print("%d시 %d분, 센서 %d: %s" % (l[0], l[1], l[2], sensorActionD[l[2]]))
