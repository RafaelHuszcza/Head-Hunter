import os 
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('domain', help="The domain that we will search for")
args = parser.parse_args()



# Amass -> other pull sources -> massdns -> waybackurl -> httprobe -> portscan -> dirsearch -> screenshot 
# ^- workflow <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- redo 


def struct_folders(domain): #Return a string to the current recon path
    recon_path = '{}/recon/{}/{}'.format(os.getenv("HOME"),domain, datetime.today().strftime('%Y-%m-%d'))
    if not os.path.exists(recon_path):
        os.makedirs(recon_path)
        return recon_path
    else:
        print("Folder already exists, moving to the next step!")
        return recon_path
 
def run_amass(domain, path): # Need to implement -config and -asn if necessary
    try:
        os.system('amass enum -v -max-dns-queries 3000 -d {} -o {}/amass.txt'.format(domain, path))
        return '{}/amass.txt'.format(path)
    except:
        print("Couldn't query for domains using the amass")

def run_sublist3r(domain, path):
    try:
        os.system('python3 {}/tools/Sublist3r/sublist3r.py -d {} -t 50 -v -o {}/sublist3r.txt'.format(os.getenv("HOME"), domain, path))
        return '{}/sublist3r.txt'.format(path)
    except:
        print("Couldn't query for domains using sublist3r")

def run_assetfinder(domain, path):
    try:
        os.system('assetfinder --subs-only {} > {}/assetfinder.txt'.format(domain, path))
        return '{}/assetfinder.txt'.format(path)
    except:
        print("Couldn't query for domains using asset finder")

def unify_domains(amass_out, sublist3r_out, assetfinder_out, path):
    try:
        os.system('cat {} {} {} | anew {}/merged-domains.txt'.format(amass_out, sublist3r_out, assetfinder_out, path))
    except:
        print("Coudn't merge domains, stopping here!")

def run_nuclei(domains_list, path):
    os.system('nuclei -l {} -t {}/tools/nuclei/nuclei-templates/subdomain-takeover/'.format(domains_list, os.getenv("HOME")))


domain = args.domain
recon_folder = struct_folders(domain)

amass_output_file = run_amass(domain, recon_folder)
sublist3r_output_file = run_sublist3r(domain, recon_folder)
assetfinder_ouput_file = run_assetfinder(domain, recon_folder)

unify_domains(amass_output_file, sublist3r_output_file, assetfinder_ouput_file)
