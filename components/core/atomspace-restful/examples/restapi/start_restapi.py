#! /usr/bin/env python3
#
# Start the restful server.

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.utilities import initialize_opencog
from opencog.web.api.apimain import RESTAPI


# Endpoint configuration
# To allow public access, set to 0.0.0.0; for local access, set to 127.0.0.1
IP_ADDRESS = "0.0.0.0"
PORT = 5000

atomspace = AtomSpace()
initialize_opencog(atomspace)

Link(ConceptNode("Test Concept"), ConceptNode("another one"))

api = RESTAPI(atomspace)
api.run(host=IP_ADDRESS, port=PORT)
