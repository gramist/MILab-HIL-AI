import pandas as pd

sensorActionD = {1: "화장실 이용", 2: "냉장고 이용", 3: "식사 시간", 4: "외출 시간", 5: "방문 열림", 6: "약 복용 시간", 7: "기타"}

dir = '../data/inputNormalD12-1.csv'
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

data_list = []
tmp = ['', '', '']
cnt = 0
# 출력 부분 좀 더 정교하게?
for l in sch_l:
    str_data = "%02d:%02d, %s" % (l[0], l[1], sensorActionD[l[2]])
    tmp[cnt] = sensorActionD[l[2]]

    cnt += 1
    if cnt == 3:
        cnt = 0

    # if (("%02d" % (l[0])) == "06") or (("%02d" % (l[0])) == "07"):
    #     if (sensorActionD[l[2]] == '방문 열림') or (sensorActionD[l[2]] == '냉장고 이용')

    print(str_data)
