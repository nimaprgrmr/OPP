# create worker class 
class Worker():
  def __init__(self, name, skills: dict, quality=dict, first=None, last=None, status='unemployed', tasks=[]):
    self.name = name
    self.first = first
    self.last = last
    self.status = status
    self.quality = quality  # this shows how much worker makes good cloths, for example if makes 100 products how % of them has good quality, if 20 numbers of them be bad, the quality of worker changes to 0.8 and the skill of worker changes to worker_skill * 0.8(that is the accuracy of worker.)
    self.skills = skills
    self.tasks = tasks

  def update(self):
    for skill, value in self.skills.items():
      for skill2, value2 in self.quality.items():
        if skill == skill2:
          self.skills[skill] = value * value2

  def describe_worker(self):
    return f"This worker name is: {self.name} | his skill is: {self.skills.keys()} his scores is: {self.skills.values()} | his qualities: {self.quality} |his tasks are: {self.tasks}"


# create machine class
class Machine():
  def __init__(self, name: str, numbers: int):
    self.name = name
    self.numbers = numbers

  def describe_machine(self):
    return f"{self.name} machine available for {self.numbers} numbers"


# create task class
class Task():
  def __init__(self, name, take_time: int, pre_required=0, status='not_started', priority=1, machines=[]):
    self.name = name
    self.take_time = int(take_time)
    self.pre_required = pre_required
    self.status = status
    self.priority = priority # this should initialize with values between 1 or greater than one, if assign with 1 it means that, it is the most important and whatever this number be greater it means that the necesity of this task is lower.
    self.machines = machines 
  def describe_task(self):
    if self.priority == 1:
      return f"this task is: {self.name} | the time required to do for once is: {self.take_time} seconds | its pre required: {self.pre_required} | its priority is first | its status is: {self.status}"
    else:
      return f"this task is: {self.name} | the time required to do for once is: {self.take_time} seconds | its pre required: {self.pre_required} | its priority is {self.priority} | its status is: {self.status}"


# create station class
class Station():
  def __init__(self, name, workers=set(), tasks=set()):
    self.name = name
    self.workers = workers
    self.tasks = tasks

  def describe_station(self):
    return f"station name isL {self.name} | workers are: {self.workers} | tasks are: {self.tasks}"
  

# create product class
class Product():
  def __init__(self, title, tasks):
    self.title = title
    self.tasks = tasks
    self.time = sum([task.take_time for task in tasks])

  def describe_product(self):
    return f"this product is: {self.title} | and tasks need for producting this item are {[task.title for task in self.tasks]}"

