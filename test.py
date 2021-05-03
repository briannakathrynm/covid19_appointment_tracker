import os
from datetime import datetime

# Directory
# Getting current date and time...
import pandas as pd

now = datetime.now()
dt_string = now.strftime("%d%m%Y_%H%M")
directory = "clinic" + str(dt_string)

# Parent Directory path
parent_dir = "C:/Users/Brianna/Dropbox/Spring Semester 2021/ELE 408/Project/"

# Path
path = os.path.join(parent_dir, directory)

os.mkdir(path)
print(path)

test_df = pd.DataFrame([1, 2, 3, 4, 5])
test_df.to_csv(path + "/" + "_" + str("hello") + '.csv', index=False)
