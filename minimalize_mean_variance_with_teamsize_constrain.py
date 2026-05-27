import pulp
import math
import random

#ここにメンバー数と、基本のチームサイズを入力(余る場合はBASE_TEAM_SIZE+1人班ができます)
MEMBER_COUNT = 16
BASE_TEAM_SIZE = 4

ADJUST_TEAM_COUNT = MEMBER_COUNT % BASE_TEAM_SIZE
TEAM_COUNT = (MEMBER_COUNT//BASE_TEAM_SIZE)
M, N = MEMBER_COUNT, TEAM_COUNT

#ここにパラメーターを入力
#元のデータ上でパラメーターが複数ある場合は重みをかけて足し合わせる
#[重要] 後半でやってる酷いコードの影響で、パラメータの値が小さい人がある程度発生するように調整するとうまくいきやすいかも(1とか2くらい)
#(よくない設定でも動くことを確かめるために１が少なくなりやすい設定で試している -> 大体うまく動いた)

#SAMPLE
input_data = {
    "NAME1": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME2": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME3": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME4": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME5": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME6": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME7": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME8": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME9": { "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME10":{ "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME11":{ "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME12":{ "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME13":{ "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME14":{ "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME15":{ "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) },
    "NAME16":{ "param1" : math.ceil(random.randint(1,16)**0.5), "param2": math.ceil(random.randint(1,16)**0.5) }
}

### ※input_dataのkeysに順序の保証があることを前提 ないならどうにかして ###
MEMBER_NAME_TAG = [*input_data.keys()]

### これ設定する ###
GetSummaryParam = lambda params: params["param1"] * 0.9 + params["param1"] * 0.1


#parametorArray = [math.ceil(random.randint(1,16)**0.5) for _ in range(MEMBER_COUNT)] 
parametorArray = [GetSummaryParam(value) for value in input_data.values()]
x = [[pulp.LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(N)] for i in range(M)]

z = [pulp.LpVariable(f"z_{i}", lowBound=0) for i in range(N)]

problem = pulp.LpProblem("Labeling", pulp.LpMaximize)

for i in range(M):
    problem += sum(x[i][j] for j in range(N)) == 1

for j in range(ADJUST_TEAM_COUNT):
    problem += sum(x[i][j] for i in range(M)) >= BASE_TEAM_SIZE
    problem += sum(x[i][j] for i in range(M)) <= BASE_TEAM_SIZE + 1

for j in range(ADJUST_TEAM_COUNT, N):
    problem += sum(x[i][j] for i in range(M)) == BASE_TEAM_SIZE

u = sum(parametorArray[:M])/N

for j in range(N):
    #無理やりだけど大体平均より大きいという制約をつけることで、絶対値(2乗の√)が線形じゃないので使えない問題を回避
    problem += (sum(x[i][j] * parametorArray[i] for i in range(M)) - u) + 1 >= 0
problem += sum((sum(x[i][j] * parametorArray[i] for i in range(M)) - u) for j in range(N))

problem.solve()

noDuplicate = True
for i in range(M):
    tmp = 1 == sum(pulp.value(x[i][j]) for j in range(N))
    print(f"1 == {tmp}")
    noDuplicate &= tmp

for j in range(N):
    print(f"team[{j}] info:")
    print(f"\tcount {sum(pulp.value(x[i][j]) for i in range(M))}")
    print(f"\tability {sum(pulp.value(x[i][j]) * parametorArray[i] for i in range(M))}")
    
    print(f"\tmembers {",".join(filter(lambda mem: mem != "no", [str(MEMBER_NAME_TAG[i]) if pulp.value(x[i][j]) else str("no") for i in range(M)]))}")


#ここがFalseだと、誰かが複数のチームに割り当てられてしまっている
print(f"\n{noDuplicate=}")
#最適化の際に目標にしている値
print(f"idealAbility = {u}")

