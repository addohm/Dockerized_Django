import shutil
import os
import sys

'''
Place this script in the main project directory.  This should be
the same directory as manage.py.  
'''
# Get the file path of this script
root = sys.path[0]

for item in os.listdir(root):
# Delete the sqlite3 database
  if item == 'db.sqlite3': 
    if os.path.exists(f'{root}/{item}'):
      os.remove(f'{root}/{item}')
    print(f"- {root}/{item}.")

# Delete USER UPLOADED MEDIA folder
  if os.path.isdir(f'{root}/{item}'):
    print(f'> {root}/{item}')
    if item == 'media':
      for subitem in item:
        if os.path.isdir(f'{root}/{item}/{subitem}'):
          shutil.rmtree(f'{root}/{item}/{subitem}')
          print(f"- {root}/{item}/{subitem}")
        if os.path.exists(f'{root}/{item}/{subitem}'):
          os.remove(f'{root}/{item}/{subitem}')
          print(f"- '{root}/{item}/{subitem}'")
    if item == 'staticfiles':
      for subitem in item:
        if os.path.isdir(f'{root}/{item}/{subitem}'):
          shutil.rmtree(f'{root}/{item}/{subitem}')
          print(f"- {root}/{item}/{subitem}")
        if os.path.exists(f'{root}/{item}/{subitem}'):
          os.remove(f'{root}/{item}/{subitem}')
          print(f"- '{root}/{item}/{subitem}'")
    if item == 'fileshare':
      for subitem in item:
        if os.path.isdir(f'{root}/{item}/{subitem}'):
          shutil.rmtree(f'{root}/{item}/{subitem}')
          print(f"- {root}/{item}/{subitem}")
        if os.path.exists(f'{root}/{item}/{subitem}'):
          os.remove(f'{root}/{item}/{subitem}')
          print(f"- '{root}/{item}/{subitem}'")


    if os.path.exists(f'{root}/{item}'):
      for subitem in os.listdir(f'{root}/{item}'):
        print(f'>> {root}/{item}')

        # Clear out the APP MIGRATIONS files
        if subitem == 'migrations':
          print(f'>>> {root}/{item}/{subitem}')
          for files in os.listdir(f'{root}/{item}/{subitem}'):
            if files != '__init__.py' and os.path.isfile(f'{root}/{item}/{subitem}/{files}'):
              if os.path.exists(f'{root}/{item}/{subitem}/{files}'):
                os.remove(f'{root}/{item}/{subitem}/{files}')
                print(f"- '{root}/{item}/{subitem}/{files}'")

        # Clear out the PYCACHE files
        if subitem == '__pycache__':
          print(f'>>> {root}/{item}/{subitem}')
          for files in os.listdir(f'{root}/{item}/{subitem}'):
            if files != '__init__.py' and os.path.isfile(f'{root}/{item}/{subitem}/{files}'):
              if os.path.isfile(f'{root}/{item}/{subitem}/{files}'):
                os.remove(f'{root}/{item}/{subitem}/{files}')
                print(f"- '{root}/{item}/{subitem}/{files}'")
      
