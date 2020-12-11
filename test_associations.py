import os
from uuid import uuid4
import time
import sys

from util.pydent_helper import create_session

session = create_session("laptop")

plan = session.Plan.new(name="Associations Test")
plan.create()
plan.associate("foo", "bar")
plan.associate_file_from_path("specimens_from_file", "test", "20201210-100429.txt")

# op_type = session.OperationType.find_by_name("Pool Samples")
# op = op_type.instance()
# print(op.id)

# plan.add_operation(op)
# plan.save()
# print(op.id)

# # op.refresh()
# # print(op.id)

# op = plan.operations[0]
# print(op.id)

# plan.associate("foo", "bar")
# print(op.get("foo"))

# op.associate_file_from_path("specimens_from_file", "test", "20201210-100429.txt")


# user = session.User.find_by_name("Joe Neptune")
# budget = session.Budget.find_by_name("My First Budget")
# plan.submit(user, budget)


# op = session.Operation.find(op.id)

# print(op.associations)

# op = session.Operation.one()
# # create a test file
# filepath = os.path.join('.', "test_upload.txt")
# val = str(uuid4())
# print(val)
# sys.exit()
# with open(filepath, "w") as f:
#     f.write(val)
# # upload the test file
# with open(filepath, 'r') as f:
#     u = session.Upload.new(job_id=None, file=f)
#     _da = op.associate('test_upload', 'val', upload=u, save=True)
# # give the server a little bit of time
# time.sleep(0.1)
# # retrieve the file from the server
# data_association = session.DataAssociation.find(_da.id)
# download_path = data_association.upload.download('.')
# # verify the contents of the download
# with open(download_path, 'r') as f:
#     assert f.read() == val

