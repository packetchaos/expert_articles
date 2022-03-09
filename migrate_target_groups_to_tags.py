from tenable.io import TenableIO
access_key = 'ACCESS_KEY_GOES_HERE'
secret_key = 'SECRET_KEY_GOES_HERE'

tio = TenableIO(access_key, secret_key, vendor='Casey Reid', product='Migrate Target Groups to Tags', build='0.0.1')

for tgroup in tio.target_groups.list():
    member = tgroup['members']
    name = tgroup['name']
    group_type = tgroup['type']

    description = 'Imported via a script'

    try:
        if name != 'Default':
            tio.tags.create(group_type, name, description, filters=[("ipv4", "eq", str(member))])
    except:
        print("\nDuplicate Tag found. Skiping\n")
