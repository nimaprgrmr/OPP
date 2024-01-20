# this function sorts workers based on their skills
def get_score(listt):
  return listt.get('score')


# take an item and returns the index of station
def get_station(item, stations):
  task = item.get('skill')
  for i, station in enumerate(stations):
    for t in station.tasks:
      if t.name == task:
        return i


# assign tasks to workers based on tasks and workers pass
def assign_workers(tasks_list, workers_list, stations):
  # assign works for first tasks in first station and workers that have best score in each task
  for task in tasks_list:
    best_score = 0
    for item in workers_list:
      if item.get('worker').status == 'unemployed':
        if item.get('skill') == task.name:
          if item.get('score') > best_score:
            index = get_station(item, stations)
            # add worker to related station
            stations[index].workers.add((item.get('worker'), item.get('name'), item.get('skill'), item.get('score')))
            #change the status of worker
            worker = item.get('worker')
            worker.status = 'employed'
            # task.status= 'started'
            best_score = item.get('score')
            # add task to worker
            worker = item.get('worker')
            worker.tasks.append(task)


# take a name of task and return that task
def find_task(title: str, tasks):
  selected_task = ''
  for task in tasks:
    if task.name == title:
      selected_task = task
  return selected_task


# for sorting based on time feature
def get_time(listt):
  return listt.get('time')


def get_necessity(listt):
  return listt.get('necessity')


# calculate how many depemdencies there are in each station
def make_list_stations(stations):
  list_stations = []
  for i in range(len(stations)):
    task_times = 0
    number_of_task_dependency = []
    for task in stations[i].tasks:
      task_times += task.take_time
      if task.pre_required is not None:
        number_of_task_dependency.append(task.pre_required)
    information = {'station_number': i, 'station_time': task_times, 'number_of_dependency_tasks': len(number_of_task_dependency), 'workers': [worker[1] for worker in stations[i].workers]}
    list_stations.append(information)
  return list_stations


# find how much nessecity each station based on make_list_stations
def make_nessecity_stations(list_stations):
  nessecity_stations = []
  for i, item in enumerate(list_stations):
    if i+1 < len(list_stations):
      nessecity_station = (((list_stations[i]).get('station_time')) * list_stations[i+1].get('number_of_dependency_tasks')) / len(list_stations[i].get('workers'))
      nessecity_stations.append({'index_station': i, 'necessity': nessecity_station})
    else:
      nessecity_station = (list_stations[i]).get('station_time')
      nessecity_stations.append({'index_station': i, 'necessity': nessecity_station})
  # sort workers based on their skills
  nessecity_stations.sort(key=get_necessity, reverse=True)
  return nessecity_stations


def assign_work_other_workers(workers, stations):
  for worker in workers:
    if(worker.status) == 'unemployed':
      # calculate how many depemdencies there are in each station
      list_stations = make_list_stations(stations)
      # nessecity_stations is the sorted stations with their necessity number
      nessecity_stations = make_nessecity_stations(list_stations)
      # get worker skills
      worker_skills = worker.skills
      for item in nessecity_stations:
        if(worker.status) == 'unemployed':
          # get first most important(station that have most trafic) station
          station = item.get("index_station")
          tasks_in_most_important_station = stations[station].tasks
          list_most_important_station = [{'task':task, 'time': task.take_time} for task in tasks_in_most_important_station]
          list_most_important_station.sort(key=get_time, reverse=True)
          tasks_in_most_important_station = set()
          for item in list_most_important_station:
            tasks_in_most_important_station.add(item.get('task'))

          for task in tasks_in_most_important_station:
            for skill in worker_skills.items():
              if skill[0] == task.name:
                if worker.status == 'unemployed':
                  # add worker to most required station
                  stations[station].workers.add((worker, worker.name, skill[0], skill[1]))
                  # change the worker status
                  worker.status='employed'
                  # add task to worker
                  worker.tasks.append(task)

        # update numbers for necessity and important stations after assign worker to station that have most trafic in there and repeat this loop again.
        list_stations = make_list_stations(stations)
        nessecity_stations = make_nessecity_stations(list_stations)