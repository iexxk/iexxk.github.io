---
title: Spring-Schedule
date: 2019-06-16 13:26:33
updated: 2019-06-16 13:33:04
categories: Spring
tags: [Schedule]
---

```java
@Component
public class TestSchedule {
    @ScheduleAnnotaion(serviceId = "DataSync", scheduleDesc = "数据同步", checkIntervalTime = 30, isSignalExecuteFlag = true, addHisTaskTableFlag = false)
    @Scheduled(cron = "0 * * * * ?") // 每1分钟执行一次

    public void executeSchedule() throws ResponseException {
        executeScheduleNow();
    }

    public void executeScheduleNow() {
        //todo 需要添加的操作
    }
}
```

