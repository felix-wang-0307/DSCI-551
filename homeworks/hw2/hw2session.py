from filesystem import Session

class HW2Session(Session):
  def __init__(self, fs):
    super().__init__(fs)

  # helper functions
  def _check_logged_in(self):
    """Check if user is logged in"""
    if self.curr_dir is None:
      print('No user logged in!')
      return False
    return True
  
  def _find_child_node(self, name):
    """Find a child node by name in current directory"""
    if self.curr_dir is None:
      return None
    for child in self.curr_dir.children:
      if child.name == name:
        return child
    return None
  
  def _remove_node_from_parent(self, node):
    """Remove a node from its parent's children list"""
    if node.parent:
      node.parent.children.remove(node)
    return node
  
  def _get_absolute_path(self, node):
    """Get the absolute path of a node"""
    if node.parent is None:  # root node
      return '/'
    elif node.parent.parent is None:  # direct child of root
      return '/' + node.name
    else:
      return self._get_absolute_path(node.parent) + '/' + node.name

  # This removes the directory dir_name from the current working directory
  # It should report errors when
  #   * dir_name does not exist
  #   * dir_name is not empty
  #   * dir_name is not a directory
  def rmdir(self, dir_name):
    # Check if user is logged in
    if not self._check_logged_in():
      return None
      
    # Find the target directory
    target_node = self._find_child_node(dir_name)
    if target_node is None:
      print(f'{dir_name} does not exist!')
      return None
    
    # Check if it's a directory
    if target_node.node_type != 'directory':
      print(f'{dir_name} is not a directory!')
      return None
    
    # Check if directory is empty
    if target_node.children:
      print(f'{dir_name} is not empty!')
      return None
    
    # Remove the directory
    return self._remove_node_from_parent(target_node)

  # this removes a file "file_name" from the current working directory
  # it should report errors when:
  #   * file_name does not exist
  #   * file_name is a directory
  def rm(self, file_name):
    # Check if user is logged in
    if not self._check_logged_in():
      return None
      
    # Find the target file
    target_node = self._find_child_node(file_name)
    if target_node is None:
      print(f'{file_name} does not exist!')
      return None
    
    # Check if it's a file (not a directory)
    if target_node.node_type != 'file':
      print(f'{file_name} is a directory!')
      return None
    
    # Remove the file
    return self._remove_node_from_parent(target_node)

  # This emulates the hdfs oiv (offline image viewer) command to print the
  # entire namespace of file system. In other words, it lists all file system
  # objects (file or directory), one line at a time. For each object,
  # it shows the path to the object and the type of object, seperated by comma.
  # For example,
  #           /,directory
  #           /home,directory
  #           /home/john,directory
  #           /home/john/hw1.py,file
  #           ...
  #
  def dump_fsimage(self):
    def dfs(node):
      """Recursively traverse the tree and print each node"""
      path = self._get_absolute_path(node)
      print(f'{path},{node.node_type}')
      
      # Recursively process children
      for child in node.children:
        dfs(child)
    
    # Start traversal from root
    if self.root is not None:
      dfs(self.root)