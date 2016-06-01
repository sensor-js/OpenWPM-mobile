from automation import TaskManager, CommandSequence

# The list of sites that we wish to crawl
NUM_BROWSERS = 15
# sites = ["https://securehomes.esat.kuleuven.be/~gacar/dev/test/sensor/"]
sites = []
csv_name = "top-1m.csv"
no_of_sites = 100000
for l in open(csv_name).readlines()[1:no_of_sites]:
    url = l.split(",")[-1].rstrip()
    sites.append("http://%s" % url)
#sites = ['http://www.example.com',
         #'http://www.princeton.edu',
         #'http://citp.princeton.edu/']

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
#for i in xrange(NUM_BROWSERS):
#    browser_params[i]['disable_flash'] = False #Enable flash for all three browsers
#    browser_params[i]['headless'] = False #Launch only browser 0 headless
    #browser_params[i]['ua_string'] = "Mozilla/5.0 (Android 6.0.1; Mobile; rv:46.0) Gecko/46.0 Firefox/46.0"

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/openwpm/'
manager_params['log_directory'] = '~/openwpm/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site)
    command_sequence.get(sleep=10, timeout=60)
    # command_sequence.dump_profile_cookies(120)
    manager.execute_command_sequence(command_sequence, index=None) # ** = synchronized browsers

# Shuts down the browsers and waits for the data to finish logging
manager.close()
