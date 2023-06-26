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

from sickle import Sickle

sickle = Sickle('http://trng-b2share.eudat.eu/api/oai2d')
sickle = Sickle('http://b2share.eudat.eu/api/oai2d')
sickle = Sickle('http://vm0897.kaj.pouta.csc.fi/api/oai2d')

eucrecords = sickle.ListRecords(metadataPrefix='eudatcore', set='591815be-a801-47c5-80e2-0a39f95c7def')

prefix = 'https://b2share.eudat.eu/records/'

count = 0

oai_records = []

for rec in eucrecords:
    id = rec.metadata.get('identifier')[0]
    if id.startswith(prefix):
        id = id[len(prefix):]
    oai_records.append({'title': rec.metadata.get('title')[0],
                 'id': id,
                 'publicationYear': rec.metadata.get('publicationYear')[0]
                })
#    print(rec.metadata.get('title'))
#    print(id)
#    print(rec.metadata.get('publicationYear'))
    count = count + 1
print(count)

# oai_records = sorted(oai_records, key=lambda d: d['publicationYear'])
oai_records = sorted(oai_records, key=lambda d: d['id'])