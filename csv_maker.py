import csv, re

def iocchecker(ip, writer1, filename, sege):
    """regex to decide what the IoC is"""
    ip_pat = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    ip_test = ip_pat.match(ip)

    md5_pat = re.compile(r"([a-fA-F\d]{32})$")
    md5_test = md5_pat.match(ip)

    sha_pat = re.compile(r"[0-9a-f]{5,40}$")
    sha_test = sha_pat.match(ip)

    two_pat = re.compile(r'[A-Fa-f0-9]{64}$')
    two_test = two_pat.match(ip)

    """If test matches write to CSV file"""
    if ip_test:
        writer1.writerow({'Indicator': ip, 'Description': filename, 'Type': 'IPv4 Address'})
        sege.writerow({'Use Rule': 'x', 'Source Host': filename, 'Source IP': ip, 'Source Port and Protocol': 'ANY',
                       'Destiniation Host': 'ANY', 'Destiniation IP': 'ANY',
                       'Destiniation Port and Protocol': 'ANY'})
        sege.writerow({'Use Rule': 'x', 'Source Host': filename, 'Source IP': 'ANY', 'Source Port and Protocol': 'ANY',
                       'Destiniation Host': 'ANY', 'Destiniation IP': ip, 'Destiniation Port and Protocol': 'ANY'})

    elif md5_test:
        writer1.writerow({'Indicator': ip, 'Type':'MD5', 'Threat Type': 'Malware Sample', 'Description': filename, 'Action': 'Request ban of hash in BIT9'})


    elif sha_test:
        writer1.writerow({'Indicator': ip, 'Type': 'SHA1', 'Threat Type': 'Malware Sample', 'Description': filename,
                          'Action': 'Request ban of hash in BIT9'})


    elif two_test:
        writer1.writerow({'Indicator': ip, 'Type':'SHA256', 'Threat Type': 'Malware Sample', 'Description': filename, 'Action': 'Request ban of hash in BIT9'})

    else:
        writer1.writerow({'Indicator': ip, 'Type': 'Domain', 'Threat Type': 'Malicious Domain' , 'Description':filename, 'Action': 'Firewall Block Requested'})

"""allowing bulk copy paste. fire when "Enter" is pressed."""
def multi_input():
    try:
        while True:
            data=input()
            if not data: break
            yield data
    except KeyboardInterrupt:
        return
"""Ask for file name to be put as description"""
filename = input(' Please type file description: ')

"""creats CRITS CSV"""
with open( filename + '.csv', 'w', newline='') as csvfile:
    fieldnames = ['Indicator', 'Type', 'Threat Type', 'Attack Type', 'Description', 'Campaign', 'Campaign Confidence', 'Confidence','Impact', 'Bucket List', 'Ticket', 'Action']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    """makes second CSV"""
    with open(filename + '1.csv', 'w', newline='') as csvfile:
        fieldnames = ['Use Rule', 'Source Host', 'Source IP', 'Source Port and Protocol', 'Destiniation Host', 'Destiniation IP',
                      'Destiniation Port and Protocol']
        sege = csv.DictWriter(csvfile, fieldnames=fieldnames)
        sege.writeheader()

        print('please input indicator: ')
        iocs = list(multi_input())
        print("Number of IoC's seen: {}".format(len(iocs)))

        for ioc in iocs:
            iocchecker(ioc, writer, filename, sege)
