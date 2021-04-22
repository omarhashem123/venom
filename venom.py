import concurrent.futures
import argparse
import os
import time
import random
import re
import requests

import colorama
colorama.init()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


parser = argparse.ArgumentParser(usage=bcolors.OKGREEN +"\nto extract endpoints from crawl:" +bcolors.ENDC + "\npython3 venom.py -f <file> -t <threads> -o <output> -l <depth level> -s <scope> -time <delay> -spider\nOR\npython3 venom.py -f <file> -t <threads> -o <output> -l <depth level> -s <scope> -time <delay> -cookie <cookie> -spider\n" +  bcolors.OKGREEN + "to extract disallowed endpoinds and allowed endpoints from robots.txt:" + bcolors.ENDC + "\npython3 venom.py -f <file> -t <threads> -o <output> -time <delay> -robots\n" + bcolors.OKGREEN + "to extract endpoints from sitemap.xml:" + bcolors.ENDC + "\npython3 venom.py -f <file> -t <threads> -o <output> -time <delay> -sitemap\n" + bcolors.OKGREEN + "to extract endpoints from wayback machine:" + bcolors.ENDC + "\npython3 venom.py -d <domain> -o <output> -archive\nOR\npython3 venom.py -f <file> -t <threads> -o <output> -archive\n" + bcolors.OKGREEN + "to extract subdomains from crt.sh:" + bcolors.ENDC + "\npython3 venom.py -d <domain> -o <output file> -crtsh\n",
    description=bcolors.WARNING + 'description:Tool that spider subdomains and extract endpoints' + bcolors.ENDC)
parser.add_argument('-f', help='<file contain subdomains>')
parser.add_argument('-d', help='<domain or subdomain>')
parser.add_argument('-s', help='<file that contain only domains in scope to validate it and extract out of scope>')
parser.add_argument('-time', help='<time to sleep between threads>', nargs="?", const=5)
parser.add_argument('-t', help='<threads>', nargs="?", const=1)
parser.add_argument('-l', help='<levels of crawl>')
parser.add_argument('-o', help='<folder that contain results>', nargs="?", const='results')
parser.add_argument('-spider', help='<extract endpoints from spider websites>', nargs="?", const='NotNone')
parser.add_argument('-cookie', help='<crawl with Cookie>')
parser.add_argument('-robots', help='<extract allowed endpoints and extract disallowed endpoints>', nargs="?", const='NotNone')
parser.add_argument('-sitemap', help='<extract endpoints from sitemap.xml>', nargs="?", const='NotNone')
parser.add_argument('-archive', help='<extract endpoints from Wayback Machine>', nargs="?", const='NotNone')
parser.add_argument('-crtsh', help='<extract subdomains from crt.sh>', nargs="?", const='NotNone')
args = parser.parse_args()


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (X11; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
]


#used in function spider() and main function to extract failed threads
failed_threads_from_spider = []
succeed_threads_from_spider = []
#used in function spider() to extract out of scope
try:
    file_contain_scope = open(args.s).readlines()
    scope = []
    for i in file_contain_scope:
        scope.append(i.strip())
except:
    pass


def spider(sub_domain):
    # add headers
    headers = {'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': random.choice(user_agents),
               'Referer': sub_domain}
    # crawl with cookie
    if args.cookie is not None:
        headers['Cookie'] = args.cookie

    failed_threads_from_spider.append(sub_domain)
    req = requests.get(sub_domain,headers=headers)
    succeed_threads_from_spider.append(sub_domain)
    extract_links_from_href_and_src = re.findall('href="(.*?)"|src="(.*?)"', req.text)
    file_contain_links = open(args.o + "/endpoint_from_crawl_website", "a")
    for link in extract_links_from_href_and_src:
        if re.match("http", link[0]):
            #extract out of scope
            for j in scope:
                if re.search(j, link[0]):
            #write endpoint to file
                    file_contain_links.write(link[0] + "\n")
                    print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + link[0] + bcolors.ENDC)

        elif re.match("(.*?)\.com(.*?)|(.*?)\.org(.*?)|(.*?)\.net(.*?)|(.*?)\.int(.*?)|(.*?)\.edu(.*?)|(.*?)\.gov(.*?)|(.*?)\.mil(.*?)|(.*?)\.co(.*?)|(.*?)\.us(.*?)|(.*?)\.de(.*?)|(.*?)\.uk(.*?)|(.*?)\.icu(.*?)|(.*?)\.ru(.*?)|(.*?)\.info(.*?)|(.*?)\.top(.*?)|(.*?)\.xyz(.*?)|(.*?)\.tk(.*?)|(.*?)\.cn(.*?)|(.*?)\.ga(.*?)|(.*?)\.cf(.*?)|(.*?)\.nl(.*?)", link[0]):
            if re.match("http", link[0]):
                # extract out of scope
                for j in scope:
                    if re.search(j, link[0]):
                # write endpoint to file
                        file_contain_links.write(link[0] + "\n")
                        print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + link[0] + bcolors.ENDC)
            elif re.match("//", link[0]):
                # extract out of scope
                for j in scope:
                    if re.search(j, link[0]):
                # write endpoint to file
                        file_contain_links.write("http:" + link[0] + "\n")
                        print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + "http:" + link[0] + bcolors.ENDC)
            elif re.match("/", link[0]):
                # extract out of scope
                for j in scope:
                    if re.search(j, link[0]):
                # write endpoint to file
                        file_contain_links.write("http:/" + link[0] + "\n")
                        print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + "http:/" + link[0] + bcolors.ENDC)
            else:
                pass
        elif re.match("//", link[0]):
            # extract out of scope
            for j in scope:
                if re.search(j, sub_domain + link[0]):
            # write endpoint to file
                    file_contain_links.write("http://" + sub_domain + link[0])
                    print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + "http://" + link[0] + bcolors.ENDC)
        elif re.match("/", link[0]):
            # extract out of scope
            for j in scope:
                if re.search(j, sub_domain + link[0]):
            # write endpoint to file
                    file_contain_links.write(sub_domain + link[0] + "\n")
                    print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + sub_domain + link[0] + bcolors.ENDC)

        if re.match("http(.*?)", link[1]):
            #extract out of scope
            for j in scope:
                if re.search(j, link[1]):
            #write endpoint to file
                    file_contain_links.write(link[1] + "\n")
                    print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + link[1] + bcolors.ENDC)

        elif re.match("(.*?)\.com(.*?)|(.*?)\.org(.*?)|(.*?)\.net(.*?)|(.*?)\.int(.*?)|(.*?)\.edu(.*?)|(.*?)\.gov(.*?)|(.*?)\.mil(.*?)|(.*?)\.co(.*?)|(.*?)\.us(.*?)|(.*?)\.de(.*?)|(.*?)\.uk(.*?)|(.*?)\.icu(.*?)|(.*?)\.ru(.*?)|(.*?)\.info(.*?)|(.*?)\.top(.*?)|(.*?)\.xyz(.*?)|(.*?)\.tk(.*?)|(.*?)\.cn(.*?)|(.*?)\.ga(.*?)|(.*?)\.cf(.*?)|(.*?)\.nl(.*?)", link[1]):
            if re.match("http(.*?)", link[1]):
                # extract out of scope
                for j in scope:
                    if re.search(j, link[1]):
                # write endpoint to file
                        file_contain_links.write(link[1] + "\n")
                        print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + link[1] + bcolors.ENDC)
            elif re.match("//(.*?)", link[1]):
                # extract out of scope
                for j in scope:
                    if re.search(j, link[1]):
                # write endpoint to file
                        file_contain_links.write("http:" + link[1] + "\n")
                        print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + "http:" + link[1] + bcolors.ENDC)
            elif re.match("/", link[1]):
                # extract out of scope
                for j in scope:
                    if re.search(j, link[1]):
                # write endpoint to file
                        file_contain_links.write("http:/" + link[1] + "\n")
                        print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + "http:/" + link[1] + bcolors.ENDC)
            else:
                pass

        elif re.match("//", link[1]):
            # extract out of scope
            for j in scope:
                if re.search(j, sub_domain + link[1]):
            # write endpoint to file
                    file_contain_links.write("http://" + sub_domain + link[1])
                    print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + "http://" + link[1] + bcolors.ENDC)
        elif re.match("/", link[1]):
            # extract out of scope
            for j in scope:
                if re.search(j, sub_domain + link[1]):
            # write endpoint to file
                    file_contain_links.write(sub_domain + link[1] + "\n")
                    print(bcolors.FAIL + "[Endpoint from crawl]  " + bcolors.ENDC +bcolors.OKGREEN + sub_domain + link[1] + bcolors.ENDC)
    # delay between threads
    if args.time is not None:
        time.sleep(int(args.time))


#used in function sitemap_xml() and main function to extract failed threads
succeed_threads = []
failed_threads = []
def sitemap_xml(subdomain):
    # add headers
    headers = {'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': random.choice(user_agents),
               'Referer': subdomain}
    #extract endpoints from sitemap.xml and write failed threads
    failed_threads.append(subdomain)
    request_parent_sitemap = requests.get(subdomain,headers=headers)
    succeed_threads.append(subdomain)
    file_contain_all_endpoints = open(args.o + "/endpoints_from_sitemap", "a")
    extract_endpoint_from_parent_sitemap = re.findall("<loc>(.*?)</loc>", request_parent_sitemap.text)
    extract_all_href_from_parent_sitemap = re.findall('href="(.*?)"', request_parent_sitemap.text)
    for endpoint in extract_endpoint_from_parent_sitemap:
        if re.search("(.*?)\.xml(.*?)", endpoint):
            sitemap_xml(endpoint)
        else:
            file_contain_all_endpoints.write(endpoint + "\n")
            print(bcolors.FAIL + "[Endpoint from sitemap.xml]  " + bcolors.ENDC +bcolors.OKGREEN + endpoint + bcolors.ENDC)
    for endpoint in extract_all_href_from_parent_sitemap:
        if re.search("(.*?)\.xml(.*?)", endpoint):
            sitemap_xml(endpoint)
        else:
            file_contain_all_endpoints.write(endpoint + "\n")
            print(bcolors.FAIL + "[Endpoint from sitemap.xml]  " + bcolors.ENDC +bcolors.OKGREEN + endpoint + bcolors.ENDC)
    #delay between threads
    if args.time is not None:
        time.sleep(int(args.time))

#used in function robots_txt and main function to extract failed threads
failed_threads_robots = []
succeed_threads_robots = []
def robots_txt(sub_domain):
    # add headers
    headers = {'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': random.choice(user_agents),
               'Referer': sub_domain}
    failed_threads_robots.append(sub_domain)
    file_contain_allowed_endpoint = open(args.o + "/endpoints_from_robots_txt", "a")
    req = requests.get(sub_domain+"/robots.txt",headers=headers)
    succeed_threads_robots.append(sub_domain)
    extract_allow_endpoint = re.findall("Allow:(.*?)\n", req.text)

    for endpoint in extract_allow_endpoint:
        file_contain_allowed_endpoint.write(sub_domain + endpoint.strip() + "\n")
        print(bcolors.FAIL + "[Endpoint from robots.txt]  " + bcolors.ENDC +bcolors.OKGREEN + sub_domain + endpoint.strip() + bcolors.ENDC)

    file_contain_disallow_endpoint = open(args.o + "/disallowed_endpoint_from_robots", "a")
    extract_disallow_endpoint = re.findall("Disallow:(.*?)\n", req.text)

    for endpoint in extract_disallow_endpoint:
        file_contain_disallow_endpoint.write(sub_domain + endpoint.strip() + "\n")
        print(bcolors.FAIL + "[Endpoint from robots.txt]  " + bcolors.ENDC +bcolors.OKGREEN + sub_domain + endpoint.strip()  + bcolors.ENDC)
    #delay between threads
    if args.time is not None:
        time.sleep(int(args.time))


def crt_sh(domain):
    req = requests.get("https://crt.sh/?q=%." + domain + "&output=json")
    res = req.json()
    file_contain_endpoints_from_crt_sh = open(args.o + "/endpoints_from_crt_sh", "a")
    for i in res:
        sub = i["name_value"]
        replaced = sub.replace("*.", "")
        file_contain_endpoints_from_crt_sh.write(replaced + "\n")
        print(bcolors.FAIL + "[Sub domain from crt.sh]  " + bcolors.ENDC +bcolors.OKGREEN + replaced  + bcolors.ENDC)



def remove_duplicate(path_of_file):
    file_contain_duplicated = open(path_of_file).readlines()
    file_contain_duplicated = set(file_contain_duplicated)
    file_contain_not_duplicated = open(path_of_file, "w")
    for endpoint in file_contain_duplicated:
        file_contain_not_duplicated.write(endpoint)

#used in function wayback_machine to extract failed threads
failed_threads_from_archive = []
succeed_threads_from_archive = []
def wayback_machine(subdomain):
    failed_threads_from_archive.append(subdomain)
    req = requests.get("https://web.archive.org/cdx/search/cdx?url=*." + subdomain+ "/*&output=text&fl=original&collapse=urlkey")
    succeed_threads_from_archive.append(subdomain)
    file = open(args.o + "/endpoints_from_archive", "a")
    file.write(req.text + "\n")
    file.close()


def logo():
    print(bcolors.FAIL+'''
    ██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗
    ██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║
    ██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║
    ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║
     ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
      ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ version:2.0
    Coded by:Omar Hashem
    Twitter:@omarhashem666                                                                                                                                                                                      
    '''+bcolors.ENDC)


if __name__ == '__main__':
    #sitemap.xml()
    if args.f is not None and args.t is not None and args.o is not None and args.sitemap is not None:
        logo()
        os.system("mkdir " + args.o)
        file_contain_subdomains = open(args.f).readlines()
        #check http for subdomains
        subdomains = []
        for i in file_contain_subdomains:
            if re.match("http", i):
                subdomains.append(i.strip())
            else:
                i = "http://" + i
                subdomains.append(i.strip())
        #add sitemap for subdomains for sitemap_xml
        subdomains_for_sitemap_xml = []
        for i in subdomains:
            subdomains_for_sitemap_xml.append(i + "/sitemap.xml")
        subdomains_for_sitemap_xml = set(subdomains_for_sitemap_xml)
        #send subdomains for sitemap_xml(subdomain)
        print(bcolors.BOLD + "Extract endpoints from sitemap" + bcolors.ENDC)
        #solve problem of stuck threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.t)) as execution:
            execution.map(sitemap_xml, subdomains_for_sitemap_xml)
# extract failed threads cuz may be appear error so you will need nt kill script then you can complete from failed threads not from first file
            # algorithm to solve problem of stuck threads if it stucked in any time to exit tool and start it again where the tool end
            if len(subdomains) > 200:
                succeed_threads_from_sitemap_222 = ''
                while True:
                    succeed_threads_from_sitemap_to_test = len(succeed_threads)
                    if len(failed_threads) >= len(subdomains):
                        for i in range(8):
                            time.sleep(10)

                            if len(succeed_threads) == succeed_threads_from_sitemap_222:
                                time.sleep(int(args.time)/8)
                            else:
                                succeed_threads_from_sitemap_222 = len(succeed_threads)

                                # extract failed threads
                                failed_threads_from_sitemap_111 = set(failed_threads)
                                succeed_threads_from_sitemap_111 = set(succeed_threads)
                                file_contain_failed_threads_111 = open(args.o + "/failed_threads", "w")
                                true_failed_111 = failed_threads_from_sitemap_111.difference(
                                    succeed_threads_from_sitemap_111)
                                for thread in true_failed_111:
                                    find = re.findall("(.*?)/sitemap\.xml", thread)
                                    file_contain_failed_threads_111.write(find[0] + "\n")
                                dosent_requested_sub = subdomains_for_sitemap_xml.difference(failed_threads)
                                for sub in dosent_requested_sub:
                                    find = re.findall("(.*?)/sitemap\.xml", sub)
                                    file_contain_failed_threads_111.write(find[0] + "\n")
                                file_contain_failed_threads_111.close()

                        time.sleep(5)
                        if len(succeed_threads) == succeed_threads_from_sitemap_222:
                            break
                    succeed_threads_from_sitemap_222 = succeed_threads_from_sitemap_to_test
                    # extract failed threads
                    failed_threads_from_sitemap_111 = set(failed_threads)
                    succeed_threads_from_sitemap_111 = set(succeed_threads)
                    file_contain_failed_threads_111 = open(args.o + "/failed_threads", "w")
                    true_failed_111 = failed_threads_from_sitemap_111.difference(succeed_threads_from_sitemap_111)
                    for thread in true_failed_111:
                        find = re.findall("(.*?)/sitemap\.xml", thread)
                        file_contain_failed_threads_111.write(find[0] + "\n")
                    dosent_requested_sub = subdomains_for_sitemap_xml.difference(failed_threads)
                    for sub in dosent_requested_sub:
                        find = re.findall("(.*?)/sitemap\.xml", sub)
                        file_contain_failed_threads_111.write(find[0] + "\n")
                    file_contain_failed_threads_111.close()
                    if args.time is None: args.time = 0
                    time.sleep(5)

        # complete extracting failed threads
        file_contain_failed_threads_from_sitemap = open(args.o + "/failed_threads_from_sitemap", "w")
        failed_threads = set(failed_threads)
        succeed_threads = set(succeed_threads)
        true_failed = failed_threads.difference(succeed_threads)
        for thread in true_failed:
            find = re.findall("(.*?)/sitemap\.xml", thread)
            file_contain_failed_threads_from_sitemap.write(find[0] + "\n")
        #remove duplicated lines
        try:
            remove_duplicate(args.o + "/endpoints_from_sitemap")
        except:
            pass

    #robots.txt()
    elif args.f is not None and args.t is not None and args.o is not None and args.robots is not None:
        logo()
        os.system("mkdir " + args.o)
        file_contain_subdomains = open(args.f).readlines()
        #check http for subdomains
        subdomains = []
        for i in file_contain_subdomains:
            if re.match("http", i):
                subdomains.append(i.strip())
            else:
                i = "http://" + i
                subdomains.append(i.strip())
        subdomains = set(subdomains)
        print(bcolors.BOLD + "Extract endpoints from robots.tx" + bcolors.ENDC)
        #solve problem of stuck threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.t)) as execution:
            execution.map(robots_txt, subdomains)
# extract failed threads cuz may be appear error so you will need nt kill script then you can complete from failed threads not from first file
            # algorithm to solve problem of stuck threads if it stucked in any time to exit tool and start it again where the tool end
            if len(subdomains) > 1500:
                succeed_threads_from_robots_222 = ''
                while True:
                    succeed_threads_from_robots_to_test = len(succeed_threads_robots)
                    if len(failed_threads_robots) == len(subdomains):
                        for i in range(8):
                            time.sleep(10)

                            if len(succeed_threads_robots) == succeed_threads_from_robots_222:
                                time.sleep(int(args.time) / 8)
                            else:
                                succeed_threads_from_robots_222 = len(succeed_threads_robots)

                                # extract failed threads
                                failed_threads_from_robots_111 = set(failed_threads_robots)
                                succeed_threads_from_robots_111 = set(succeed_threads_robots)
                                file_contain_failed_threads_111 = open(args.o + "/failed_threads_from_robots", "w")
                                true_failed_111 = failed_threads_from_robots_111.difference(
                                    succeed_threads_from_robots_111)
                                for thread in true_failed_111:
                                    file_contain_failed_threads_111.write(thread + "\n")
                                dosent_requested_sub = subdomains.difference(failed_threads_robots)
                                for sub in dosent_requested_sub:
                                    file_contain_failed_threads_111.write(sub + "\n")
                                file_contain_failed_threads_111.close()

                        time.sleep(5)
                        if len(succeed_threads_robots) == succeed_threads_from_robots_222:
                            break
                    succeed_threads_from_robots_222 = succeed_threads_from_robots_to_test
                    # extract failed threads
                    failed_threads_from_robots_111 = set(failed_threads_robots)
                    succeed_threads_from_robots_111 = set(succeed_threads_robots)
                    file_contain_failed_threads_111 = open(args.o + "/failed_threads_from_robots", "w")
                    true_failed_111 = failed_threads_from_robots_111.difference(succeed_threads_from_robots_111)
                    for thread in true_failed_111:
                        file_contain_failed_threads_111.write(thread + "\n")
                    dosent_requested_sub = subdomains.difference(failed_threads_robots)
                    for sub in dosent_requested_sub:
                        file_contain_failed_threads_111.write(sub + "\n")
                    file_contain_failed_threads_111.close()
                    if args.time is None: args.time = 0
                    time.sleep(5)
        file_contain_failed_threads_from_robots = open(args.o + "/failed_threads_from_robots", "w")
        failed_threads_robots = set(failed_threads_robots)
        succeed_threads_robots = set(succeed_threads_robots)
        true_failed = failed_threads_robots.difference(succeed_threads_robots)
        for thread in true_failed:
            file_contain_failed_threads_from_robots.write(thread + "\n")
        #remove duplicated lines
        try:
            remove_duplicate(args.o + "/endpoints_from_robots_txt")
        except:
            pass
        try:
            remove_duplicate(args.o + "/disallowed_endpoint_from_robots")
        except:
            pass

    #spider()
    elif args.f is not None and args.t is not None and args.o is not None and args.spider is not None and args.s is not None:
        logo()
        os.system("mkdir " + args.o)
        file_contain_subdomains = open(args.f).readlines()
        sub_domains = []
        for i in file_contain_subdomains:
            if re.match("http", i):
                sub_domains.append(i.strip())
            else:
                i = "http://" + i
                sub_domains.append(i.strip())
        sub_domains = set(sub_domains)
        print(bcolors.BOLD + "Extract endpoints from crawl" + bcolors.ENDC)
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.t)) as execution:
            execution.map(spider, sub_domains)
#extract failed threads cuz may be appear error so you will need nt kill script then you can complete from failed threads not from first file

            # algorithm to solve problem of stuck threads if it stucked in any time to exit tool and start it again where the tool end
            if len(sub_domains) > 1500:
                succeed_threads_from_spider_222 = ''
                while True:

                    succeed_threads_from_spider_to_test = len(succeed_threads_from_spider)
                    if len(failed_threads_from_spider) == len(sub_domains):
                        for i in range(8):
                            time.sleep(10)


                            if len(succeed_threads_from_spider) == succeed_threads_from_spider_222:
                                time.sleep(int(args.time) / 8)

                            else:

                                succeed_threads_from_spider_222 = len(succeed_threads_from_spider)

                                # extract failed threads
                                failed_threads_from_spider_111 = set(failed_threads_from_spider)
                                succeed_threads_from_spider_111 = set(succeed_threads_from_spider)
                                file_contain_failed_threads_111 = open(args.o + "/failed_threads", "w")
                                true_failed_111 = failed_threads_from_spider_111.difference(
                                    succeed_threads_from_spider_111)
                                for thread in true_failed_111:
                                    file_contain_failed_threads_111.write(thread + "\n")
                                dosent_requested_sub = sub_domains.difference(failed_threads_from_spider)
                                for sub in dosent_requested_sub:
                                    file_contain_failed_threads_111.write(sub + "\n")
                                file_contain_failed_threads_111.close()

                        time.sleep(5)
                        if len(succeed_threads_from_spider) == succeed_threads_from_spider_222:
                            break

                    succeed_threads_from_spider_222 = succeed_threads_from_spider_to_test
                    # extract failed threads
                    failed_threads_from_spider_111 = set(failed_threads_from_spider)
                    succeed_threads_from_spider_111 = set(succeed_threads_from_spider)
                    file_contain_failed_threads_111 = open(args.o + "/failed_threads", "w")
                    true_failed_111 = failed_threads_from_spider_111.difference(succeed_threads_from_spider_111)
                    for thread in true_failed_111:
                        file_contain_failed_threads_111.write(thread + "\n")
                    dosent_requested_sub = sub_domains.difference(failed_threads_from_spider)
                    for sub in dosent_requested_sub:
                        file_contain_failed_threads_111.write(sub + "\n")
                    file_contain_failed_threads_111.close()
                    if args.time is None: args.time = 0
                    time.sleep(5)
        # extract failed threads from spider()
        file_contain_failed_threads = open(args.o + "/failed_threads", "w")
        failed_threads_from_spider = set(failed_threads_from_spider)
        succeed_threads_from_spider = set(succeed_threads_from_spider)
        true_failed = failed_threads_from_spider.difference(succeed_threads_from_spider)
        remove_duplicate(args.o + "/endpoint_from_crawl_website")
        for thread in true_failed:
            file_contain_failed_threads.write(thread + "\n")

    #crawl_levels
        if args.l is not None:
            for i in range(2, int(args.l) + 1):
                failed_threads_from_spider = []
                succeed_threads_from_spider = []
                os.system("mkdir " + args.o + "/crawl_level_" + str(i))
                sub = open(args.o + "/endpoint_from_crawl_website").readlines()
                sub_domains = []
                for endpoint in sub:
                    sub_domains.append(endpoint.strip())
                sub_domains = set(sub_domains)

                args.o = args.o + "/crawl_level_" + str(i)
                with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.t)) as execution:
                    execution.map(spider, sub_domains)
# extract failed threads cuz may be appear error so you will need nt kill script then you can complete from failed threads not from first file
                    # algorithm to solve problem of stuck threads if it stucked in any time to exit tool and start it again where the tool end
                    if len(sub_domains) > 1500:
                        succeed_threads_from_spider_222 = ''
                        while True:
                            succeed_threads_from_spider_to_test = len(succeed_threads_from_spider)
                            if len(failed_threads_from_spider) == len(sub_domains):
                                for i in range(8):
                                    time.sleep(10)

                                    if len(succeed_threads_from_spider) == succeed_threads_from_spider_222:
                                        time.sleep(int(args.time) / 8)
                                    else:
                                        succeed_threads_from_spider_222 = len(succeed_threads_from_spider)

                                        # extract failed threads
                                        failed_threads_from_spider_111 = set(failed_threads_from_spider)
                                        succeed_threads_from_spider_111 = set(succeed_threads_from_spider)
                                        file_contain_failed_threads_111 = open(args.o + "/failed_threads", "w")
                                        true_failed_111 = failed_threads_from_spider_111.difference(
                                            succeed_threads_from_spider_111)
                                        for thread in true_failed_111:
                                            file_contain_failed_threads_111.write(thread + "\n")
                                        dosent_requested_sub = sub_domains.difference(failed_threads_from_spider)
                                        for sub in dosent_requested_sub:
                                            file_contain_failed_threads_111.write(sub + "\n")
                                        file_contain_failed_threads_111.close()

                                time.sleep(5)
                                if len(succeed_threads_from_spider) == succeed_threads_from_spider_222:
                                    break
                            succeed_threads_from_spider_222 = succeed_threads_from_spider_to_test
                            # extract failed threads
                            failed_threads_from_spider_111 = set(failed_threads_from_spider)
                            succeed_threads_from_spider_111 = set(succeed_threads_from_spider)
                            file_contain_failed_threads_111 = open(args.o + "/failed_threads", "w")
                            true_failed_111 = failed_threads_from_spider_111.difference(succeed_threads_from_spider_111)
                            for thread in true_failed_111:
                                file_contain_failed_threads_111.write(thread + "\n")
                            dosent_requested_sub = sub_domains.difference(failed_threads_from_spider)
                            for sub in dosent_requested_sub:
                                file_contain_failed_threads_111.write(sub + "\n")
                            file_contain_failed_threads_111.close()
                            if args.time is None: args.time = 0
                            time.sleep(5)
                # extract failed threads from spider()
                file_contain_failed_threads = open(args.o + "/failed_threads", "w")
                failed_threads_from_spider = set(failed_threads_from_spider)
                succeed_threads_from_spider = set(succeed_threads_from_spider)
                true_failed = failed_threads_from_spider.difference(succeed_threads_from_spider)
                remove_duplicate(args.o + "/endpoint_from_crawl_website")
                for thread in true_failed:
                    file_contain_failed_threads.write(thread + "\n")


    #Wayback Machine
    elif args.f is not None and args.t is not None and args.archive is not None and args.o is not None or args.d is not None and args.o is not None and args.archive is not None:
        logo()
        os.system("mkdir " + str(args.o))
        subdomains = []
        try:
            file_contain_subdomains = open(args.f).readlines()
            for sub in file_contain_subdomains:
                subdomains.append(sub.strip())
        except:
            pass
        try:
            subdomains.append(str(args.d))
        except:
            pass
        print(bcolors.BOLD + "Extract endpoints from Wayback Machine" + bcolors.ENDC)
        if args.f is not None:
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.t)) as execution:
                execution.map(wayback_machine, subdomains)
            remove_duplicate(args.o + "/endpoints_from_archive")
            failed_threads_from_archive = set(failed_threads_from_archive)
            succeed_threads_from_archive = set(succeed_threads_from_archive)
            true_failed = failed_threads_from_archive.difference(succeed_threads_from_archive)
            file_contain_failed_threads = open(args.o + "/failed_threads_from_archive")
            for thread in true_failed:
                file_contain_failed_threads.write(thread + "\n")
        elif args.d is not None:
            wayback_machine(subdomains[0])
            remove_duplicate(args.o + "/endpoints_from_archive")

    #cert_sh()
    elif  args.d is not None and args.o is not None and args.crtsh is not None:
        logo()
        os.system("mkdir " + str(args.o))
        print(bcolors.BOLD + "Extract sub domains from cert.sh" + bcolors.ENDC)
        crt_sh(str(args.d))
        remove_duplicate(args.o + "/endpoints_from_crt_sh")

    else:

        parser.print_help()
        logo()
