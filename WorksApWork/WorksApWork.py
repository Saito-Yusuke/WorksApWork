# Libraries
import sys
import datetime

def main():
    
    # 変数
    statutoryWorking = 0    # 法定内残業時間数
    overtime = 0    # 法定外残業時間数
    lateNightOvertime = 0    # 深夜残業時間数
    certainHoliday = 0    # 所定休日労働時間数
    legalHoliday = 0    # 法定休日労働時間数
    
    # リスト
    inputList = []    # 入力を格納するリスト

    # 標準入力に複数行入力
    for line in sys.stdin.readlines():
        # リストに格納
        inputList.append(line.rstrip().split())

    # 1行目は使わないので消しておく
    del inputList[0]
    try:
        for i in range(len(inputList)):
            # 勤務日を取得
            # 不適切な入力に対してはここでエラー処理する
            workDate  = datetime.datetime.strptime(inputList[i][0], '%Y/%m/%d')
            tempList = []
            
            for j in range(len(inputList[i])):
                if j == 0:
                    pass
                else:
                    # 勤務開始時刻と終了時刻を取得
                    # 日付を跨ぐ場合は0時, 1時, ... となるように修正
                    if int(inputList[i][j][:2], 10) >= 24:
                        hourTemp = int(inputList[i][j][:2], 10) - 24
                        startTime = datetime.datetime.strptime(inputList[i][0] + ' ' + str(hourTemp) + inputList[i][j][2:5], '%Y/%m/%d %H:%M')
                        startTime = startTime + datetime.timedelta(days = 1)
                    else:
                        startTime = datetime.datetime.strptime(inputList[i][0] + ' ' + inputList[i][j][:5], '%Y/%m/%d %H:%M')
                    
                    if int(inputList[i][j][6:8], 10) >= 24:
                        hourTemp = int(inputList[i][j][6:8], 10) - 24
                        endTime = datetime.datetime.strptime(inputList[i][0] + ' ' + str(hourTemp) + inputList[i][j][8:], '%Y/%m/%d %H:%M')
                        endTime = endTime + datetime.timedelta(days = 1)
                    else:
                        endTime = datetime.datetime.strptime(inputList[i][0] + ' ' + inputList[i][j][6:], '%Y/%m/%d %H:%M')
                    
                    # 労働時間を計算
                    workTime = endTime - startTime
                    tempList.append(workTime.seconds / 60)

                    # 法定内残業時間・休日労働時間の計算
                    # 曜日で分岐
                    if startTime.weekday() < 5:    # 平日
                        if startTime < datetime.datetime.strptime(inputList[i][0] + ' 08:00', '%Y/%m/%d %H:%M'):    # 開始時刻が8時以前のとき
                            if endTime < datetime.datetime.strptime(inputList[i][0] + ' 08:00', '%Y/%m/%d %H:%M'):    # 終了時刻も8時以前なら
                                statutoryWorking += workTime.seconds / 60    # 法定内残業時間にそのまま加える
                            else:
                                statutoryTemp = datetime.datetime.strptime(inputList[i][0] + ' 08:00', '%Y/%m/%d %H:%M') - startTime    # 8時以前の分を計算
                                statutoryWorking += statutoryTemp.seconds / 60
                        
                        if endTime > datetime.datetime.strptime(inputList[i][0] + ' 16:00', '%Y/%m/%d %H:%M'):    # 終了時刻が16時以降のとき
                            if startTime > datetime.datetime.strptime(inputList[i][0] + ' 16:00', '%Y/%m/%d %H:%M'):    # 開始時刻も16時以降なら
                                statutoryWorking += workTime.seconds / 60    # 法定内残業時間にそのまま加える
                            else:
                                statutoryTemp = endTime - datetime.datetime.strptime(inputList[i][0] + ' 16:00', '%Y/%m/%d %H:%M')    # 16時超過分を計算
                                statutoryWorking += statutoryTemp.seconds / 60
                    
                        if endTime.weekday() == 5:    # 金曜について日付を跨いだ場合
                            if startTime.weekday() == 5:    # 開始時刻も日付を跨いでいるなら
                                certainHoliday += workTime.seconds / 60    # 所定休日労働時間にそのまま加える
                            else:
                                certainTemp = endTime - (datetime.datetime.strptime(inputList[i][0] + ' 00:00', '%Y/%m/%d %H:%M') + datetime.timedelta(days = 1))    # 0時超過分を計算
                                certainHoliday += certainTemp.seconds / 60

                    elif startTime.weekday() == 5:    # 土曜
                        if endTime.weekday() == 6:    # 日付を跨いだ場合
                            if startTime.weekDay() == 6:    # 開始時刻も日付を跨いでいるなら
                                legalHoliday += workTime.seconds / 60    # 法定休日労働時間にそのまま加える
                            else:
                                certainTemp = (datetime.datetime.strptime(inputList[i][0] + ' 00:00', '%Y/%m/%d %H:%M') + datetime.timedelta(days = 1))    # 0時までの時間を計算
                                certainHoliday += certainTemp.seconds / 60    # 所定休日労働時間に加える
                                legalTemp = endTime - (datetime.datetime.strptime(inputList[i][0] + ' 00:00', '%Y/%m/%d %H:%M') + datetime.timedelta(days = 1))    # 0時超過分を計算
                                legalHoliday += legalTemp.seconds / 60    # 法定休日労働時間に加える
                        else:
                            certainHoliday += workTime.seconds / 60    # 所定休日労働時間にそのまま加える

                    elif startTime.weekDay() == 6:    # 日曜
                        legalHoliday += workTime.seconds / 60    # 法定休日労働時間に加える

                    # 深夜残業時間を計算
                    if endTime > datetime.datetime.strptime(inputList[i][0] + ' 22:00', '%Y/%m/%d %H:%M'):    # 終了時刻が22時以降のとき
                        if startTime >= datetime.datetime.strptime(inputList[i][0] + ' 22:00', '%Y/%m/%d %H:%M'):    # 開始時刻も22時以降なら
                            lateNightOvertime += workTime.seconds / 60    # そのまま加える
                        else:
                            lateNightTemp = endTime - datetime.datetime.strptime(inputList[i][0] + ' 22:00', '%Y/%m/%d %H:%M')    # 22時超過分を計算
                            lateNightOvertime += lateNightTemp.seconds / 60

            # 1日の労働時間を計算
            workMinutes = sum(tempList)

            # 8時間を超えたならば法定外残業を計算
            if workMinutes >= 480.0:
                overtimeTemp = workMinutes - 480.0
                overtime += overtimeTemp
                statutoryWorking -= overtimeTemp    # 法定内残業と重複する分を除く

    except Exception:
        sys.stderr.write('エラーが発生したので終了します. ')
        sys.exit()

    # 出力
    print(str(round(statutoryWorking / 60)))
    print(str(round(overtime / 60)))
    print(str(round(lateNightOvertime / 60)))
    print(str(round(certainHoliday / 60)))
    print(str(round(legalHoliday / 60)))

if __name__ == "__main__":
    main()