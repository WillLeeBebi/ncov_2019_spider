

# 地级市
select *
from (
select a.id,
       a._id,
       a.provinceName,
       b.cityName,
       b.confirmedCount                                              '确认感染',
       b.deadCount                                                   '死亡数',
       b.curedCount                                                  '治愈',
#        a.suspectedCount                                              '疑似',
       from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') as utime


from dxyarea a,
     dxyarea_city b
where from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') >=
      str_to_date('2020-01-30  00:00:00', '%Y-%m-%d %H:%i:%s')
  and from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') <=
      str_to_date('2020-01-30  23:59:00', '%Y-%m-%d %H:%i:%s')
  and a.updateTime = (SELECT MAX(updateTime + 0)
                      FROM dxyarea_city
                      WHERE cityName = b.cityName)
  and a.country = '中国'
  and a._id = b.dxyarea_id
group by  b.cityName) aa
order by aa.确认感染 desc, aa.provinceName,  aa.cityName;

#
# select *
# from dxyarea a
#
# where from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') >=
#       str_to_date('2020-01-30  00:00:00', '%Y-%m-%d %H:%i:%s')
#   and from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') <=
#       str_to_date('2020-01-30  23:59:00', '%Y-%m-%d %H:%i:%s')
# and a.provinceName like '%海南%'

# 省级数据
select a.id,
       a._id,
       max(CAST(a.updateTime as SIGNED))                          as mutime,
       a.confirmedCount                                              '确认感染',
       a.deadCount                                                   '死亡数',
       a.curedCount                                                  '治愈',
#        a.suspectedCount                                              '疑似',
       from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') as utime,
       a.provinceName,
       a.confirmedCount,
       a.*
from dxyarea a
where from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') >=
      str_to_date('2020-01-29  00:00:00', '%Y-%m-%d %H:%i:%s')
  and from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') <=
      str_to_date('2020-01-30  23:59:00', '%Y-%m-%d %H:%i:%s')
  and a.updateTime = (SELECT MAX(updateTime + 0)
                      FROM dxyarea
                      WHERE provinceName = a.provinceName)
  and a.country = '中国'
group by a.provinceName, a.confirmedCount
order by a.confirmedCount desc;


# 省级，每天的
select a.id,
       a._id,
              a.provinceName,
       a.confirmedCount                                              '确认感染',
       a.deadCount                                                   '死亡数',
       a.curedCount                                                  '治愈',
#        a.suspectedCount                                              '疑似',
       from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') as utime,
       from_unixtime(left(a.updateTime, 10), '%Y-%m-%d') as udate,

       a.confirmedCount,
       a.*
from dxyarea a
where from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') >=
      str_to_date('2020-01-24  00:00:00', '%Y-%m-%d %H:%i:%s')
  and from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') <=
      str_to_date('2020-01-30  23:59:00', '%Y-%m-%d %H:%i:%s')

  and a.country = '中国'
order by a.provinceName, utime desc;


# 概览
select sum(aa.confirmedCount) as '确诊总数',
       sum(aa.deadCount)      as '死亡数',
       sum(aa.curedCount)     as '治愈',
       aa.utime,
       aa.udate
#        sum(aa.suspectedCount) as '疑似'
from (
         select a.id,
                a._id,
                a.confirmedCount,
       from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') as utime,
       from_unixtime(left(a.updateTime, 10), '%Y-%m-%d') as udate,
                a.deadCount,
                a.curedCount,
                a.suspectedCount,
                 a.provinceName
         from dxyarea a
         where from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') >=
               str_to_date('2020-01-29  00:00:00', '%Y-%m-%d %H:%i:%s')
           and from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') <=
               str_to_date('2020-01-30  23:59:00', '%Y-%m-%d %H:%i:%s')
           and a.updateTime = (SELECT MAX(updateTime + 0)
                               FROM dxyarea
                               WHERE provinceName = a.provinceName)
           and a.country = '中国'
         group by a.provinceName, a.confirmedCount
         order by a.confirmedCount desc) aa



# 概览
select (aa.confirmedCount) as '确诊总数',
       (aa.deadCount)      as '死亡数',
       (aa.curedCount)     as '治愈',
       aa.utime,
       aa.udate
#        sum(aa.suspectedCount) as '疑似'
from (
         select a.id,
                a._id,
                a.confirmedCount,
       from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') as utime,
       from_unixtime(left(a.updateTime, 10), '%Y-%m-%d') as udate,
                a.deadCount,
                a.curedCount,
                a.suspectedCount,
                 a.provinceName
         from dxyarea a
         where from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') >=
               str_to_date('2020-01-29  00:00:00', '%Y-%m-%d %H:%i:%s')
           and from_unixtime(left(a.updateTime, 10), '%Y-%m-%d %H:%i:%s') <=
               str_to_date('2020-01-30  23:59:00', '%Y-%m-%d %H:%i:%s')
           and a.updateTime = (SELECT MAX(updateTime + 0)
                               FROM dxyarea
                               WHERE provinceName = a.provinceName)
           and a.country = '中国'
         group by a.provinceName, a.confirmedCount
         order by a.confirmedCount desc) aa