import os
import collections
import requests
import datetime
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://sqbu-github.cisco.com/api/v3/'
SEARCH_ISSUES = 'search/issues?'
QUERY_GET_ISSUES = 'q=repo:WebExSquared/spark-client-framework+label:{}+is:merged+merged:>{}&per_page=80'
GET_PULL = BASE_URL + 'repos/WebExSquared/spark-client-framework/pulls/'

def print_fancy_lines():
    print('\n\n*******************************************')
    print('\n*******************************************\n\n')

def get_token():
    token = os.environ['GITHUB_PERSONAL_TOKEN']
    if not token:
        raise ValueError('Need to set GITHUB_PERSONAL_TOKEN environ variable')
    return token

def get_auth_header():
    return { 'Authorization': 'token %s' % get_token() }

def build_get_prs_url(labels, merge_date):
    return BASE_URL + SEARCH_ISSUES + QUERY_GET_ISSUES.format(labels, merge_date)

def main():
    args = parse_input_args()
    get_prs = build_get_prs_url(args.labels, args.date)

    auth_header = get_auth_header()

    r = requests.get(get_prs, headers=auth_header, verify=False, timeout=5)

    all_prs = r.json()
    print('total count: %d' % all_prs['total_count'])
    print('items count: %d' % len(all_prs['items']))

    pr_info = collections.OrderedDict()

    for i in all_prs['items']:
        as_datetime = datetime.datetime.strptime(i['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
        pr_info[as_datetime] = i['number']

    print_fancy_lines()

    sorted_keys = sorted(pr_info.keys())

    print('\nSorted By Merge Date:')
    for k, v in pr_info.items():
        print('PR closed at: %s, PR Number: %d' % (k, v))

    print_fancy_lines()

    merged_shas = collections.OrderedDict()

    for i, k in enumerate(sorted_keys):
        pr_number = pr_info[k]
        print('%d: PR closed at: %s, PR Number: %d' % (i, k, pr_number))    

        pr = requests.get(GET_PULL + str(pr_number), headers=auth_header, verify=False, timeout=5)
        print(pr)
        pr_json = pr.json()
        merged_shas[k] = { pr_number: pr_json['merge_commit_sha'] }

    print_fancy_lines()

    for k, v in merged_shas.items():
        pr_number = pr_info[k]
        print('[PR %d](https://sqbu-github.cisco.com/WebExSquared/spark-client-framework/pull/%d) merged at: %s, Commit SHA: `%s`' % (pr_number, pr_number, k, v[pr_number]))

def parse_input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--labels', type=str, default="\"New User Journeys\"", help='PR labels to filter on')
    parser.add_argument('-d', '--date', type=str, default="2020-11-24", help='Date after which PRs were merged to master, format YYYY-MM-DD')
    return parser.parse_args()

if __name__ == '__main__':
    main()