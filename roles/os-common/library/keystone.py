#!/usr/bin/python
# (c) 2014, Kevin Carter <kevin.carter@rackspace.com>
#
# Copyright 2014, Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Based on Jimmy Tang's implementation

DOCUMENTATION = """
---
module: keystone
version_added: "1.6.2"
short_description:
    - Manage OpenStack Identity (keystone) users, projects, roles, and
      endpoints.
description:
    - Manage OpenStack Identity (keystone) users, projects, roles, and
      endpoints.
options:
    return_code:
        description:
            - Allow for return Codes other than 0 when executing commands.
            - This is a comma separated list of acceptable return codes.
        default: 0
    login_user:
        description:
            - login username to authenticate to keystone
        required: false
        default: admin
    login_password:
        description:
            - Password of login user
        required: false
        default: 'yes'
    login_project_name:
        description:
            - The project login_user belongs to
        required: false
        default: None
    login_tenant_name:
        description:
            - The tenant login_user belongs to
        required: false
        default: None
    token:
        description:
            - The token to be uses in case the password is not specified
        required: false
        default: None
    endpoint:
        description:
            - The keystone url for authentication
        required: false
    password:
        description:
            - The password to be assigned to the user
        required: false
        default: None
    user_name:
        description:
            - The name of the user that has to added/removed from OpenStack
        required: false
        default: None
    project_name:
        description:
            - The project name that has be added/removed
        required: false
        default: None
    tenant_name:
        description:
            - The tenant name that has be added/removed
        required: false
        default: None
    role_name:
        description:
            - The name of the role to be assigned or created
        required: false
    service_name:
        description:
            - Name of the service.
        required: false
        default: None
    region_name:
        description:
            - Name of the region.
        required: false
        default: None
    domain_name:
        description:
            - Name of the domain to add a project to.
        required: false
        default: 'Default'
    description:
        description:
            - A description for the project
        required: false
        default: None
    email:
        description:
            - Email address for the user, this is only used in "ensure_user"
        required: false
        default: None
    service_type:
        description:
            - Type of service.
        required: false
        default: None
    endpoint_list:
        description:
            - List of endpoints to add to keystone for a service
        required: false
        default: None
        type: list
    group_name:
        description:
            - A name for the group
        required: False
        default: None
    idp_name:
        description:
            - A name for the identity provider
        required: False
        default: None
    idp_remote_ids:
        description:
            - A URL that identifies the remote identity provider
        required: False
        default: None
    idp_enabled:
        description:
            - Set whether a remote identity provider is enabled
        required: False
        default: True
    sp_name:
        description:
            - A name for the service provider
        required: False
        default: None
    sp_enabled:
        description:
            - Set whether a service provider is enabled
        required: False
        default: True
    sp_url:
        description:
            - URL where the service provider expects to receive SAML assertions
            - eg: http(s)://${SP_HOST}:5000/Shibboleth.sso/SAML2/ECP
        required: False
        default: None
    sp_auth_url:
        description:
            - URL for federated users to request tokens from
            - eg: http(s)://${SP_HOST}:5000/v3/OS-FEDERATION
                  /identity_providers/${IDP_ID}/saml2/auth
        required: False
        default: None
    protocol_name:
        description:
            - A name for the protocol
        required: False
        default: None
    mapping_name:
        description:
            - A name for the mapping
        required: False
        default: None
    mapping_rules:
        description:
            - A dictionary mapping federated users to local groups.
            - see: http://specs.openstack.org/openstack/keystone-specs
                   /api/v3/identity-api-v3-os-federation-ext.html#mappings
        required: False
        default: None
    domain_enabled:
        description:
            - Name for a domain
        required: False
        default: True
    command:
        description:
            - Indicate desired state of the resource
        choices: ['get_tenant', 'get_project', 'get_user', 'get_role',
                  'ensure_service', 'ensure_endpoint', 'ensure_role',
                  'ensure_user', 'ensure_user_role', 'ensure_tenant',
                  'ensure_project', 'ensure_service_provider',
                  'ensure_group', 'ensure_identity_provider',
                  'ensure_protocol', ensure_mapping',
                  'ensure_group_role']
        required: true
    insecure:
        description:
            - Explicitly allow client to perform "insecure" TLS
        choices:
            - false
            - true
        default: false
requirements: [ python-keystoneclient ]
author: Kevin Carter
"""

EXAMPLES = """
# Create an admin project
- keystone:
    command: "ensure_project"
    project_name: "admin"
    domain_name: "Default"
    description: "Admin project"

# Create a service project
- keystone:
    command: "ensure_project"
    project_name: "service"
    description: "Service project"

# Create an admin user
- keystone:
    command: "ensure_user"
    user_name: "admin"
    project_name: "admin"
    password: "secrete"
    email: "admin@some-domain.com"

# Create an admin role
- keystone:
    command: "ensure_role"
    role_name: "admin"

# Create a user
- keystone:
    command: "ensure_user"
    user_name: "glance"
    project_name: "service"
    password: "secrete"
    domain_name: "Default"
    email: "glance@some-domain.com"

# Add a role to a user
- keystone:
    command: "ensure_user_role"
    user_name: "glance"
    project_name: "service"
    role_name: "admin"

# Add a project role to a group
- keystone:
    command: "ensure_group_role"
    group_name: "fedgroup"
    project_name: "fedproject"
    role_name: "_member_"

# Create a service
- keystone:
    command: "ensure_service"
    service_name: "glance"
    service_type: "image"
    description: "Glance Image Service"

# Create an endpoint
- keystone:
    command: "ensure_endpoint"
    region_name: "RegionOne"
    service_name: "glance"
    service_type: "image"
    endpoint_list:
      - url: "http://127.0.0.1:9292"
        interface: "public"
      - url: "http://127.0.0.1:9292"
        interface: "admin"
      - url: "http://127.0.0.1:9292"
        interface: "internal"

# Get project id
- keystone:
    command: "get_project"
    project_name: "admin"

# Get user id
- keystone:
    command: "get_user"
    user_name: "admin"

# Get role id
- keystone:
    command: "get_role"
    user_name: "admin"

"""

COMMAND_MAP = {
    'get_tenant': {
        'variables': [
            'project_name',
            'tenant_name'
        ]
    },
    'get_project': {
        'variables': [
            'project_name',
            'tenant_name'
        ]
    },
    'get_user': {
        'variables': [
            'user_name'
        ]
    },
    'get_role': {
        'variables': [
            'role_name',
            'project_name',
            'tenant_name',
            'user_name'
        ]
    },
    'ensure_service': {
        'variables': [
            'service_name',
            'service_type',
            'description'
        ]
    },
    'ensure_endpoint': {
        'variables': [
            'region_name',
            'service_name',
            'service_type',
            'endpoint_list'
        ]
    },
    'ensure_role': {
        'variables': [
            'role_name'
        ]
    },
    'ensure_user': {
        'variables': [
            'project_name',
            'tenant_name',
            'user_name',
            'password',
            'email',
            'domain_name'
        ]
    },
    'ensure_user_role': {
        'variables': [
            'user_name',
            'project_name',
            'tenant_name',
            'role_name'
        ]
    },
    'ensure_group_role': {
        'variables': [
            'group_name',
            'project_name',
            'role_name'
        ]
    },
    'ensure_project': {
        'variables': [
            'project_name',
            'tenant_name',
            'description',
            'domain_name'
        ]
    },
    'ensure_tenant': {
        'variables': [
            'project_name',
            'tenant_name',
            'description',
            'domain_name'
        ]
    },
    'ensure_group': {
        'variables': [
            'group_name',
            'domain_name'
        ]
    },
    'ensure_identity_provider': {
        'variables': [
            'idp_name',
            'idp_remote_ids',
            'idp_enabled'
        ]
    },
    'ensure_service_provider': {
        'variables': [
            'sp_name',
            'sp_url',
            'sp_auth_url',
            'sp_enabled'
        ]
    },
    'ensure_protocol': {
        'variables': [
            'protocol_name',
            'idp_name',
            'mapping_name'
        ]
    },
    'ensure_mapping': {
        'variables': [
            'mapping_name',
            'mapping_rules',
        ]
    },
    'ensure_domain': {
        'variables': [
            'domain_name',
            'domain_enabled'
        ]
    }
}

try:
    from keystoneclient import exceptions as kexceptions
    from keystoneclient.v3 import client
except ImportError:
    keystoneclient_found = False
else:
    keystoneclient_found = True


class ManageKeystone(object):
    def __init__(self, module):
        """Manage Keystone via Ansible."""
        self.state_change = False
        self.keystone = None

        # Load AnsibleModule
        self.module = module

    def command_router(self):
        """Run the command as its provided to the module."""
        command_name = self.module.params['command']
        if command_name not in COMMAND_MAP:
            self.failure(
                error='No Command Found',
                rc=2,
                msg='Command [ %s ] was not found.' % command_name
            )

        action_command = COMMAND_MAP[command_name]
        if hasattr(self, '%s' % command_name):
            action = getattr(self, '%s' % command_name)
            facts = action(variables=action_command['variables'])
            if facts is None:
                self.module.exit_json(changed=self.state_change)
            else:
                self.module.exit_json(
                    changed=self.state_change,
                    ansible_facts=facts
                )
        else:
            self.failure(
                error='Command not in ManageKeystone class',
                rc=2,
                msg='Method [ %s ] was not found.' % command_name
            )

    @staticmethod
    def _facts(facts):
        """Return a dict for our Ansible facts.

        :param facts: ``dict``  Dict with data to return
        """
        return {'keystone_facts': facts}

    def _get_vars(self, variables, required=None):
        """Return a dict of all variables as found within the module.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        :param required: ``list``  Name of variables that are required.
        """
        return_dict = {}
        for variable in variables:
            return_dict[variable] = self.module.params.get(variable)
        else:
            if isinstance(required, list):
                for var_name in required:
                    check = return_dict.get(var_name)
                    if check is None:
                        self.failure(
                            error='Missing [ %s ] from Task or found a None'
                                  ' value' % var_name,
                            rc=000,
                            msg='variables %s - available params [ %s ]'
                                % (variables, self.module.params)
                        )
            return return_dict

    def failure(self, error, rc, msg):
        """Return a Failure when running an Ansible command.

        :param error: ``str``  Error that occurred.
        :param rc: ``int``     Return code while executing an Ansible command.
        :param msg: ``str``    Message to report.
        """
        self.module.fail_json(msg=msg, rc=rc, err=error)

    def _authenticate(self):
        """Return a keystone client object."""
        required_vars = ['endpoint']
        variables = [
            'endpoint',
            'login_user',
            'login_password',
            'login_project_name',
            'login_tenant_name',
            'token',
            'insecure'
        ]
        variables_dict = self._get_vars(variables, required=required_vars)

        endpoint = variables_dict.pop('endpoint')
        login_user = variables_dict.pop('login_user')
        login_password = variables_dict.pop('login_password')
        login_project_name = (variables_dict.pop('login_project_name', None) or
                              variables_dict.pop('login_tenant_name'))
        token = variables_dict.pop('token')
        insecure = variables_dict.pop('insecure')

        if token is None:
            if login_project_name is None:
                self.failure(
                    error='Missing Project Name',
                    rc=2,
                    msg='If you do not specify a token you must use a project'
                        ' name for authentication. Try adding'
                        ' [ login_project_name ] to the task'
                )
            if login_password is None:
                self.failure(
                    error='Missing Password',
                    rc=2,
                    msg='If you do not specify a token you must use a password'
                        ' name for authentication. Try adding'
                        ' [ login_password ] to the task'
                )

        if token:
            self.keystone = client.Client(
                insecure=insecure,
                endpoint=endpoint,
                token=token
            )
        else:
            self.keystone = client.Client(
                insecure=insecure,
                auth_url=endpoint,
                username=login_user,
                password=login_password,
                project_name=login_project_name
            )

    def _get_domain_from_vars(self, variables):
        # NOTE(sigmavirus24): Since we don't require domain, this will be None
        # in the dictionary. When we pop it, we can't provide a default
        # because 'domain' exists and is None. In order to use a default
        # value, we need to use `or 'default'` here to make sure we default to
        # the default domain. If we don't do it this way, Keystone throws a
        # 401 Unauthorized which is just plain wrong.
        domain_name = variables.pop('domain_name', None) or 'Default'

        return self._get_domain(name=domain_name)

    def _get_domain(self, name):
        """Return domain information.

        :param str name: Name of the domain.
        """
        for entry in self.keystone.domains.list():
            if entry.name == name:
                return entry
        else:
            return None

    def _get_project(self, name):
        """Return project information.

        Formerly, _get_tenant

        :param name: ``str``  Name of the project.
        """
        for entry in self.keystone.projects.list():
            if entry.name == name:
                return entry
        else:
            return None

    def get_tenant(self, variables):
        return self.get_project(variables)

    def get_project(self, variables):
        """Return a project id.

        This will return `None` if the ``name`` is not found.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """
        self._authenticate()
        variables_dict = self._get_vars(variables)
        project_name = (variables_dict.pop('project_name', None) or
                        variables_dict.pop('tenant_name'))
        project = self._get_project(name=project_name)
        if project is None:
            self.failure(
                error='project [ %s ] was not found.' % project_name,
                rc=2,
                msg='project was not found, does it exist?'
            )

        return self._facts(facts={'id': project.id})

    def ensure_tenant(self, variables):
        return self.ensure_project(variables)

    def ensure_project(self, variables):
        """Create a new project within Keystone if it does not exist.

        Returns the project ID on a successful run.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """
        self._authenticate()
        variables_dict = self._get_vars(variables)
        project_name = (variables_dict.pop('project_name', None) or
                        variables_dict.pop('tenant_name'))
        project_description = variables_dict.pop('description')
        if project_description is None:
            project_description = 'Project %s' % project_name

        domain = self._get_domain_from_vars(variables_dict)
        project = self._get_project(name=project_name)
        if project is None:
            self.state_change = True
            project = self.keystone.projects.create(
                name=project_name,
                description=project_description,
                domain=domain,
                enabled=True
            )

        return self._facts(facts={'id': project.id})

    def _get_user(self, name, domain):
        """Return a user information.

        This will return `None` if the ``name`` is not found.

        :param name: ``str``  Name of the user.
        """
        for entry in self.keystone.users.list(domain=domain):
            if getattr(entry, 'name', None) == name:
                return entry
        else:
            return None

    def get_user(self, variables):
        """Return a project id.

        This will return `None` if the ``name`` is not found.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """
        self._authenticate()
        variables_dict = self._get_vars(variables, required=['user_name'])
        user_name = variables_dict.pop('user_name')
        domain = self._get_domain_from_vars(variables_dict)
        user = self._get_user(name=user_name, domain=domain)
        if user is None:
            self.failure(
                error='user [ %s ] was not found.' % user_name,
                rc=2,
                msg='user was not found, does it exist?'
            )

        return self._facts(facts={'id': user.id})

    def ensure_user(self, variables):
        """Create a new user within Keystone if it does not exist.

        Returns the user ID on a successful run.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """
        self._authenticate()
        required_vars = ['user_name', 'password']
        variables_dict = self._get_vars(variables, required=required_vars)
        project_name = (variables_dict.pop('project_name', None) or
                        variables_dict.pop('tenant_name'))
        password = variables_dict.pop('password')
        user_name = variables_dict.pop('user_name')
        email = variables_dict.pop('email')

        domain = self._get_domain_from_vars(variables_dict)
        project = self._get_project(name=project_name)
        if project is None:
            self.failure(
                error='project [ %s ] was not found.' % project_name,
                rc=2,
                msg='project was not found, does it exist?'
            )

        user = self._get_user(name=user_name, domain=domain)
        if user is None:
            self.state_change = True
            user = self.keystone.users.create(
                name=user_name,
                password=password,
                email=email,
                domain=domain,
                default_project=project
            )

        return self._facts(facts={'id': user.id})

    def _get_role(self, name, domain):
        """Return a role by name.

        This will return `None` if the ``name`` is not found.

        :param name: ``str``  Name of the role.
        :param domain: ``str`` ID of the domain
        """
        for entry in self.keystone.roles.list(domain=domain):
            if entry.name == name:
                return entry
        else:
            return None

    def _get_group(self, name, domain='Default'):
        """Return a group by name.

        This will return `None` if the ``name`` is not found.

        :param name: ``str``  Name of the role.
        """
        for entry in self.keystone.groups.list(domain=domain):
            if domain is None:
                if entry.name == name:
                    return entry
            else:
                if entry.name == name and entry.domain_id == domain.id:
                    return entry
        else:
            return None

    def get_role(self, variables):
        """Return a role by name.

        This will return `None` if the ``name`` is not found.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """
        self._authenticate()
        variables_dict = self._get_vars(variables, required=['role_name'])
        role_name = variables_dict.pop('role_name')
        domain = self._get_domain_from_vars(variables_dict)
        role_data = self._get_role(name=role_name, domain=domain)
        if role_data is None:
            self.failure(
                error='role [ %s ] was not found.' % role_name,
                rc=2,
                msg='role was not found, does it exist?'
            )

        return self._facts(facts={'id': role_data.id})

    def _get_role_data(self, user_name, project_name, role_name, group_name,
                       domain):
        if user_name is not None:
            user = self._get_user(name=user_name, domain=domain)
            if user is None:
                self.failure(
                    error='user [ %s ] was not found.' % user_name,
                    rc=2,
                    msg='User was not found, does it exist?'
                )
        else:
            user = None

        project = self._get_project(name=project_name)
        if project is None:
            self.failure(
                error='project [ %s ] was not found.' % project_name,
                rc=2,
                msg='project was not found, does it exist?'
            )

        role = self._get_role(name=role_name, domain=domain)
        if role is None:
            self.failure(
                error='role [ %s ] was not found.' % role_name,
                rc=2,
                msg='role was not found, does it exist?'
            )

        if group_name is not None:
            group = self._get_group(name=group_name, domain=domain)
            if group is None:
                self.failure(
                    error='group [ %s ] was not found.' % group_name,
                    rc=2,
                    msg='group was not found, does it exist?'
                )
        else:
            group = None

        return user, project, role, group

    def ensure_role(self, variables):
        """Create a new role within Keystone if it does not exist.

        Returns the user ID on a successful run.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """
        self._authenticate()
        variables_dict = self._get_vars(variables, required=['role_name'])
        domain = self._get_domain_from_vars(variables_dict)
        role_name = variables_dict.pop('role_name')

        role = self._get_role(name=role_name, domain=domain)
        if role is None:
            self.state_change = True
            role = self.keystone.roles.create(role_name)

        return self._facts(facts={'id': role.id})

    def _get_user_roles(self, name, user, project):
        role_list = self.keystone.roles.list(
            user=user,
            project=project
        )
        for entry in role_list:
            if entry.name == name:
                return entry
        else:
            return None

    def _get_group_roles(self, name, group, project, domain):
        group_list = self.keystone.roles.list(
            group=group,
            project=project,
            domain=domain
        )
        for entry in group_list:
            if entry.name == name:
                return entry
        else:
            return None

    def ensure_user_role(self, variables):
        self._authenticate()
        required_vars = ['user_name', 'role_name']
        variables_dict = self._get_vars(variables, required=required_vars)
        domain = self._get_domain_from_vars(variables_dict)
        user_name = variables_dict.pop('user_name')
        # NOTE(sigmavirus24): Try to get the project_name, but
        # don't error out on it. This will change when the playbooks are
        # updated to use project_name instead of tenant_name
        project_name = (variables_dict.pop('project_name', None) or
                        variables_dict.pop('tenant_name'))
        role_name = variables_dict.pop('role_name')

        user, project, role, group = self._get_role_data(
            user_name=user_name, project_name=project_name,
            role_name=role_name, group_name=None, domain=domain
        )

        user_role = self._get_user_roles(
            name=role_name, user=user, project=project
        )

        if user_role is None:
            self.keystone.roles.grant(
                user=user, role=role, project=project
            )
            user_role = self._get_user_roles(
                name=role_name, user=user, project=project
            )

        return self._facts(facts={'id': user_role.id})

    def ensure_group_role(self, variables):
        self._authenticate()
        required_vars = ['group_name', 'project_name', 'role_name']
        variables_dict = self._get_vars(variables, required=required_vars)
        domain = self._get_domain_from_vars(variables_dict)
        group_name = variables_dict.pop('group_name')
        project_name = variables_dict.pop('project_name')
        role_name = variables_dict.pop('role_name')

        user, project, role, group = self._get_role_data(
            group_name=group_name, project_name=project_name,
            role_name=role_name, user_name=None, domain=domain
        )

        group_role = self._get_group_roles(
            name=role_name, group=group, project=project, domain=domain
        )

        if group_role is None:
            self.keystone.roles.grant(
                group=group, role=role, project=project
            )
            group_role = self._get_group_roles(
                name=role_name,
                group=group,
                project=project,
                domain=domain
            )

        return self._facts(facts={'id': group_role.id})

    def ensure_group(self, variables):
        """Create a new group within Keystone if it does not exist.

        Returns the group ID on a successful run.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """

        self._authenticate()
        required_vars = ['group_name', 'domain_name']
        variables_dict = self._get_vars(variables, required=required_vars)
        group_name = variables_dict.pop('group_name')

        domain = self._get_domain_from_vars(variables_dict)

        group = self._get_group(
            name=group_name, domain=domain
        )

        if group is None:
            self.state_change = True
            group = self.keystone.groups.create(
                name=group_name, domain=domain
            )

        return self._facts(facts={'id': group.id})

    def _get_service(self, name, srv_type=None):
        for entry in self.keystone.services.list():
            if srv_type is not None:
                if entry.type == srv_type and name == entry.name:
                    return entry
            elif entry.name == name:
                return entry
        else:
            return None

    def ensure_service(self, variables):
        """Create a new service within Keystone if it does not exist.

        Returns the service ID on a successful run.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """
        self._authenticate()
        required_vars = ['service_name', 'service_type']
        variables_dict = self._get_vars(variables, required=required_vars)

        service_name = variables_dict.pop('service_name')
        description = variables_dict.pop('description')
        service_type = variables_dict.pop('service_type')

        service = self._get_service(name=service_name, srv_type=service_type)
        if service is None or service.type != service_type:
            self.state_change = True
            service = self.keystone.services.create(
                name=service_name,
                type=service_type,
                description=description
            )

        return self._facts(facts={'id': service.id})

    def _get_endpoint(self, region, url, interface):
        for entry in self.keystone.endpoints.list():
            check = [
                entry.region == region,
                entry.url == url,
                entry.interface == interface
            ]
            if all(check):
                return entry
        else:
            return None

    def ensure_endpoint(self, variables):
        """Create a new endpoint within Keystone if it does not exist.

        Returns the endpoint ID on a successful run.

        :param variables: ``list``  List of all variables that are available to
                                    use within the Keystone Command.
        """
        self._authenticate()
        required_vars = [
            'region_name',
            'service_name',
            'service_type',
            'endpoint_list'
        ]
        variables_dict = self._get_vars(variables, required=required_vars)

        service_name = variables_dict.pop('service_name')
        service_type = variables_dict.pop('service_type')
        region = variables_dict.pop('region_name')
        endpoint_list = variables_dict.pop('endpoint_list')

        service = self._get_service(name=service_name, srv_type=service_type)
        if service is None:
            self.failure(
                error='service [ %s ] was not found.' % service_name,
                rc=2,
                msg='Service was not found, does it exist?'
            )

        endpoints = {}
        for endpoint_dict in endpoint_list:
            url = endpoint_dict.pop('url')
            interface = endpoint_dict.pop('interface')
            endpoint = self._get_endpoint(
                region=region,
                url=url,
                interface=interface
            )
            if endpoint is None:
                self.state_change = True
                endpoint = self.keystone.endpoints.create(
                    region=region,
                    service=service,
                    url=url,
                    interface=interface
                )
            endpoints[interface] = endpoint

        return self._facts(
            facts={'%sid' % interface: endpoint.id
                   for interface, endpoint in endpoints.items()})

    def _ensure_generic(self, manager, required_vars, variables):
        """Try and create a new 'thing' in keystone.

        Thing type is determined by the manager passed in.

        :param: manager - openstack object manager eg self.keystone.groups
        :param: required_vars - dictionary:
                ansible module argument name : manager argument name
                eg {'group_name': 'name'}

        :returns: Facts dictionary with things =
            <list of things converted to dict>

        TODO: make this handle updates as well as creates
        TODO (maybe, if we decide to use this module long term):
            migrate other ensures to use this
        """

        # Get values for variables
        variables_dict = self._get_vars(variables,
                                        required=required_vars.keys())

        # Translate ansible module argument names to manager expected names
        args_dict = {required_vars[k]: v for k, v in variables_dict.items()}

        try:
            manager.create(**args_dict)
            self.state_change = True
        except kexceptions.Conflict:
            self.state_change = False

        try:
            return self._facts(facts={
                manager.collection_key:
                    [x.to_dict() for x in manager.list()]
            })
        except TypeError:
            # some managers require arguments to their list functions :/
            # return no facts in this case.
            return self._facts(facts={})

    def ensure_identity_provider(self, variables):
        self._authenticate()
        return self._ensure_generic(
            manager=self.keystone.federation.identity_providers,
            required_vars={'idp_name': 'id',
                           'idp_remote_ids': 'remote_ids',
                           'idp_enabled': 'enabled'},
            variables=variables
        )

    def ensure_service_provider(self, variables):
        self._authenticate()
        return self._ensure_generic(
            manager=self.keystone.federation.service_providers,
            required_vars={'sp_name': 'id',
                           'sp_auth_url': 'auth_url',
                           'sp_url': 'sp_url',
                           'sp_enabled': 'enabled'},
            variables=variables
        )

    def ensure_protocol(self, variables):
        """Facts not returned

        This is because you can't list protocols without
        specifying an identity provider
        """

        self._authenticate()
        return self._ensure_generic(
            manager=self.keystone.federation.protocols,
            required_vars={'protocol_name': 'protocol_id',
                           'idp_name': 'identity_provider',
                           'mapping_name': 'mapping'},
            variables=variables
        )

    def ensure_mapping(self, variables):
        self._authenticate()
        return self._ensure_generic(
            manager=self.keystone.federation.mappings,
            required_vars={'mapping_name': 'mapping_id',
                           'mapping_rules': 'rules'},
            variables=variables
        )

    def ensure_domain(self, variables):
        self._authenticate()
        return self._ensure_generic(
            manager=self.keystone.domains,
            required_vars={'domain_name': 'name',
                           'domain_enabled': 'enabled'},
            variables=variables
        )


def main():
    module = AnsibleModule(
        argument_spec=dict(
            login_user=dict(
                required=False
            ),
            login_password=dict(
                required=False
            ),
            login_tenant_name=dict(
                required=False
            ),
            login_project_name=dict(
                required=False
            ),
            token=dict(
                required=False
            ),
            password=dict(
                required=False
            ),
            endpoint=dict(
                required=True,
            ),
            user_name=dict(
                required=False
            ),
            tenant_name=dict(
                required=False
            ),
            project_name=dict(
                required=False
            ),
            domain_name=dict(
                required=False
            ),
            role_name=dict(
                required=False
            ),
            service_name=dict(
                required=False
            ),
            region_name=dict(
                required=False
            ),
            description=dict(
                required=False
            ),
            email=dict(
                required=False
            ),
            service_type=dict(
                required=False
            ),
            endpoint_list=dict(
                required=False,
                type='list'
            ),
            command=dict(
                required=True,
                choices=COMMAND_MAP.keys()
            ),
            insecure=dict(
                default=False,
                required=False,
                choices=BOOLEANS + ['True', 'False']
            ),
            return_code=dict(
                type='str',
                default='0'
            ),
            group_name=dict(
                type='str',
                required=False
            ),
            idp_remote_ids=dict(
                type='list',
                required=False,
            ),
            idp_name=dict(
                type='str',
                required=False,
            ),
            idp_enabled=dict(
                type='bool',
                default=True,
                required=False,
            ),
            sp_name=dict(
                type='str',
                required=False,
            ),
            sp_auth_url=dict(
                type='str',
                required=False,
            ),
            sp_url=dict(
                type='str',
                required=False,
            ),
            sp_enabled=dict(
                type='bool',
                default=True,
                required=False,
            ),
            protocol_name=dict(
                type='str',
                required=False,
            ),
            mapping_name=dict(
                type='str',
                required=False,
            ),
            mapping_rules=dict(
                type='list',
                required=False,
            ),
            domain_enabled=dict(
                type='bool',
                required=False,
                default=True
            )
        ),
        supports_check_mode=False,
        mutually_exclusive=[
            ['token', 'login_user'],
            ['token', 'login_password'],
            ['token', 'login_tenant_name']
        ]
    )

    km = ManageKeystone(module=module)
    if not keystoneclient_found:
        km.failure(
            error='python-keystoneclient is missing',
            rc=2,
            msg='keystone client was not importable, is it installed?'
        )

    return_code = module.params.get('return_code', '').split(',')
    module.params['return_code'] = return_code
    km.command_router()


# import module snippets
from ansible.module_utils.basic import *  # NOQA
if __name__ == '__main__':
    main()
