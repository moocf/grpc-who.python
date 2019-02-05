from optparse import (OptionParser,BadOptionError,AmbiguousOptionError)
import grpc
import who_pb2
import who_pb2_grpc
import sys


class PassThroughOptionParser(OptionParser):
  def _process_args(self, largs, rargs, values):
    while rargs:
      try:
        OptionParser._process_args(self,largs,rargs,values)
      except (BadOptionError,AmbiguousOptionError) as e:
        largs.append(e.opt_str)


parser = PassThroughOptionParser()
parser.set_defaults(server="localhost:50051")
parser.add_option("--server", dest="server", help="set server address")
parser.usage = "python rhwo.py <arguments> [--server <address>]"
(options, args) = parser.parse_args()

address = options.server
with grpc.insecure_channel(address) as channel:
  stub = who_pb2_grpc.WhoStub(channel)
  response = stub.Call(who_pb2.CallRequest(args='|'.join(args)))
  print(response.out)
