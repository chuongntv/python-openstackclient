#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid

from functional.common import test


class NetworkRBACTests(test.TestCase):
    """Functional tests for network rbac. """
    NET_NAME = uuid.uuid4().hex
    OBJECT_ID = None
    ID = None
    HEADERS = ['ID']
    FIELDS = ['id']

    @classmethod
    def setUpClass(cls):
        opts = cls.get_opts(cls.FIELDS)
        raw_output = cls.openstack('network create ' + cls.NET_NAME + opts)
        cls.OBJECT_ID = raw_output.strip('\n')
        opts = cls.get_opts(['id', 'object_id'])
        raw_output = cls.openstack('network rbac create ' +
                                   cls.OBJECT_ID +
                                   ' --action access_as_shared' +
                                   ' --target-project admin' +
                                   ' --type network' + opts)
        cls.ID, object_id, rol = tuple(raw_output.split('\n'))
        cls.assertOutput(cls.OBJECT_ID, object_id)

    @classmethod
    def tearDownClass(cls):
        raw_output = cls.openstack('network rbac delete ' + cls.ID)
        cls.assertOutput('', raw_output)
        raw_output = cls.openstack('network delete ' + cls.OBJECT_ID)
        cls.assertOutput('', raw_output)

    def test_network_rbac_list(self):
        opts = self.get_opts(self.HEADERS)
        raw_output = self.openstack('network rbac list' + opts)
        self.assertIn(self.ID, raw_output)

    def test_network_rbac_show(self):
        opts = self.get_opts(self.FIELDS)
        raw_output = self.openstack('network rbac show ' + self.ID + opts)
        self.assertEqual(self.ID + "\n", raw_output)