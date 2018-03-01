# tryplacement

This project is just usded to try Openstack Placement.

Most of code are hardcode.

With this code, you can under statck Openstack Placement easily.

We can parser argument and tap complement to make it as cli.
And make good organization for the code architecture.

But this beyond the goal of the original intention.
Just learn Placement and know how to use it as as quickly as possible.

Assume that you have install placement and keystone.

Just run:
$ ./cmd.py

You can edit any of the flow in the ./cmd.py as you want.

or your run the command to test Placement interactive:
$ ipython -i bootstrap.py


upload an image, use the follow commad. Then it can generate a placement.
$ openstack image create --file token.json  test.token
$ openstack image list
$ openstack image show 58b813db-1fb7-43ec-b85c-3b771c685d22
$ openstack image set --tag INTEL --tag FPGA --property vendor=intel type=crypto  58b813db-1fb7-43ec-b85c-3b771c685d22
all in one
$ openstack image create --file cirros.qcow2 --property vendor=intel --property type=crypto --tag INTEL --tag FPGA fpga-cirros
