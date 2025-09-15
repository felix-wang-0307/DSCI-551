import requests
import json

############ add codes here, if needed

class TodoClient:
  # this method simply remembers the given dburl
  def __init__(self, dburl):
    # fill in code
    self.dburl = dburl.rstrip('/')  # remove trailing '/' if any
    self.todo_data = {}  # local cache of the todo list

    try:
      self.connection = requests.get(self.dburl + '/.json')
      if self.connection.status_code == 200:
        response_data = self.connection.json()
        if response_data is None:
          self.todo_data = {}
        else:
          self.todo_data = response_data
      else:
        self.todo_data = {}
    except:
      self.todo_data = {}

  # Remove all existing tasks from the todo list.
  # If the removal was successful, return "Success!".
  # otherwise, return the error message from the Firebase server.
  # The error message should be in a Python dictionary, e.g., 
  #        {'error': '404 Not Found'}
  # clear() method should be called first before any tasks are added to the 
  #    todo list.
  # You should assume that no other methods will be called on the todo list,
  # if the clear method failed.
  def clear(self):
    # fill in code
    try:
      response = requests.delete(self.dburl + '/.json')
      if response.status_code == 200:
        self.todo_data = {}
        return "Success!"
      else:
        return {'error': f'{response.status_code} {response.reason}'}
    except:
      return {'error': '404 Not Found'}


  # if the task exists in the todo list,, 
  #    return an error message in this format:
  #       Error in add_task: task "xyz" already exists!
  #         where xyz should be replaced with the actual task name
  # else, 
  #    add the task to the todo list stored in Firebase, and
  #    return "Success!"
  def add_task(self, task):
    # fill in code
    # First, sync with Firebase to get latest data
    self._sync_with_firebase()
    
    if task in self.todo_data:
      return f'Error in add_task: task "{task}" already exists!'
    else:
      self.todo_data[task] = 'pending'
      return self._update_firebase()

  # if the task does not exist in the list, 
  #    return an error message in this format:
  #        Error in delete_task: task "xyz" does not exist!
  #         where xyz should be replaced with the actual task name
  # else, 
  #    remove the task from the list, and 
  #    return "Success!"
  def delete_task(self, task):
    # fill in code
    # First, sync with Firebase to get latest data
    self._sync_with_firebase()
    
    if task not in self.todo_data:
      return f'Error in delete_task: task "{task}" does not exist!'
    else:
      del self.todo_data[task]
      return self._update_firebase()


  # if the task does not exist in the list, 
  #    return an error message in this format:
  #        Error in mark_completed: task "xyz" does not exist!
  #         where xyz should be replaced with the actual task name
  # else, 
  #    change the status of the task to "completed", and 
  #    return "Success!"
  def mark_completed(self, task):
    # fill in code
    # First, sync with Firebase to get latest data
    self._sync_with_firebase()
    
    if task not in self.todo_data:
      return f'Error in mark_completed: task "{task}" does not exist!'
    else:
      self.todo_data[task] = 'completed'
      return self._update_firebase()
    
 

  # return a list of tasks in the given status, 
  # and empty list if no such tasks
  def get_task_by_status(self, status):  # status is either completed or pending
    # fill in code
    # First, sync with Firebase to get latest data
    self._sync_with_firebase()
    
    result = []
    for task, task_status in self.todo_data.items():
      if task_status == status:
        result.append(task)
    return result
    
  # return a dictionary of task:status pairs, 
  # and None if no tasks in the todo list.
  def get_all_tasks(self):
    # fill in code
    # First, sync with Firebase to get latest data
    self._sync_with_firebase()
    
    if not self.todo_data:
      return None
    return self.todo_data

  ############ add codes here if needed
  
  def _sync_with_firebase(self):
    """Private method to sync local cache with Firebase data"""
    try:
      response = requests.get(self.dburl + '/.json')
      if response.status_code == 200:
        response_data = response.json()
        if response_data is None:
          self.todo_data = {}
        else:
          self.todo_data = response_data
        return True
    except:
      pass
    return False
  
  def _update_firebase(self):
    """Private method to update Firebase with local cache data"""
    try:
      response = requests.put(self.dburl + '/.json', json=self.todo_data)
      if response.status_code == 200:
        return "Success!"
      else:
        return response.json()
    except Exception as e:
      return {"error": str(e)}