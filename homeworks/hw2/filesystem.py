# Every file or directory is stored in a Node object.
# Every node except for root has exactly one parent.
# Every node except for leaf nodes (e.g., files)
#   may have a number of child nodes.
class Node:
  def __init__(self, name, node_type, parent=None):
    self.name = name
    self.node_type = node_type # node_type is either 'file' or 'directory'
    self.parent = parent
    self.children = []

    if (self.parent): # not the root node
      # no two files/directories can have the same name
      if any(c.name == name for c in self.parent.children):
        raise ValueError(f"Child '{name}' already exists under {self.parent.name}")

      # the parent now has one more child
      self.parent.children.append(self)

  # string representation of node, describing the node.
  def __repr__(self) -> str:
    out = f'name: {self.name}, type: {self.node_type}'

    if (self.parent):
      out += f', parent: {self.parent.name}'

    if (self.children):
      cnames = [c.name for c in self.children]
      out += f', children: {cnames}'

    return out

class FileSystem:
  def __init__(self):
    self.root = None # root of file system
    self.home = None # home is parent node of all user homes
    # e.g., /home/john and /home/david where john and david are two users

  # create the initial directory tree
  def format(self):
    self.root = Node('root', "directory")
    self.home = Node('home', "directory", parent = self.root)
    return self.root

  def add_user(self, user_name):
    return Node(user_name, 'directory', parent = self.home)

  # remove user node and all its descendant nodes
  # not implemented for this homework!!!
  def drop_user(self, user_name):
    return None

# This emulates the interaction with file system and OS
# when a user logins to system
class Session:
  def __init__(self, fs): # fs is file system instance
    self.fs = fs
    self.curr_dir = None # this keep tracks of where the user is
    #      currently located, i.e., the current working directory
    self.home = None # this points to user home, e.g., /home/john
    self.user_name = None
    self.root = fs.root

  def login(self, user_name):
    for c in self.fs.home.children:
      if (c.name == user_name): # find the name by user_name
        self.curr_dir = c
        self.home = c
        self.user_name = user_name
        return c
    raise ValueError(f'user {user_name} does not exists!')

  def cd(self, dir_name=None):
    if (dir_name is None): # "cd" will bring us back to home
      self.curr_dir = self.home
      return self.curr_dir
    elif dir_name == '/': # "cd /" will take us to root
      self.curr_dir = self.root
      return self.curr_dir
    elif (dir_name == '..'): # "cd .." is to go one level up
      if self.curr_dir.name != 'root': # if already reaching root, stay put
        self.curr_dir = self.curr_dir.parent
      return self.curr_dir
    elif not any(dir_name == c.name for c in self.curr_dir.children):
      # make sure in "cd xyz", "xyz" exists
      print(f'{dir_name} does not exist!')
      return None
    else:
      node = next(c for c in self.curr_dir.children if c.name == dir_name)

      # make sure dir_name indeeds is a directory
      if (node.node_type != 'directory'):
        print(f'{dir_name} is not a directory!')
        return None
      else:
        self.curr_dir = node

        return node

  # create a directory under the current working dir
  def mkdir(self, dir_name):
    # make sure dir_name does not exist yet in the current dir
    if any(dir_name == c.name for c in self.curr_dir.children):
      print(f'{dir_name} already exist!')
    else:
      return Node(dir_name, node_type='directory', parent=self.curr_dir)

  # print the absolute path to the current working directory, e.g.,
  # /home/john/hw1
  def pwd(self):
    # return a list of names of nodes from root down to the current dir
    # root is represented as '/'
    def find_path(node):
      if node.parent is None:
        return []
      else: 
        return find_path(node.parent) + [node.name]
     
    return '/' + '/'.join(find_path(self.curr_dir))

  # this emulated the "ls" command
  def ls(self):
    if self.curr_dir.children: # the current dir has some children
      res = [f'{c.name}({c.node_type})' for c in self.curr_dir.children]
      return ' '.join(res)
    else:
      return None

  # this creates an empty file, emulating the "touch" command in Unix-like OS
  def touch(self, file_name):
    if any(file_name == c.name for c in self.curr_dir.children):
      print(f'{file_name} already exist!')
    else:
      return Node(file_name, node_type='file', parent=self.curr_dir)