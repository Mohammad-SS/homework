from django.shortcuts import render, HttpResponse
from eaecontrol import models
from django.views.decorators.csrf import csrf_exempt
import jdatetime
import datetime
import csv
import locale


@csrf_exempt
def sumbitEnter(request):
    userId = request.POST['id']
    user = models.Person.objects.filter(id=userId)
    user.update(isIn=True)
    timing = models.Timing(person=user[0], type=1)
    timing.save()
    return HttpResponse('Done')


@csrf_exempt
def sumbitExit(request):
    userId = request.POST['id']
    user = models.Person.objects.filter(id=userId)
    user.update(isIn=False)
    timing = models.Timing(person=user[0], type=0)
    timing.save()
    return HttpResponse('Done')


def showTable(request):
    users = models.Person.objects.order_by('id')
    jdatetime.set_locale("fa_IR")
    context = {'users': users, 'date': jdatetime.datetime.now().strftime('%Y/%-m/%-d')}
    return render(request, 'eaecontrol/index.html', context)


def showPersonReport(request, id, m, y):
    user = models.Person.objects.get(pk=id)
    print(user)
    mindata = jdatetime.datetime(y, m, 1).togregorian()
    if(m == 12):
        maxdata = jdatetime.datetime(y+1, 1, 1).togregorian() - datetime.timedelta(days=1)
    else:
        maxdata = jdatetime.datetime(y, m+1, 1).togregorian() - datetime.timedelta(days=1)
    range = [mindata, maxdata]
    alltimes = models.Timing.objects.filter(person=user, date__range=range).order_by("-id")
    context = {'times': alltimes, 'user': user, 'year': y, 'month': m, 'person': id}
    return render(request, 'eaecontrol/personTimes.html', context)

    # this_date = mindata
    # data = {}
    # datesArray = {}
    # print(type(data))
    # i = 1
    # while (this_date < maxdata):
    #     dates = alltimes.filter(date=this_date)
    #     if(dates.count()):
    #         datesArray[this_date] = {}
    #     this_date = this_date + datetime.timedelta(days=1)
    #     i = i + 1
    # for date in dates:
    #     this_date = alltimes.filter(date=date)
    #     datesArray[date][]
    # # t =
    # print(data)


def selectPerson(request):
    users = models.Person.objects.filter()
    months = [(1, 'فروردین'), (2, 'اردیبهشت'), (3, 'خرداد'), (4, 'تیر'), (5, 'مرداد'),
              (6, 'شهریور'), (7, 'مهر'), (8, 'آبان'), (9, 'آذر'), (10, 'دی'),
              (11, 'بهمن'), (12, 'اسفند')]
    years = [(1399, '1399')]
    print(type(months))
    context = {'users': users, 'months': months, 'years': years}
    return render(request, 'eaecontrol/selectPerson.html', context)


def selectMonth(request):
    months = [(1, 'فروردین'), (2, 'اردیبهشت'), (3, 'خرداد'), (4, 'تیر'), (5, 'مرداد'),
              (6, 'شهریور'), (7, 'مهر'), (8, 'آبان'), (9, 'آذر'), (10, 'دی'),
              (11, 'بهمن'), (12, 'اسفند')]
    years = [(1399, '1399')]
    print(type(months))
    context = {'months': months, 'years': years}
    return render(request, 'eaecontrol/selectMonth.html', context)


def showMounthlyReport(request, y, m):
    users = models.Person.objects.filter()
    datesArray = []
    persianMinDate = jdatetime.datetime(y, m, 1)
    if m ==12:
        persianMaxData = jdatetime.datetime(y+1, 1, 1) - datetime.timedelta(days=1)
    else :
        persianMaxData = jdatetime.datetime(y, m + 1, 1) - datetime.timedelta(days=1)
    persianRange = [persianMinDate.date().strftime('%Y/%m/%d'), persianMaxData.date().strftime('%Y/%m/%d')]
    range = [persianMinDate.togregorian(), persianMaxData.togregorian()]
    i = 0
    data = []
    for user in users:
        thisUser = {}
        group = user.group
        print(user)
        standardEnterTime = user.group.standardEnter
        standardExitTime = user.group.standardExit
        times = models.Timing.objects.filter(person=user, date__range=range)
        sumEnter = datetime.timedelta(hours=0, minutes=0, seconds=0)
        sumExit = datetime.timedelta(hours=0, minutes=0, seconds=0)
        for time in times:
            if time.type == 1:
                if time.time < standardEnterTime:
                    time.time = standardEnterTime
                sumEnter = sumEnter + datetime.timedelta(hours=time.time.hour, minutes=time.time.minute,
                                                         seconds=time.time.second)
            if time.type == 0:
                if time.time > standardExitTime:
                    time.time = standardExitTime
                sumExit = sumExit + datetime.timedelta(hours=time.time.hour, minutes=time.time.minute,
                                                       seconds=time.time.second)

        montlyWorks = sumExit - sumEnter
        thisUser['user'] = user
        thisUser['group'] = group
        thisUser['monthlyWork'] = montlyWorks
        data.append(thisUser)
    print(data)
    context = {'data': data, 'timeRange': persianRange, 'month': m, 'year': y}
    return render(request, 'eaecontrol/monthlyTimes.html', context)


def downloadMReport(request, y, m):
    users = models.Person.objects.filter()
    persianMinDate = jdatetime.datetime(y, m, 1)
    persianMaxData = jdatetime.datetime(y, m + 1, 1) - datetime.timedelta(days=1)
    range = [persianMinDate.togregorian(), persianMaxData.togregorian()]
    response = HttpResponse(content_type='text/csv')
    filename = str(y) + "/" + str(m) + "_" + "Report" + ".csv"
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(["کد", "نام کاربر", "گروه کاربری", "میزان کارکرد ماهانه"])
    for user in users:
        print(user)
        standardEnterTime = user.group.standardEnter
        standardExitTime = user.group.standardExit
        times = models.Timing.objects.filter(person=user, date__range=range)
        sumEnter = datetime.timedelta(hours=0, minutes=0, seconds=0)
        sumExit = datetime.timedelta(hours=0, minutes=0, seconds=0)
        for time in times:
            if time.type == 1:
                if time.time < standardEnterTime:
                    time.time = standardEnterTime
                sumEnter = sumEnter + datetime.timedelta(hours=time.time.hour, minutes=time.time.minute,
                                                         seconds=time.time.second)
            if time.type == 0:
                if time.time > standardExitTime:
                    time.time = standardExitTime
                sumExit = sumExit + datetime.timedelta(hours=time.time.hour, minutes=time.time.minute,
                                                       seconds=time.time.second)

        montlyWorks = sumExit - sumEnter
        writer.writerow([user.id, user.name, user.group, montlyWorks])

    return response


def downloadPReport(request , id , y , m):
    user = models.Person.objects.get(pk=id)
    response = HttpResponse(content_type='text/csv')
    filename = str(y) + "/" + str(m) + "_" + "_" + "User " + str(id)  + ".csv"
    print(filename)
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(["کد", "نام کاربر", "تاریخ", "ورود/خروج" , "ساعت"])
    mindata = jdatetime.datetime(y, m, 1).togregorian()
    maxdata = jdatetime.datetime(y, m + 1, 1).togregorian()
    range = [mindata, maxdata]
    alltimes = models.Timing.objects.filter(person=user, date__range=range).order_by("-id")
    for time in alltimes:
        writer.writerow([time.id , time.person.name , time.persianDate , time.operation , time.formatedTime])
    print(alltimes)
    return response
