from modules import Machine, Task, Worker, Product, Station
from utilities import * 

# define tasks 
task1 = Task(name='cutting_cloth',    take_time=160,  pre_required=[None],    priority=5, machines=[])
task2 = Task(name='sewing_sleeves',   take_time=90,   pre_required=[task1],   priority=2, machines=[])
task3 = Task(name='sewing_colar',     take_time=90,   pre_required=[task1],   priority=2, machines=[])
task4 = Task(name='sewing_body',      take_time=60,   pre_required=[task1],   priority=2, machines=[])
task5 = Task(name='connecting_parts', take_time=120,  pre_required=[task2, task3, task4], priority=1, machines=[])
task6 = Task(name='printing_logo',    take_time=120,  pre_required=[task5],   priority=3, machines=[])
task7 = Task(name='checking_quality', take_time=40,   pre_required=[task6],   priority=4, machines=[])


### define wokers 
worker1 = Worker(name='ali abdi', skills={'cutting_cloth': 1., 'checking_quality': 0.5},
                 quality={'cutting_cloth': .8, 'checking_quality': 1.} , status='unemployed', tasks=[])

worker2 = Worker(name='mohamad molaei',skills={'sewing_sleeves': 0.9, 'sewing_colar': 0.7},
                 quality={'sewing_sleeves': 0.9, 'sewing_colar': 1.0} , status='unemployed', tasks=[])

worker3 = Worker(name='iman najafi', skills={'sewing_colar':1.}, quality={'sewing_colar': 1.}, status='unemployed', tasks=[])

worker4 = Worker(name='mina azizi', skills={'sewing_body': 1., 'connecting_parts': 0.6},
                quality={'sewing_body': 1., 'connecting_parts': 1.} , status='unemployed', tasks=[])

worker5 = Worker(name='azita hajian', skills={'connecting_parts':.9, 'sewing_body': 0.6, 'cutting_cloth': 1.0},
                 quality={'connecting_parts':1., 'sewing_body': 0.9, 'cutting_cloth': 1.0}, status='unemployed', tasks=[])

worker6 = Worker(name='abas aghayi', skills={'printing_logo': 0.9},
                 quality={'printing_logo': 0.8}, status='unemployed', tasks=[])

worker7 = Worker(name='rasool khadem', skills={'printing_logo': 1.},
                 quality={'printing_logo': 0.9}, status='unemployed', tasks=[])

worker8 = Worker(name='hamed ghorbani', skills={'checking_quality': 1.},
                 quality={'checking_quality': 8.}, status='unemployed', tasks=[])

worker9 = Worker(name='setare derakhshan', skills={'cutting_cloth': 0.8},
                 quality={'cutting_cloth': 1.0}, status='unemployed', tasks=[])

worker10 = Worker(name='hamid bagheri', skills={'connecting_parts': 0.7, 'cutting_cloth': 0.5},
                  quality={'connecting_parts': 0.9, 'cutting_cloth': 1.0}, status='unemployed', tasks=[])

worker11 = Worker(name='mahdi behboodi', skills={'connecting_parts':1.0, 'cutting_cloth': 0.5, 'sewing_body': 0.7},
                  quality={'connecting_parts':1.0, 'cutting_cloth': 1., 'sewing_body': 1.}, status='unemployed', tasks=[])

worker12 = Worker(name='amin ojaghi', skills={'connecting_parts': 0.6, 'printing_logo': 0.6},
                  quality = {'connecting_parts': 0.9, 'printing_logo': 0.7}, status='unemployed', tasks=[])

worker13 = Worker(name='rasool babayi', skills={'cutting_cloth': 0.6, 'printing_logo': 0.3},
                  quality={'cutting_cloth': 1., 'printing_logo': 0.9}, status='unemployed', tasks=[])

worker14 = Worker(name='negar ahmadi', skills={'connecting_parts': 0.8, 'checking_quality': 0.9},
                  quality={'connecting_parts': 1., 'checking_quality': 1.}, status='unemployed', tasks=[])

worker15 = Worker(name='mohamadreza ahmadi', skills={'sewing_colar': 0.3, 'sewing_body': 0.9},
                  quality={'sewing_colar': 1.0, 'sewing_body': 1.0}, status='unemployed', tasks=[])

# define workers and thn update their skills based on their qualities.
workers = [worker1, worker2, worker3, worker4, worker5, worker6, worker7, worker8, worker9, worker10, worker11, worker12, worker13, worker14, worker15]
workers = [worker.update() for worker in workers]
workers = [worker1, worker2, worker3, worker4, worker5, worker6, worker7, worker8, worker9, worker10, worker11, worker12, worker13, worker14, worker15]

# define machines
machine1 = Machine(name = 'cutting', numbers=5)
machine2 = Machine(name = 'sewing', numbers=10)
machine3 = Machine(name = 'connecting', numbers=3)
machine4 = Machine(name = 'printing', numbers=3)
machine5 = Machine(name = 'checking', numbers=2)

# define product contains all tasks that should this product made by them 
product = Product('t-shert', tasks=[task5, task2, task7, task4, task1, task3, task6])

# find how many stations we have based on dependency on each other tasks 
def make_stations(product):
    tasks = product.tasks
    s = 0
    before_req = [0]
    for task in tasks:
        req = task.pre_required
        if req not in before_req:
            before_req.append(req) 
            s += 1
    stations = []
    for i in range(s):
        station = Station(name='station'+f'{i+1}', tasks=set(), workers=set())
        stations.append(station)
    return stations 

# define stations contain all stations 
stations = make_stations(product=product)

# assign each task to a station based on their dependecy to each station 
def find_tasks(product, stations):
    tasks = product.tasks
    # assign tasks to stations

    for task in tasks:
        for task in tasks:
            pre_required_tasks = [task, [task.name for task in task.pre_required if task is not None]]

            if len(pre_required_tasks[1]) == 0:
                stations[0].tasks.add(task)

            if len(pre_required_tasks[1]) > 0:
                new_task = pre_required_tasks[0]
                for pre_req in pre_required_tasks[1]:
                    for i, station in enumerate(stations):
                        station_tasks = station.tasks
                        for t in station_tasks:
                            if pre_req == t.name:
                                stations[i+1].tasks.add(new_task)
                                
# call fundtion that make tasks sit in each station
find_tasks(product=product, stations=stations)

# make main function that assign different workers to different stations  
def make_plan(product:Product, workers: list, stations: list):
  # get all tasks required for this product
  tasks = product.tasks

  # sort tasks based on their priority
  tasks.sort(reverse=False, key=lambda x: x.priority)

  # get priorities for tasks
  priorities = [task.priority for task in tasks]

  # get first tasks with min priority. it can be more than one task
  first_tasks = [task for task in tasks if task.priority == min(priorities)]

  # get last tasks priority it can be more than one task
  last_tasks = [task for task in tasks if task.priority == max(priorities)]

  # get all tasks between first and last task
  other_tasks = [task for task in tasks if min(priorities) < task.priority < max(priorities)]

  # assign what workers and do first, last and other tasks
  workers_for_first_tasks = []
  workers_for_last_tasks = []
  workers_for_other_tasks = []

  # get what workers can do first, other and last tasks and add them to above lists
  for worker in workers:

    worker_skills = worker.skills

    for s, val in worker_skills.items():

      for task in first_tasks:

        if s == task.name:

          workers_for_first_tasks.append({'worker': worker, 'name': worker.name, 'skill': s, 'score': val})

      for task in last_tasks:

        if s == task.name:

          workers_for_last_tasks.append({'worker': worker, 'name': worker.name, 'skill': s, 'score': val})

      for task in other_tasks:

        if s == task.name:
          
          workers_for_other_tasks.append({'worker': worker, 'name': worker.name, 'skill': s, 'score': val})

  # sort workers based on their skills
  workers_for_first_tasks.sort(key=get_score, reverse=True)
  workers_for_last_tasks.sort(key=get_score, reverse=True)
  workers_for_other_tasks.sort(key=get_score, reverse=True)

  # assign works for first tasks in first station and workers that have best score in each task
  assign_workers(tasks_list=first_tasks, workers_list=workers_for_first_tasks, stations=stations)

  # assign works for tasks between first and last task and station and workers
  assign_workers(tasks_list=other_tasks, workers_list=workers_for_other_tasks, stations=stations)

  # assign works for last tasks and last station and workers that have best score in each task
  assign_workers(tasks_list=last_tasks, workers_list=workers_for_last_tasks, stations=stations)

  # assign works to workers that has not employed yet to the tasks that need more time and workers skill
  assign_work_other_workers(workers, stations)

# call make_plan to assign workers to stations 
make_plan(product, workers, stations)

# make another assign task to workers that has free time between their tasks, workers could get more than one tasks
def assign_second_work(workers, tasks: product.tasks):
  for worker in workers:
    now_task = [task for task in worker.tasks]
    now_task_time = sum([task.take_time for task in worker.tasks])
    pre_required_task = now_task[0].pre_required
    if pre_required_task[0] is not None:
      time_pre_required_task = max([task.take_time for task in pre_required_task])
    else:
      time_pre_required_task = 0
    another_skills_worker = [(skill, find_task(skill, tasks).take_time) for skill in worker.skills if skill != now_task[0].name]
    quality_skills_worker = worker.quality
    free_time =  time_pre_required_task - now_task_time
    if free_time > 0:
    #   print(f"worker_name: {worker.name}   |   time: {now_task_time}   |   time_pre_required: {time_pre_required_task}   |   another_skills: {another_skills_worker}   |   skills_quality: {quality_skills_worker}   |   free time: {free_time}")
      if len(another_skills_worker) >= 1:
        if free_time > another_skills_worker[0][1]:
          worker.tasks.append(find_task(another_skills_worker[0][0], tasks))

# define all tasks required for product and pass it to assign_second_work function.
tasks = product.tasks 
assign_second_work(workers, tasks)
# see the result.
# for worker in workers:
#   print(worker.name, worker.tasks)

for station in stations:
  for worker in station.workers:
    print(f"station: {station.name} | worker: {worker[0].name} | tasks: {[task.name for task in worker[0].tasks]}")
