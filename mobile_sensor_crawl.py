from automation import TaskManager, CommandSequence

# number of browsers to run in parallel
NUM_BROWSERS = 10


sites = []
csv_name = "top-1m.csv"
no_of_sites = 100000  # crawl 100K sites
for l in open(csv_name).readlines()[0:no_of_sites]:
    site = l.split(",")[-1].rstrip()
    sites.append(site)

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in xrange(NUM_BROWSERS):
    browser_params[i]['http_instrument'] = True  # Record HTTP Requests and Responses
    browser_params[i]['disable_flash'] = True  # Disable flash for all browsers
    browser_params[i]['js_instrument'] = True  # Enable JS instrumentation
    browser_params[i]['save_javascript'] = True  # save JS files
    browser_params[i]['headless'] = True  # headless
    browser_params[i]['trigger_sensor_events'] = True  # fake sensor events
    browser_params[i]['mobile_platform'] = "android"  # or "iphone"

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/openwpm_mobile_100k/'
manager_params['log_directory'] = '~/openwpm_mobile_100k/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for rank, site in enumerate(sites, 1):
    url = "http://%s" % site
    command_sequence = CommandSequence.CommandSequence(url, reset=True)

    # Start by visiting the page
    command_sequence.get(sleep=10, timeout=60)
    # command_sequence.save_screenshot('%d_%s_screenshot' % (rank, site))
    # dump_profile_cookies/dump_flash_cookies closes the current tab.
    command_sequence.dump_profile_cookies(120)

    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
