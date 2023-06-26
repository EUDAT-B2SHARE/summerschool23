# -*- coding: utf-8 -*-
#
# This file is part of EUDAT B2Share.
# Copyright (C) 2023 CSC - IT Center for Science Ltd.
#
# B2Share is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# B2Share is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with B2Share; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

import json
import os
import re
from uuid import UUID
from invenio_db import db
from b2share.modules.communities import Community
from b2share.modules.schemas import BlockSchema, CommunitySchema
from b2share.modules.schemas.helpers import resolve_schemas_ref

def resolve_block_schema_id(source):
    """Resolve all references to Block Schema and replace them with their ID.

    Every instance of '$BLOCK_SCHEMA_ID[<schema_name>]' will be replaced with
    the corresponding ID.

    Args:
        source (str): the source string to transform.

    Returns:
        str: a copy of source with the references replaced.
    """
    def block_schema_ref_match(match):
        name = match.group(1)
        found_schemas = BlockSchema.get_all_block_schemas(name=name)
        if len(found_schemas) > 1:
            raise Exception(
                'Too many schemas matching name "{}".'.format(name))
        elif len(found_schemas) == 0:
            raise Exception('No schema matching name "{}" found.'.format(name))
        return found_schemas[0]
    return re.sub(
        r'\$BLOCK_SCHEMA_ID\[([^\]:]+)\]',
        lambda m: str(block_schema_ref_match(m).id),
        source
    )

try:
    with db.session.begin_nested():
        print('Creating a Community')
        #with os.fdopen(3, 'r') as json_file:
        with open("/eudat/demo/eudat.json") as json_file:
        #with open(os.path.join(os.getcwd(), "/eudat/demo/eudat.json")) as json_file:
            json_config = json.loads(json_file.read())
            workflow = json_config.get('publication_workflow',
                                    'review_and_publish')
            is_restricted = json_config.get('restricted_submission',
                                            False)
            community = Community.create_community(
                name=json_config['name'],
                description=json_config['description'],
                logo=json_config['logo'],
                publication_workflow=workflow,
                restricted_submission=is_restricted,
                id_=UUID(json_config['id']),
            )
            print('Community created')

            print('Creating BlockSchemas for Community')
            for schema_name, schema in json_config['block_schemas'].items():
                block_schema = BlockSchema.create_block_schema(
                    community.id,
                    schema_name,
                    id_=UUID(schema['id']),
                )
                for json_schema in schema['versions']:
                    block_schema.create_version(json_schema)
            print('BlockSchemas created')

            print('Creating CommunitySchemas for Community')
            for schema in json_config['community_schemas']:
                json_schema_str = json.dumps(schema['json_schema'])
                # expand variables in the json schema
                json_schema_str = resolve_block_schema_id(json_schema_str)
                json_schema_str = resolve_schemas_ref(json_schema_str)
                CommunitySchema.create_version(
                    community_id=community.id,
                    community_schema=json.loads(json_schema_str),
                    root_schema_version=int(schema['root_schema_version']))
            print('CommunitySchemas created')
    db.session.commit()

    print('Successfully created a Community and its Schemas')
except Exception as e:
    print('Something went wrong.')
    print(e)
