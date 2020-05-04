import requests
import threading
import calendar
import heapq
from datetime import datetime, date, timedelta


class TimerReminder:
    def __init__(self):
        self.queue = []
        self.current = None
        self.timer = None

    def __set_timer(self):
        if self.timer:
            self.timer.cancel()
        t_sec = (self.current[0] - datetime.now()).total_seconds()
        self.timer = threading.Timer(t_sec, self.__remind)
        self.timer.start()

    def convert_to_datetime(self, params, diff=False):
        now = datetime.now()
        if diff:
            time_delta = timedelta(days=params['days'],
                                   hours=params['hours'],
                                   minutes=params['minutes'],
                                   seconds=params['seconds'])
            res = now + time_delta
        else:
            dt_now = {'year': now.year, 'month': now.month, 'day': now.day,
                      'hour': now.hour, 'minute': now.minute, 'second': 0}
            dt = dt_now
            for key in params.keys():
                if key == 'year' and dt['year'] > params['year']:
                    continue
                elif key == 'month' and dt['month'] > params['month']:
                    dt['year'] += 1
                    dt['month'] = params['month']
                elif key == 'hour' and dt['hour'] > params['hour']:
                    dt['day'] += 1
                    if dt['day'] > calendar.monthrange(dt['year'], dt['month'])[1]:
                        dt['day'] = 1
                        dt['month'] += 1
                        if dt['month'] > 12:
                            dt['month'] = 1
                            dt['year'] += 1
                else:
                    dt[key] = params[key]
            res = datetime(dt['year'], dt['month'], dt['day'], dt['hour'], dt['minute'], dt['second'])
        return res

    def add_reminder(self, t, address, message="It's time!"):
        item = (t, address, message)
        if self.current is None:
            self.current = item
        elif self.current[0] < item[0]:
            heapq.heappush(self.queue, item)
        else:
            heapq.heappush(self.queue, self.current)
            self.current = item
        self.__set_timer()

    def __remind(self):
        r = requests.post(url=self.current[1], json={"text": self.current[2]})
        self.current = None
        if self.queue:
            self.current = heapq.heappop(self.queue)
            self.__set_timer()


if __name__ == '__main__':
    params = {'month': 5, 'day': 30, 'hour': 19, 'minute': 30, 'second': 10}

    # tr = TimerReminder()
    # t = 20
    # tdelta = timedelta(seconds=t)
    # time = datetime.now() + tdelta
    # item = (time, "https:/127.0.0.1")
    # tr.add_reminder(item)
    # t = datetime.now()
    # item = (t, "https:/127.0.0.2")
    # tr.add_reminder(item)
    # tdelta = timedelta(seconds=10)
    # t = datetime.now() + tdelta
    # item = (t, "https:/127.0.0.3")
    # tr.add_reminder(item)
    print(datetime.now())
