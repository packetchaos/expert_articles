from tenable.io import TenableIO
access_key = 'ACCESS_KEY_GOES_HERE'
secret_key = 'SECRET_KEY_GOES_HERE'

tio = TenableIO(access_key, secret_key, vendor='Casey Reid', product='expert-article-examples', build='0.0.1')


def get_target_group_members(target_group_list):
    text_target_string = ""
    for target_id in target_group_list:
        text_target_string += ",{}".format(tio.target_groups.details(target_id)['members'])
    return text_target_string[1:]


def get_target_group_ids_from_a_scan(scan_id):
    scan_data = tio.get('editor/scan/{}'.format(str(scan_id))).json()

    for scan_basic_inputs in scan_data["settings"]["basic"]["inputs"]:
        if scan_basic_inputs["name"] == "Target Groups":
            return scan_basic_inputs["default"]


new_text_targets = get_target_group_members(get_target_group_ids_from_a_scan(5647))
update_scan = tio.scans.configure(5647, target_groups=[], targets=[new_text_targets])

print(update_scan)

