""" Set prefs and load extensions in Firefox """
from ..Errors import BrowserConfigError
import shutil
import sys
import os

def privacy(browser_params, fp, root_dir, browser_profile_path):
    """
    Configure the privacy settings in Firefox. This includes:
    * DNT
    * Third-part cookie blocking
    * Tracking protection
    * Privacy extensions
    """

    # Turns on Do Not Track
    if browser_params['donottrack']:
        fp.set_preference("privacy.donottrackheader.enabled", True)
        fp.set_preference("privacy.donottrackheader.value", 1)

    # Sets the third party cookie setting
    if browser_params['tp_cookies'].lower() == 'never':
        fp.set_preference("network.cookie.cookieBehavior", 1)
    elif browser_params['tp_cookies'].lower() == 'from_visited':
        fp.set_preference("network.cookie.cookieBehavior", 3)
    else:  # always allow third party cookies
        fp.set_preference("network.cookie.cookieBehavior", 0)

    # Tracking Protection
    if browser_params['tracking-protection']:
        print "ERROR: Tracking Protection doesn't seem to work in Firefox 41 with selenium."
        print "       It does work in 42 Beta. This will be enabled once that lands in release."
        print "       Press Ctrl+C to exit"
        sys.exit(1)
        #fp.set_preference('privacy.trackingprotection.enabled', True)

    # Load Ghostery - Enable all blocking
    if browser_params['ghostery']:
        fp.add_extension(extension=os.path.join(root_dir,'firefox_extensions/ghostery/ghostery-5.4.10.xpi'))
        os.makedirs(browser_profile_path+'jetpack/firefox@ghostery.com/simple-storage/')
        src = os.path.join(root_dir,'firefox_extensions/ghostery/store.json') # settings - block all trackers/cookies
        dst = os.path.join(browser_profile_path,'jetpack/firefox@ghostery.com/simple-storage/store.json')
        shutil.copy(src,dst)

    # Enable HTTPS Everywhere
    if browser_params['https-everywhere']:
        fp.add_extension(extension=os.path.join(root_dir,'firefox_extensions/https_everywhere-5.1.0.xpi'))
        fp.set_preference("extensions.https_everywhere.firstrun_context_menu", True)
        fp.set_preference("extensions.https_everywhere.prefs_version", 1)
        fp.set_preference("extensions.https_everywhere.toolbar_hint_shown", True)
        fp.set_preference("extensions.https_everywhere._observatory.popup_shown", True)
        fp.set_preference("extensions.https_everywhere._observatory.clean_config", True)

    # Enable AdBlock Plus - Uses "Easy List" by default
    # "Allow some non-intrusive advertising" disabled
    if browser_params['adblock-plus']:
        fp.add_extension(extension=os.path.join(root_dir,'firefox_extensions/adblock_plus-2.7.xpi'))
        fp.set_preference('extensions.adblockplus.suppress_first_run_page', True)
        fp.set_preference('extensions.adblockplus.subscriptions_exceptionsurl', '')
        fp.set_preference('extensions.adblockplus.subscriptions_listurl', '')
        fp.set_preference('extensions.adblockplus.subscriptions_fallbackurl', '')
        fp.set_preference('extensions.adblockplus.subscriptions_antiadblockurl', '')
        fp.set_preference('extensions.adblockplus.suppress_first_run_page', True)
        fp.set_preference('extensions.adblockplus.notificationurl', '')

        # Force pre-loading so we don't allow some ads through
        fp.set_preference('extensions.adblockplus.please_kill_startup_performance', True)

        # Don't allow auto-update -- pull list from user location
        fp.set_preference('extensions.adblockplus.subscriptions_autoupdate', False)
        os.mkdir(browser_profile_path + 'adblockplus')
        try:
            list_loc = os.path.expanduser(browser_params['adblock-plus_list_location'])
            shutil.copy(os.path.join(list_loc,'patterns.ini'),
                    browser_profile_path+'adblockplus/')
            shutil.copy(os.path.join(list_loc,'elemhide.css'),
                    browser_profile_path+'adblockplus/')
        except (KeyError, IOError):
            raise BrowserConfigError(("In order to use AdBlock Plus, you must "
                "specify the location of an updated `patterns.ini` via "
                "`browser_params['adblock-plus_list_location']`. This can be "
                "generated with `utilities.platform_utils.fetch_adblockplus_list()`."))

def optimize_prefs(fp):
    """
    Disable various features and checks the browser will do on startup.
    Some of these (e.g. disabling the newtab page) are required to prevent
    extraneous data in the proxy.
    """
    # Startup / Speed
    fp.set_preference('browser.shell.checkDefaultBrowser', False)
    fp.set_preference("browser.slowStartup.notificationDisabled", True)
    fp.set_preference("browser.slowStartup.maxSamples", 0)
    fp.set_preference("browser.slowStartup.samples", 0)
    fp.set_preference('extensions.checkCompatibility.nightly', False)
    fp.set_preference('browser.rights.3.shown', True)
    fp.set_preference("reader.parse-on-load.enabled", False)
    fp.set_preference('browser.pagethumbnails.capturing_disabled', True)
    fp.set_preference('devtools.profiler.enabled', False)

    # Disable health reports / telemetry / crash reports
    fp.set_preference("datareporting.policy.dataSubmissionEnabled", False) #FF41+ Master Switch
    fp.set_preference('datareporting.healthreport.uploadEnabled', False)
    fp.set_preference("datareporting.healthreport.service.enabled", False)
    fp.set_preference('toolkit.telemetry.enabled', False)
    fp.set_preference("toolkit.telemetry.unified", False)
    fp.set_preference("breakpad.reportURL", "")
    fp.set_preference("dom.ipc.plugins.flash.subprocess.crashreporter.enabled", False)

    # Predictive Actions / Prefetch
    fp.set_preference('network.seer.enabled', False)
    fp.set_preference('network.dns.disablePrefetch', True)
    fp.set_preference('network.prefetch-next', False)
    fp.set_preference("browser.search.suggest.enabled", False)
    fp.set_preference("network.http.speculative-parallel-limit", 0)
    fp.set_preference("keyword.enabled", False) # location bar using search

    # Disable pinging Mozilla for geoip
    fp.set_preference('browser.search.geoip.url', '')
    fp.set_preference("browser.search.countryCode", "US")
    fp.set_preference("browser.search.region", "US")

    # Disable pinging Mozilla for geo-specific search
    fp.set_preference("browser.search.geoSpecificDefaults", False)
    fp.set_preference("browser.search.geoSpecificDefaults.url", "")

    # Disable auto-updating
    fp.set_preference("app.update.enabled", False) # browser
    fp.set_preference("app.update.url", "") # browser
    fp.set_preference("media.gmp-manager.url", "") # OpenH264 Codec
    fp.set_preference("browser.search.update", False) # search
    fp.set_preference("extensions.update.enabled", False) # extensions
    fp.set_preference("extensions.update.autoUpdateDefault", False) # addons
    fp.set_preference("extensions.getAddons.cache.enabled", False)
    fp.set_preference("lightweightThemes.update.enabled", False) # Personas
    fp.set_preference("browser.safebrowsing.provider.mozilla.updateURL", "") # Safebrowsing
    fp.set_preference("browser.safebrowsing.provider.mozilla.lists", "") # Tracking Protection Lists

    # Disable Safebrowsing
    fp.set_preference("browser.safebrowsing.enabled", False)
    fp.set_preference("browser.safebrowsing.malware.enabled", False)
    fp.set_preference("browser.safebrowsing.downloads.enabled", False)
    fp.set_preference("browser.safebrowsing.downloads.remote.enabled", False)
    fp.set_preference('security.OCSP.enabled', 0)

    # Disable Experiments
    fp.set_preference("experiments.enabled", False)
    fp.set_preference("experiments.manifest.uri", "")
    fp.set_preference("experiments.supported", False)
    fp.set_preference("experiments.activeExperiment", False)
    fp.set_preference("network.allow-experiments", False)

    # Disable pinging Mozilla for newtab
    fp.set_preference("browser.newtabpage.directory.ping", "")
    fp.set_preference("browser.newtabpage.directory.source", "")
    fp.set_preference("browser.newtabpage.enabled", False)
    fp.set_preference("browser.newtabpage.enhanced", False)
    fp.set_preference("browser.newtabpage.introShown", True)

    # Disable Pocket
    fp.set_preference("browser.pocket.enabled", False)

    # Disable Hello
    fp.set_preference("loop.enabled", False)

def set_mobile_prefs(fp, platform):
    """
    Set all the prefs related to mobile firefox.
    All preferences set based on values found at:
    mobile/android/app/mobile.js ESR45 branch.
    Version adapted assumes high memory device, with
    private browsing enabled and release build.
    MOZ_PKG_SPECIAL -> False
    NIGHTLY_BUILD   -> False
    RELEASE_BUILD   -> True
    MOZ_ANDROID_APZ -> True
    MOZ_UPDATER     -> False
    """

    if platform == "android":
        fp.set_preference("window.navigator.platform", "")
        fp.set_preference("window.navigator.appVersion", "")
    elif platform == "iphone":
        fp.set_preference("window.navigator.platform", "")
        fp.set_preference("window.navigator.appVersion", "")

    # Disable Plugins, fixes mimeTypes as well.
    fp.set_preference("plugin.disable", True)

    # Setting window screen depth.
    fp.set_preference("window.screen.colorDepth", 32)
    fp.set_preference("window.screen.pixelDepth", 32)

    # For browser.xml binding
    # cacheRatio* is a ratio that determines the amount of pixels to cache. The
    # ratio is multiplied by the viewport width or height to get the displayports
    # width or height, respectively.
    # (divide integer value by 1000 to get the ratio)
    # For instance: cachePercentageWidth is 1500
    #               viewport height is 500
    #               => display port height will be 500 * 1.5 = 750
    fp.set_preference("toolkit.browser.cacheRatioWidth", 2000)
    fp.set_preference("toolkit.browser.cacheRatioHeight", 3000)

    # How long before a content view (a handle to a remote scrollable object)
    # expires.
    fp.set_preference("toolkit.browser.contentViewExpire", 3000)

    fp.set_preference("toolkit.defaultChromeURI", "chrome://browser/content/browser.xul")
    fp.set_preference("browser.chromeURL", "chrome://browser/content/")

    # If a tab has not been active for this long (seconds), then it may be
    # turned into a zombie tab to preemptively free up memory. -1 disables time-based
    # expiration (but low-memory conditions may still require the tab to be zombified).
    fp.set_preference("browser.tabs.expireTime", 900)

    # From libpref/src/init/all.js, extended to allow a slightly wider zoom range.
    fp.set_preference("zoom.minPercent", 20)
    fp.set_preference("zoom.maxPercent", 400)
    fp.set_preference("toolkit.zoomManager.zoomValues", ".2,.3,.5,.67,.8,.9,1,1.1,1.2,1.33,1.5,1.7,2,2.4,3,4")

    # Mobile will use faster, less durable mode.
    fp.set_preference("toolkit.storage.synchronous", 0)

    fp.set_preference("browser.viewport.desktopWidth", 980)
    # The default fallback zoom level to render pages at. Set to -1 to fit page; otherwise
    # the value is divided by 1000 and clamped to hard-coded min/max scale values.
    fp.set_preference("browser.viewport.defaultZoom", -1)

    # Show/Hide scrollbars when active/inactive
    fp.set_preference("ui.showHideScrollbars", 1)
    fp.set_preference("ui.useOverlayScrollbars", 1)
    fp.set_preference("ui.scrollbarFadeBeginDelay", 450)
    fp.set_preference("ui.scrollbarFadeDuration", 0)

    # turn off the caret blink after 10 cycles */
    fp.set_preference("ui.caretBlinkCount", 10)

    # cache prefs */
    fp.set_preference("browser.cache.disk.enable", True)
    fp.set_preference("browser.cache.disk.capacity", 20480)     # kilobytes
    fp.set_preference("browser.cache.disk.max_entry_size", 4096)     # kilobytes
    fp.set_preference("browser.cache.disk.smart_size.enabled", True)
    fp.set_preference("browser.cache.disk.smart_size.first_run", True)

    fp.set_preference("browser.cache.memory.enable", True)
    fp.set_preference("browser.cache.memory.capacity", 1024)     # kilobytes

    fp.set_preference("browser.cache.memory_limit", 5120)     # 5 MB

    # image cache prefs */
    fp.set_preference("image.cache.size", 1048576)     # bytes

    # offline cache prefs */
    fp.set_preference("browser.offline-apps.notify", True)
    fp.set_preference("browser.cache.offline.enable", True)
    fp.set_preference("browser.cache.offline.capacity", 5120)     # kilobytes
    fp.set_preference("offline-apps.quota.warn", 1024)     # kilobytes

    # cache compression turned off for now - see bug #715198
    fp.set_preference("browser.cache.compression_level", 0)

    # disable some protocol warnings */
    fp.set_preference("network.protocol-handler.warn-external.tel", False)
    fp.set_preference("network.protocol-handler.warn-external.sms", False)
    fp.set_preference("network.protocol-handler.warn-external.mailto", False)
    fp.set_preference("network.protocol-handler.warn-external.vnd.youtube", False)

    # http prefs */
    fp.set_preference("network.http.pipelining", True)
    fp.set_preference("network.http.pipelining.ssl", True)
    fp.set_preference("network.http.proxy.pipelining", True)
    fp.set_preference("network.http.pipelining.maxrequests" , 6)
    fp.set_preference("network.http.keep-alive.timeout", 109)
    fp.set_preference("network.http.max-connections", 20)
    fp.set_preference("network.http.max-persistent-connections-per-server", 6)
    fp.set_preference("network.http.max-persistent-connections-per-proxy", 20)

    # spdy
    fp.set_preference("network.http.spdy.push-allowance", 32768)

    # See bug 545869 for details on why these are set the way they are
    fp.set_preference("network.buffer.cache.count", 24)
    fp.set_preference("network.buffer.cache.size",  16384)

    # predictive actions
    fp.set_preference("network.predictor.enabled", False)
    fp.set_preference("network.predictor.max-db-size", 2097152)     # bytes
    fp.set_preference("network.predictor.preserve", 50)     # percentage of predictor data to keep when cleaning up

    # history max results display */
    fp.set_preference("browser.display.history.maxresults", 100)

    # How many times should have passed before the remote tabs list is refreshed */
    fp.set_preference("browser.display.remotetabs.timeout", 10)

    # session history */
    fp.set_preference("browser.sessionhistory.max_total_viewers", 1)
    fp.set_preference("browser.sessionhistory.max_entries", 50)
    fp.set_preference("browser.sessionhistory.contentViewerTimeout", 360)

    # session store */
    fp.set_preference("browser.sessionstore.resume_session_once", False)
    # webdriver pref
    # fp.set_preference("browser.sessionstore.resume_from_crash", True)
    fp.set_preference("browser.sessionstore.interval", 10000)     # milliseconds
    fp.set_preference("browser.sessionstore.max_tabs_undo", 5)
    fp.set_preference("browser.sessionstore.max_resumed_crashes", 1)
    fp.set_preference("browser.sessionstore.recent_crashes", 0)
    fp.set_preference("browser.sessionstore.privacy_level", 0)     # saving data: 0 = all, 1 = unencrypted sites, 2 = never

    # these should help performance */
    fp.set_preference("mozilla.widget.force-24bpp", True)
    fp.set_preference("mozilla.widget.use-buffer-pixmap", True)
    fp.set_preference("mozilla.widget.disable-native-theme", True)
    fp.set_preference("layout.reflow.synthMouseMove", False)
    fp.set_preference("layout.css.report_errors", False)

    # download manager (don't show the window or alert) */
    fp.set_preference("browser.download.useDownloadDir", True)
    fp.set_preference("browser.download.folderList", 1)     # Default to ~/Downloads
    fp.set_preference("browser.download.manager.showAlertOnComplete", False)
    fp.set_preference("browser.download.manager.showAlertInterval", 2000)
    fp.set_preference("browser.download.manager.retention", 2)
    # webdriver pref
    # fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.manager.closeWhenDone", True)
    fp.set_preference("browser.download.manager.openDelay", 0)
    fp.set_preference("browser.download.manager.focusWhenStarting", False)
    fp.set_preference("browser.download.manager.flashCount", 2)
    fp.set_preference("browser.download.manager.displayedHistoryDays", 7)
    fp.set_preference("browser.download.manager.addToRecentDocs", True)

    # download helper */
    fp.set_preference("browser.helperApps.deleteTempFileOnExit", False)

    # password manager */
    # webdriver pref
    # fp.set_preference("signon.rememberSignons", True)
    fp.set_preference("signon.expireMasterPassword", False)
    fp.set_preference("signon.debug", False)

    # form helper (scroll to and optionally zoom into editable fields)  */
    fp.set_preference("formhelper.mode", 2)      # 0 = disabled, 1 = enabled, 2 = dynamic depending on screen size
    fp.set_preference("formhelper.autozoom", True)

    # find helper */
    fp.set_preference("findhelper.autozoom", True)

    # autocomplete */
    fp.set_preference("browser.formfill.enable", True)

    # spellcheck */
    fp.set_preference("layout.spellcheckDefault", 0)

    # new html5 forms */
    fp.set_preference("dom.experimental_forms", True)
    fp.set_preference("dom.forms.number", True)

    # extension manager and xpinstall */
    fp.set_preference("xpinstall.whitelist.directRequest", False)
    fp.set_preference("xpinstall.whitelist.fileRequest", False)
    fp.set_preference("xpinstall.whitelist.add", "https://addons.mozilla.org")
    fp.set_preference("xpinstall.whitelist.add.180", "https://marketplace.firefox.com")

    # webdriver pref
    # fp.set_preference("xpinstall.signatures.required", False)

    fp.set_preference("extensions.enabledScopes", 1)
    fp.set_preference("extensions.autoupdate.enabled", False)
    fp.set_preference("extensions.autoupdate.interval", 86400)
    # webdriver pref
    # fp.set_preference("extensions.update.enabled", True)
    fp.set_preference("extensions.update.interval", 86400)
    fp.set_preference("extensions.dss.enabled", False)
    fp.set_preference("extensions.dss.switchPending", False)
    fp.set_preference("extensions.ignoreMTimeChanges", False)
    # webdriver pref
    # fp.set_preference("extensions.logging.enabled", False)
    fp.set_preference("extensions.hideInstallButton", True)
    fp.set_preference("extensions.showMismatchUI", False)
    fp.set_preference("extensions.hideUpdateButton", False)
    fp.set_preference("extensions.strictCompatibility", False)
    fp.set_preference("extensions.minCompatibleAppVersion", "11.0")

    fp.set_preference("extensions.update.url", "https://versioncheck.addons.mozilla.org/update/VersionCheck.php?reqVersion=%REQ_VERSION%&id=%ITEM_ID%&version=%ITEM_VERSION%&maxAppVersion=%ITEM_MAXAPPVERSION%&status=%ITEM_STATUS%&appID=%APP_ID%&appVersion=%APP_VERSION%&appOS=%APP_OS%&appABI=%APP_ABI%&locale=%APP_LOCALE%&currentAppVersion=%CURRENT_APP_VERSION%&updateType=%UPDATE_TYPE%&compatMode=%COMPATIBILITY_MODE%")
    fp.set_preference("extensions.update.background.url", "https://versioncheck-bg.addons.mozilla.org/update/VersionCheck.php?reqVersion=%REQ_VERSION%&id=%ITEM_ID%&version=%ITEM_VERSION%&maxAppVersion=%ITEM_MAXAPPVERSION%&status=%ITEM_STATUS%&appID=%APP_ID%&appVersion=%APP_VERSION%&appOS=%APP_OS%&appABI=%APP_ABI%&locale=%APP_LOCALE%&currentAppVersion=%CURRENT_APP_VERSION%&updateType=%UPDATE_TYPE%&compatMode=%COMPATIBILITY_MODE%")

    fp.set_preference("extensions.hotfix.id", "firefox-android-hotfix@mozilla.org")
    fp.set_preference("extensions.hotfix.cert.checkAttributes", True)
    fp.set_preference("extensions.hotfix.certs.1.sha1Fingerprint", "91:53:98:0C:C1:86:DF:47:8F:35:22:9E:11:C9:A7:31:04:49:A1:AA")

    # preferences for the Get Add-ons pane */
    fp.set_preference("extensions.getAddons.cache.enabled", True)
    fp.set_preference("extensions.getAddons.maxResults", 15)
    fp.set_preference("extensions.getAddons.recommended.browseURL", "https://addons.mozilla.org/%LOCALE%/android/recommended/")
    fp.set_preference("extensions.getAddons.recommended.url", "https://services.addons.mozilla.org/%LOCALE%/android/api/%API_VERSION%/list/featured/all/%MAX_RESULTS%/%OS%/%VERSION%")
    fp.set_preference("extensions.getAddons.search.browseURL", "https://addons.mozilla.org/%LOCALE%/android/search?q=%TERMS%&platform=%OS%&appver=%VERSION%")
    fp.set_preference("extensions.getAddons.search.url", "https://services.addons.mozilla.org/%LOCALE%/android/api/%API_VERSION%/search/%TERMS%/all/%MAX_RESULTS%/%OS%/%VERSION%/%COMPATIBILITY_MODE%")
    fp.set_preference("extensions.getAddons.browseAddons", "https://addons.mozilla.org/%LOCALE%/android/")
    fp.set_preference("extensions.getAddons.get.url", "https://services.addons.mozilla.org/%LOCALE%/android/api/%API_VERSION%/search/guid:%IDS%?src=mobile&appOS=%OS%&appVersion=%VERSION%")
    fp.set_preference("extensions.getAddons.getWithPerformance.url", "https://services.addons.mozilla.org/%LOCALE%/android/api/%API_VERSION%/search/guid:%IDS%?src=mobile&appOS=%OS%&appVersion=%VERSION%&tMain=%TIME_MAIN%&tFirstPaint=%TIME_FIRST_PAINT%&tSessionRestored=%TIME_SESSION_RESTORED%")

    # preference for the locale picker */
    fp.set_preference("extensions.getLocales.get.url", "")
    fp.set_preference("extensions.compatability.locales.buildid", "0")

    # blocklist preferences */
    # webdriver pref
    # fp.set_preference("extensions.blocklist.enabled", True)
    # OneCRL freshness checking depends on this value, so if you change it,
    # please also update security.onecrl.maximum_staleness_in_seconds.
    fp.set_preference("extensions.blocklist.interval", 86400)
    fp.set_preference("extensions.blocklist.url", "https://blocklist.addons.mozilla.org/blocklist/3/%APP_ID%/%APP_VERSION%/%PRODUCT%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/%PING_COUNT%/%TOTAL_PING_COUNT%/%DAYS_SINCE_LAST_PING%/")
    fp.set_preference("extensions.blocklist.detailsURL", "https://www.mozilla.com/%LOCALE%/blocklist/")

    # Don't let XPIProvider install distribution add-ons; we do our own thing on mobile. */
    fp.set_preference("extensions.installDistroAddons", False)

    # block popups by default, and notify the user about blocked popups */
    # webdriver pref
    # fp.set_preference("dom.disable_open_during_load", True)
    fp.set_preference("privacy.popups.showBrowserMessage", True)

    # disable opening windows with the dialog feature */
    fp.set_preference("dom.disable_window_open_dialog_feature", True)
    fp.set_preference("dom.disable_window_showModalDialog", True)
    fp.set_preference("dom.disable_window_print", True)
    fp.set_preference("dom.disable_window_find", True)

    fp.set_preference("keyword.enabled", True)
    fp.set_preference("browser.fixup.domainwhitelist.localhost", True)

    fp.set_preference("accessibility.typeaheadfind", False)
    fp.set_preference("accessibility.typeaheadfind.timeout", 5000)
    fp.set_preference("accessibility.typeaheadfind.flashBar", 1)
    fp.set_preference("accessibility.typeaheadfind.linksonly", False)
    fp.set_preference("accessibility.typeaheadfind.casesensitive", 0)
    fp.set_preference("accessibility.browsewithcaret_shortcut.enabled", False)

    # Whether the character encoding menu is under the main Firefox button. This
    # preference is a string so that localizers can alter it.
    fp.set_preference("browser.menu.showCharacterEncoding", "chrome://browser/locale/browser.properties")

    # pointer to the default engine name
    fp.set_preference("browser.search.defaultenginename", "chrome://browser/locale/region.properties")
    # maximum number of search suggestions, as a string because the search service expects a string pref
    fp.set_preference("browser.search.param.maxSuggestions", "4")
    # SSL error page behaviour
    fp.set_preference("browser.ssl_override_behavior", 2)
    fp.set_preference("browser.xul.error_pages.expert_bad_cert", False)

    # ordering of search engines in the engine list.
    fp.set_preference("browser.search.order.1", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.search.order.2", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.search.order.3", "chrome://browser/locale/region.properties")

    # Market-specific search defaults
    fp.set_preference("browser.search.geoSpecificDefaults", True)
    fp.set_preference("browser.search.geoSpecificDefaults.url", "https://search.services.mozilla.com/1/%APP%/%VERSION%/%CHANNEL%/%LOCALE%/%REGION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%")

    # US specific default (used as a fallback if the geoSpecificDefaults request fails).
    fp.set_preference("browser.search.defaultenginename.US", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.search.order.US.1", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.search.order.US.2", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.search.order.US.3", "chrome://browser/locale/region.properties")

    # disable updating
    # webdriver pref
    # fp.set_preference("browser.search.update", False)

    # enable tracking protection for private browsing
    fp.set_preference("privacy.trackingprotection.pbmode.enabled", True)

    # disable search suggestions by default
    fp.set_preference("browser.search.suggest.enabled", False)
    fp.set_preference("browser.search.suggest.prompted", False)

    # tell the search service that we don't really expose the "current engine"
    fp.set_preference("browser.search.noCurrentEngine", True)

    # Control media casting & mirroring features
    fp.set_preference("browser.casting.enabled", True)
    # Chromecast mirroring is broken (bug 1131084)
    fp.set_preference("browser.mirroring.enabled", False)

    # Enable sparse localization by setting a few package locale overrides
    fp.set_preference("chrome.override_package.global", "browser")
    fp.set_preference("chrome.override_package.mozapps", "browser")
    fp.set_preference("chrome.override_package.passwordmgr", "browser")

    # enable xul error pages
    fp.set_preference("browser.xul.error_pages.enabled", True)

    # disable color management
    fp.set_preference("gfx.color_management.mode", 0)

    # 0=fixed margin, 1=velocity bias, 2=dynamic resolution, 3=no margins, 4=prediction bias
    fp.set_preference("gfx.displayport.strategy", 1)

    # all of the following displayport strategy prefs will be divided by 1000
    # to obtain some multiplier which is then used in the strategy.
    # fixed margin strategy options
    fp.set_preference("gfx.displayport.strategy_fm.multiplier", -1)     # displayport dimension multiplier
    fp.set_preference("gfx.displayport.strategy_fm.danger_x", -1)     # danger zone on x-axis when multiplied by viewport width
    fp.set_preference("gfx.displayport.strategy_fm.danger_y", -1)     # danger zone on y-axis when multiplied by viewport height

    # velocity bias strategy options
    fp.set_preference("gfx.displayport.strategy_vb.multiplier", -1)     # displayport dimension multiplier
    fp.set_preference("gfx.displayport.strategy_vb.threshold", -1)     # velocity threshold in inches/frame
    fp.set_preference("gfx.displayport.strategy_vb.reverse_buffer", -1)     # fraction of buffer to keep in reverse direction from scroll
    fp.set_preference("gfx.displayport.strategy_vb.danger_x_base", -1)     # danger zone on x-axis when multiplied by viewport width
    fp.set_preference("gfx.displayport.strategy_vb.danger_y_base", -1)     # danger zone on y-axis when multiplied by viewport height
    fp.set_preference("gfx.displayport.strategy_vb.danger_x_incr", -1)     # additional danger zone on x-axis when multiplied by viewport width and velocity
    fp.set_preference("gfx.displayport.strategy_vb.danger_y_incr", -1)     # additional danger zone on y-axis when multiplied by viewport height and velocity

    # prediction bias strategy options
    fp.set_preference("gfx.displayport.strategy_pb.threshold", -1)     # velocity threshold in inches/frame

    # Allow 24-bit colour when the hardware supports it
    fp.set_preference("gfx.android.rgb16.force", False)

    # Allow GLContexts to be attached/detached from SurfaceTextures
    fp.set_preference("gfx.SurfaceTexture.detach.enabled", True)

    # don't allow JS to move and resize existing windows
    fp.set_preference("dom.disable_window_move_resize", True)

    # prevent click image resizing for nsImageDocument
    fp.set_preference("browser.enable_click_image_resizing", False)

    """
    Disabling prefs based on selenium webdriver prefs
    # open in tab preferences
    # 0=default window, 1=current window/tab, 2=new window, 3=new tab in most window
    fp.set_preference("browser.link.open_external", 3)
    fp.set_preference("browser.link.open_newwindow", 3)
    # 0=force all new windows to tabs, 1=don't force, 2=only force those with no features set
    fp.set_preference("browser.link.open_newwindow.restriction", 0)
    """
    # show images option
    # 0=never, 1=always, 2=cellular-only
    fp.set_preference("browser.image_blocking", 1)

    # controls which bits of private data to clear. by default we clear them all.
    fp.set_preference("privacy.item.cache", True)
    fp.set_preference("privacy.item.cookies", True)
    fp.set_preference("privacy.item.offlineApps", True)
    fp.set_preference("privacy.item.history", True)
    fp.set_preference("privacy.item.searchHistory", True)
    fp.set_preference("privacy.item.formdata", True)
    fp.set_preference("privacy.item.downloads", True)
    fp.set_preference("privacy.item.passwords", True)
    fp.set_preference("privacy.item.sessions", True)
    fp.set_preference("privacy.item.geolocation", True)
    fp.set_preference("privacy.item.siteSettings", True)
    fp.set_preference("privacy.item.syncAccount", True)

    # enable geo
    fp.set_preference("geo.enabled", True)

    # content sink control -- controls responsiveness during page load
    # see https://bugzilla.mozilla.org/show_bug.cgi?id=481566#c9
    #    fp.set_preference("content.sink.enable_perf_mode",  2)     # 0 - switch, 1 - interactive, 2 - perf
    #    fp.set_preference("content.sink.pending_event_mode", 0)
    #    fp.set_preference("content.sink.perf_deflect_count", 1000000)
    #    fp.set_preference("content.sink.perf_parse_time", 50000000)

    # Disable the JS engine's gc on memory pressure, since we do one in the mobile
    # browser (bug 669346).
    fp.set_preference("javascript.options.gc_on_memory_pressure", False)

    fp.set_preference("javascript.options.mem.high_water_mark", 32)

    # webdriver pref
    # fp.set_preference("dom.max_chrome_script_run_time", 0)     # disable slow script dialog for chrome
    # fp.set_preference("dom.max_script_run_time", 20)

    # JS error console
    # webdriver pref
    # fp.set_preference("devtools.errorconsole.enabled", False)
    # Absolute path to the devtools unix domain socket file used
    # to communicate with a usb cable via adb forward.
    fp.set_preference("devtools.debugger.unix-domain-socket", "/data/data/@ANDROID_PACKAGE_NAME@/firefox-debugger-socket")

    fp.set_preference("devtools.remote.usb.enabled", False)
    fp.set_preference("devtools.remote.wifi.enabled", False)

    fp.set_preference("font.size.inflation.minTwips", 0)

    # When True, zooming will be enabled on all sites, even ones that declare user-scalable=no.
    fp.set_preference("browser.ui.zoom.force-user-scalable", False)

    # When removing this Nightly flag, also remember to remove the flags surrounding this feature
    # in GeckoPreferences and BrowserApp (see bug 1245930).
    fp.set_preference("ui.zoomedview.enabled", False)
    fp.set_preference("ui.zoomedview.keepLimitSize", 16)     # value in layer pixels, used to not keep the large elements in the cluster list (Bug 1191041)
    fp.set_preference("ui.zoomedview.limitReadableSize", 8)     # value in layer pixels
    fp.set_preference("ui.zoomedview.defaultZoomFactor", 2)
    fp.set_preference("ui.zoomedview.simplified", True)     # Do not display all the zoomed view controls, do not use size heurisistic

    fp.set_preference("ui.touch.radius.enabled", False)
    fp.set_preference("ui.touch.radius.leftmm", 3)
    fp.set_preference("ui.touch.radius.topmm", 5)
    fp.set_preference("ui.touch.radius.rightmm", 3)
    fp.set_preference("ui.touch.radius.bottommm", 2)
    fp.set_preference("ui.touch.radius.visitedWeight", 120)

    fp.set_preference("ui.mouse.radius.enabled", False)
    fp.set_preference("ui.mouse.radius.leftmm", 3)
    fp.set_preference("ui.mouse.radius.topmm", 5)
    fp.set_preference("ui.mouse.radius.rightmm", 3)
    fp.set_preference("ui.mouse.radius.bottommm", 2)
    fp.set_preference("ui.mouse.radius.visitedWeight", 120)
    fp.set_preference("ui.mouse.radius.reposition", True)

    # The percentage of the screen that needs to be scrolled before toolbar
    # manipulation is allowed.
    fp.set_preference("browser.ui.scroll-toolbar-threshold", 10)

    # Maximum distance from the point where the user pressed where we still
    # look for text to select
    fp.set_preference("browser.ui.selection.distance", 250)

    # plugins
    fp.set_preference("plugin.disable", False)
    fp.set_preference("dom.ipc.plugins.enabled", False)

    # This pref isn't actually used anymore, but we're leaving this here to avoid changing
    # the default so that we can migrate a user-set pref. See bug 885357.
    fp.set_preference("plugins.click_to_play", True)
    # The default value for nsIPluginTag.enabledState (STATE_CLICKTOPLAY = 1)
    fp.set_preference("plugin.default.state", 1)

    # product URLs
    # The breakpad report server to link to in about:crashes
    fp.set_preference("breakpad.reportURL", "https://crash-stats.mozilla.com/report/index/")
    fp.set_preference("app.support.baseURL", "http://support.mozilla.org/1/mobile/%VERSION%/%OS%/%LOCALE%/")
    # Used to submit data to input from about:feedback
    fp.set_preference("app.feedback.postURL", "https://input.mozilla.org/api/v1/feedback/")
    fp.set_preference("app.privacyURL", "https://www.mozilla.org/privacy/firefox/")
    fp.set_preference("app.creditsURL", "http://www.mozilla.org/credits/")
    fp.set_preference("app.channelURL", "http://www.mozilla.org/%LOCALE%/firefox/channel/")
    fp.set_preference("app.releaseNotesURL", "http://www.mozilla.com/%LOCALE%/mobile/%VERSION%/releasenotes/")
    fp.set_preference("app.faqURL", "https://support.mozilla.org/1/mobile/%VERSION%/%OS%/%LOCALE%/faq")

    # Name of alternate about: page for certificate errors (when undefined, defaults to about:neterror)
    fp.set_preference("security.alternate_certificate_error_page", "certerror")

    fp.set_preference("security.warn_viewing_mixed", False)     # Warning is disabled.  See Bug 616712.

    # Block insecure active content on https pages
    fp.set_preference("security.mixed_content.block_active_content", True)

    # Enable pinning
    fp.set_preference("security.cert_pinning.enforcement_level", 1)

    # Allow SHA-1 certificates
    fp.set_preference("security.pki.sha1_enforcement_level", 0)

    # Required blocklist freshness for OneCRL OCSP bypass
    # (default is 1.25x extensions.blocklist.interval, or 30 hours)
    fp.set_preference("security.onecrl.maximum_staleness_in_seconds", 108000)

    # Only fetch OCSP for EV certificates
    fp.set_preference("security.OCSP.enabled", 2)

    # Override some named colors to avoid inverse OS themes
    fp.set_preference("ui.-moz-dialog", "#efebe7")
    fp.set_preference("ui.-moz-dialogtext", "#101010")
    fp.set_preference("ui.-moz-field", "#fff")
    fp.set_preference("ui.-moz-fieldtext", "#1a1a1a")
    fp.set_preference("ui.-moz-buttonhoverface", "#f3f0ed")
    fp.set_preference("ui.-moz-buttonhovertext", "#101010")
    fp.set_preference("ui.-moz-combobox", "#fff")
    fp.set_preference("ui.-moz-comboboxtext", "#101010")
    fp.set_preference("ui.buttonface", "#ece7e2")
    fp.set_preference("ui.buttonhighlight", "#fff")
    fp.set_preference("ui.buttonshadow", "#aea194")
    fp.set_preference("ui.buttontext", "#101010")
    fp.set_preference("ui.captiontext", "#101010")
    fp.set_preference("ui.graytext", "#b1a598")
    fp.set_preference("ui.highlight", "#fad184")
    fp.set_preference("ui.highlighttext", "#1a1a1a")
    fp.set_preference("ui.infobackground", "#f5f5b5")
    fp.set_preference("ui.infotext", "#000")
    fp.set_preference("ui.menu", "#f7f5f3")
    fp.set_preference("ui.menutext", "#101010")
    fp.set_preference("ui.threeddarkshadow", "#000")
    fp.set_preference("ui.threedface", "#ece7e2")
    fp.set_preference("ui.threedhighlight", "#fff")
    fp.set_preference("ui.threedlightshadow", "#ece7e2")
    fp.set_preference("ui.threedshadow", "#aea194")
    fp.set_preference("ui.window", "#efebe7")
    fp.set_preference("ui.windowtext", "#101010")
    fp.set_preference("ui.windowframe", "#efebe7")

    # prefs used by the update timer system (including blocklist pings)
    fp.set_preference("app.update.timerFirstInterval", 30000)     # milliseconds
    fp.set_preference("app.update.timerMinimumDelay", 30)     # seconds

    # used by update service to decide whether or not to
    # automatically download an update
    fp.set_preference("app.update.autodownload", "wifi")
    fp.set_preference("app.update.url.android", "https://aus5.mozilla.org/update/4/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/%MOZ_VERSION%/update.xml")

    # prefs used specifically for updating the app
    # webdriver pref
    # fp.set_preference("app.update.enabled", False)
    fp.set_preference("app.update.channel", "@MOZ_UPDATE_CHANNEL@")

    # replace newlines with spaces on paste into single-line text boxes
    fp.set_preference("editor.singleLine.pasteNewlines", 2)

    # threshold where a tap becomes a drag, in 1/240" reference pixels
    # The names of the preferences are to be in sync with EventStateManager.cpp
    fp.set_preference("ui.dragThresholdX", 25)
    fp.set_preference("ui.dragThresholdY", 25)

    fp.set_preference("layers.acceleration.disabled", False)
    fp.set_preference("layers.offmainthreadcomposition.enabled", True)
    fp.set_preference("layers.async-video.enabled", True)

    fp.set_preference("layers.async-pan-zoom.enabled", True)
    # APZ physics settings, copied from B2G
    fp.set_preference("apz.axis_lock.mode", 2)     # Use "sticky" axis locking
    fp.set_preference("apz.fling_curve_function_x1", "0.41")
    fp.set_preference("apz.fling_curve_function_y1", "0.0")
    fp.set_preference("apz.fling_curve_function_x2", "0.80")
    fp.set_preference("apz.fling_curve_function_y2", "1.0")
    fp.set_preference("apz.fling_curve_threshold_inches_per_ms", "0.01")
    fp.set_preference("apz.fling_friction", "0.0019")
    fp.set_preference("apz.max_velocity_inches_per_ms", "0.07")

    fp.set_preference("layers.progressive-paint", True)
    fp.set_preference("layers.low-precision-buffer", True)
    fp.set_preference("layers.low-precision-resolution", "0.25")
    fp.set_preference("layers.low-precision-opacity", "1.0")
    # We want to limit layers for two reasons:
    # 1) We can't scroll smoothly if we have to many draw calls
    # 2) Pages that have too many layers consume too much memory and crash.
    # By limiting the number of layers on mobile we're making the main thread
    # work harder keep scrolling smooth and memory low.
    fp.set_preference("layers.max-active", 20)

    fp.set_preference("notification.feature.enabled", True)
    fp.set_preference("dom.webnotifications.enabled", True)

    # prevent tooltips from showing up
    fp.set_preference("browser.chrome.toolbar_tips", False)

    # prevent video elements from preloading too much data
    fp.set_preference("media.preload.default", 1)     # default to preload none
    fp.set_preference("media.preload.auto", 2)        # preload metadata if preload=auto
    fp.set_preference("media.cache_size", 32768)        # 32MB media cache
    # Try to save battery by not resuming reading from a connection until we fall
    # below 10s of buffered data.
    fp.set_preference("media.cache_resume_threshold", 10)
    fp.set_preference("media.cache_readahead_limit", 30)

    # Number of video frames we buffer while decoding video.
    # On Android this is decided by a similar value which varies for
    # each OMX decoder |OMX_PARAM_PORTDEFINITIONTYPE::nBufferCountMin|. This
    # number must be less than the OMX equivalent or gecko will think it is
    # chronically starved of video frames. All decoders seen so far have a value
    # of at least 4.
    fp.set_preference("media.video-queue.default-size", 3)

    # Enable the MediaCodec PlatformDecoderModule by default.
    fp.set_preference("media.android-media-codec.enabled", True)
    fp.set_preference("media.android-media-codec.preferred", True)

    # Enable MSE
    fp.set_preference("media.mediasource.enabled", True)

    # optimize images memory usage
    fp.set_preference("image.downscale-during-decode.enabled", True)

    """
    Disabling based on selenium webdriver prefs.
    fp.set_preference("browser.safebrowsing.enabled", True)
    fp.set_preference("browser.safebrowsing.malware.enabled", True)
    fp.set_preference("browser.safebrowsing.downloads.enabled", False)
    fp.set_preference("browser.safebrowsing.downloads.remote.enabled", False)
    fp.set_preference("browser.safebrowsing.downloads.remote.timeout_ms", 10000)
    fp.set_preference("browser.safebrowsing.debug", False)

    fp.set_preference("browser.safebrowsing.provider.google.lists", "goog-badbinurl-shavar,goog-downloadwhite-digest256,goog-phish-shavar,goog-malware-shavar,goog-unwanted-shavar")
    fp.set_preference("browser.safebrowsing.provider.google.updateURL", "https://safebrowsing.google.com/safebrowsing/downloads?client=SAFEBROWSING_ID&appver=%VERSION%&pver=2.2&key=%GOOGLE_API_KEY%")
    fp.set_preference("browser.safebrowsing.provider.google.gethashURL", "https://safebrowsing.google.com/safebrowsing/gethash?client=SAFEBROWSING_ID&appver=%VERSION%&pver=2.2")
    fp.set_preference("browser.safebrowsing.provider.google.reportURL", "https://safebrowsing.google.com/safebrowsing/diagnostic?client=%NAME%&hl=%LOCALE%&site=")
    fp.set_preference("browser.safebrowsing.provider.google.appRepURL", "https://sb-ssl.google.com/safebrowsing/clientreport/download?key=%GOOGLE_API_KEY%")

    fp.set_preference("browser.safebrowsing.reportPhishMistakeURL", "https://%LOCALE%.phish-error.mozilla.com/?hl=%LOCALE%&url=")
    fp.set_preference("browser.safebrowsing.reportPhishURL", "https://%LOCALE%.phish-report.mozilla.com/?hl=%LOCALE%&url=")
    fp.set_preference("browser.safebrowsing.reportMalwareMistakeURL", "https://%LOCALE%.malware-error.mozilla.com/?hl=%LOCALE%&url=")
    fp.set_preference("browser.safebrowsing.appRepURL", "https://sb-ssl.google.com/safebrowsing/clientreport/download?key=%GOOGLE_API_KEY%")

    fp.set_preference("browser.safebrowsing.id", @MOZ_APP_UA_NAME@)
    """

    # Name of the about: page contributed by safebrowsing to handle display of error
    # pages on phishing/malware hits.  (bug 399233)
    fp.set_preference("urlclassifier.alternate_error_page", "blocked")

    # The number of random entries to send with a gethash request.
    fp.set_preference("urlclassifier.gethashnoise", 4)

    # Gethash timeout for Safebrowsing.
    fp.set_preference("urlclassifier.gethash.timeout_ms", 5000)

    # If an urlclassifier table has not been updated in this number of seconds,
    # a gethash request will be forced to check that the result is still in
    # the database.
    fp.set_preference("urlclassifier.max-complete-age", 2700)

    # True if this is the first time we are showing about:firstrun
    fp.set_preference("browser.firstrun.show.uidiscovery", True)
    fp.set_preference("browser.firstrun.show.localepicker", False)

    # True if you always want dump() to work
    # On Android, you also need to do the following for the output
    # to show up in logcat:
    # $ adb shell stop
    # $ adb shell setprop log.redirect-stdio True
    # $ adb shell start
    # webdriver pref
    # fp.set_preference("browser.dom.window.dump.enabled", True)

    # SimplePush
    fp.set_preference("services.push.enabled", False)

    # controls if we want camera support
    fp.set_preference("device.camera.enabled", True)
    fp.set_preference("media.realtime_decoder.enabled", True)

    # webdriver pref
    # fp.set_preference("dom.report_all_js_exceptions", True)
    # fp.set_preference("javascript.options.showInConsole", True)

    fp.set_preference("full-screen-api.enabled", True)

    fp.set_preference("direct-texture.force.enabled", False)
    fp.set_preference("direct-texture.force.disabled", False)

    # This fraction in 1000ths of velocity remains after every animation frame when the velocity is low.
    fp.set_preference("ui.scrolling.friction_slow", -1)
    # This fraction in 1000ths of velocity remains after every animation frame when the velocity is high.
    fp.set_preference("ui.scrolling.friction_fast", -1)
    # The maximum velocity change factor between events, per ms, in 1000ths.
    # Direction changes are excluded.
    fp.set_preference("ui.scrolling.max_event_acceleration", -1)
    # The rate of deceleration when the surface has overscrolled, in 1000ths.
    fp.set_preference("ui.scrolling.overscroll_decel_rate", -1)
    # The fraction of the surface which can be overscrolled before it must snap back, in 1000ths.
    fp.set_preference("ui.scrolling.overscroll_snap_limit", -1)
    # The minimum amount of space that must be present for an axis to be considered scrollable,
    # in 1/1000ths of pixels.
    fp.set_preference("ui.scrolling.min_scrollable_distance", -1)
    # The axis lock mode for panning behaviour - set between standard, free and sticky
    fp.set_preference("ui.scrolling.axis_lock_mode", "standard")
    # Negate scroll, True will make the mouse scroll wheel move the screen the same direction as with most desktops or laptops.
    fp.set_preference("ui.scrolling.negate_wheel_scroll", True)
    # Determine the dead zone for gamepad joysticks. Higher values result in larger dead zones; use a negative value to
    # auto-detect based on reported hardware values
    fp.set_preference("ui.scrolling.gamepad_dead_zone", 115)

    # Prefs for fling acceleration
    fp.set_preference("ui.scrolling.fling_accel_interval", -1)
    fp.set_preference("ui.scrolling.fling_accel_base_multiplier", -1)
    fp.set_preference("ui.scrolling.fling_accel_supplemental_multiplier", -1)

    # Prefs for fling curving
    fp.set_preference("ui.scrolling.fling_curve_function_x1", -1)
    fp.set_preference("ui.scrolling.fling_curve_function_y1", -1)
    fp.set_preference("ui.scrolling.fling_curve_function_x2", -1)
    fp.set_preference("ui.scrolling.fling_curve_function_y2", -1)
    fp.set_preference("ui.scrolling.fling_curve_threshold_velocity", -1)
    fp.set_preference("ui.scrolling.fling_curve_max_velocity", -1)
    fp.set_preference("ui.scrolling.fling_curve_newton_iterations", -1)

    # Enable accessibility mode if platform accessibility is enabled.
    fp.set_preference("accessibility.accessfu.activate", 2)
    fp.set_preference("accessibility.accessfu.quicknav_modes", "Link,Heading,FormElement,Landmark,ListItem")
    # Active quicknav mode, index value of list from quicknav_modes
    fp.set_preference("accessibility.accessfu.quicknav_index", 0)
    # Setting for an utterance order (0 - description first, 1 - description last).
    fp.set_preference("accessibility.accessfu.utterance", 1)
    # Whether to skip images with empty alt text
    fp.set_preference("accessibility.accessfu.skip_empty_images", True)

    # Transmit UDP busy-work to the LAN when anticipating low latency
    # network reads and on wifi to mitigate 802.11 Power Save Polling delays
    fp.set_preference("network.tickle-wifi.enabled", True)

    # Mobile manages state by autodetection
    # webdriver pref
    # fp.set_preference("network.manage-offline-status", True)

    # increase the timeout clamp for background tabs to 15 minutes
    fp.set_preference("dom.min_background_timeout_value", 900000)

    # Media plugins for libstagefright playback on android
    fp.set_preference("media.plugins.enabled", True)

    # Stagefright's OMXCodec::CreationFlags. The interesting flag values are:
    #  0 = Let Stagefright choose hardware or software decoding (default)
    #  8 = Force software decoding
    # 16 = Force hardware decoding
    fp.set_preference("media.stagefright.omxcodec.flags", 0)

    # Coalesce touch events to prevent them from flooding the event queue
    fp.set_preference("dom.event.touch.coalescing.enabled", False)

    # default orientation for the app, default to undefined
    # the java GeckoScreenOrientationListener needs this to be defined
    fp.set_preference("app.orientation.default", "")

    # On memory pressure, release dirty but unused pages held by jemalloc
    # back to the system.
    fp.set_preference("memory.free_dirty_pages", True)

    fp.set_preference("layout.imagevisibility.numscrollportwidths", 1)
    fp.set_preference("layout.imagevisibility.numscrollportheights", 1)

    fp.set_preference("layers.enable-tiles", True)

    # Speculative 'fix' to work around OOM issues
    fp.set_preference("layers.tiles.adjust", False)

    # Enable the dynamic toolbar
    fp.set_preference("browser.chrome.dynamictoolbar", True)

    # Hide common parts of URLs like "www." or "http://"
    fp.set_preference("browser.urlbar.trimURLs", True)

    # initial web feed readers list
    fp.set_preference("browser.contentHandlers.types.0.title", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.contentHandlers.types.0.uri", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.contentHandlers.types.0.type", "application/vnd.mozilla.maybe.feed")
    fp.set_preference("browser.contentHandlers.types.1.title", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.contentHandlers.types.1.uri", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.contentHandlers.types.1.type", "application/vnd.mozilla.maybe.feed")
    fp.set_preference("browser.contentHandlers.types.2.title", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.contentHandlers.types.2.uri", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.contentHandlers.types.2.type", "application/vnd.mozilla.maybe.feed")
    fp.set_preference("browser.contentHandlers.types.3.title", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.contentHandlers.types.3.uri", "chrome://browser/locale/region.properties")
    fp.set_preference("browser.contentHandlers.types.3.type", "application/vnd.mozilla.maybe.feed")

    # WebPayment
    fp.set_preference("dom.mozPay.enabled", True)

    fp.set_preference("dom.payment.provider.0.name", "Firefox Marketplace")
    fp.set_preference("dom.payment.provider.0.description", "marketplace.firefox.com")
    fp.set_preference("dom.payment.provider.0.uri", "https://marketplace.firefox.com/mozpay/?req=")
    fp.set_preference("dom.payment.provider.0.type", "mozilla/payments/pay/v1")
    fp.set_preference("dom.payment.provider.0.requestMethod", "GET")

    # Shortnumber matching needed for e.g. Brazil:
    # 01187654321 can be found with 87654321
    fp.set_preference("dom.phonenumber.substringmatching.BR", 8)
    fp.set_preference("dom.phonenumber.substringmatching.CO", 10)
    fp.set_preference("dom.phonenumber.substringmatching.VE", 7)

    # Enable hardware-accelerated Skia canvas
    fp.set_preference("gfx.canvas.azure.backends", "skia")
    fp.set_preference("gfx.canvas.azure.accelerated", True)

    # See ua-update.json.in for the packaged UA override list
    fp.set_preference("general.useragent.updates.enabled", True)
    fp.set_preference("general.useragent.updates.url", "https://dynamicua.cdn.mozilla.net/0/%APP_ID%")
    fp.set_preference("general.useragent.updates.interval", 604800)     # 1 week
    fp.set_preference("general.useragent.updates.retry", 86400)     # 1 day

    # When True, phone number linkification is enabled.
    fp.set_preference("browser.ui.linkify.phone", False)

    # Enables/disables Spatial Navigation
    fp.set_preference("snav.enabled", True)

    # This url, if changed, MUST continue to point to an https url. Pulling arbitrary content to inject into
    # this page over http opens us up to a man-in-the-middle attack that we'd rather not face. If you are a downstream
    # repackager of this code using an alternate snippet url, please keep your users safe
    fp.set_preference("browser.snippets.updateUrl", "https://snippets.cdn.mozilla.net/json/%SNIPPETS_VERSION%/%NAME%/%VERSION%/%APPBUILDID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/")

    # How frequently we check for new snippets, in seconds (1 day)
    fp.set_preference("browser.snippets.updateInterval", 86400)

    # URL used to check for user's country code
    fp.set_preference("browser.snippets.geoUrl", "https://geo.mozilla.org/country.json")

    # URL used to ping metrics with stats about which snippets have been shown
    fp.set_preference("browser.snippets.statsUrl", "https://snippets-stats.mozilla.org/mobile")

    # These prefs require a restart to take effect.
    fp.set_preference("browser.snippets.enabled", True)
    fp.set_preference("browser.snippets.syncPromo.enabled", True)
    fp.set_preference("browser.snippets.firstrunHomepage.enabled", True)

    # The URL of the APK factory from which we obtain APKs for webapps.
    fp.set_preference("browser.webapps.apkFactoryUrl", "https://controller.apk.firefox.com/application.apk")

    # How frequently to check for webapp updates, in seconds (86400 is daily).
    fp.set_preference("browser.webapps.updateInterval", 86400)

    # Whether or not to check for updates.  Enabled by default, but the runtime
    # disables it for webapp profiles on firstrun, so only the main Fennec process
    # checks for updates (to avoid duplicate update notifications).
    # In the future, we might want to make each webapp process check for updates
    # for its own webapp, in which case we'll need to have a third state for this
    # preference.  Thus it's an integer rather than a boolean.
    # Possible values:
    #   0: don't check for updates
    #   1: do check for updates
    fp.set_preference("browser.webapps.checkForUpdates", 1)

    # The URL of the service that checks for updates.
    # To test updates, set this to http://apk-update-checker.paas.allizom.org,
    # which is a test server that always reports all apps as having updates.
    fp.set_preference("browser.webapps.updateCheckUrl", "https://controller.apk.firefox.com/app_updates")

    # The mode of home provider syncing.
    # 0: Sync always
    # 1: Sync only when on wifi
    fp.set_preference("home.sync.updateMode", 0)

    # How frequently to check if we should sync home provider data.
    fp.set_preference("home.sync.checkIntervalSecs", 3600)

    # Enable device storage API
    fp.set_preference("device.storage.enabled", True)

    # Enable meta-viewport support for font inflation code
    fp.set_preference("dom.meta-viewport.enabled", True)

    # Enable GMP support in the addon manager.
    fp.set_preference("media.gmp-provider.enabled", True)

    # The default color scheme in reader mode (light, dark, auto)
    # auto = color automatically adjusts according to ambient light level
    # (auto only works on platforms where the 'devicelight' event is enabled)
    fp.set_preference("reader.color_scheme", "auto")

    # Color scheme values available in reader mode UI.
    fp.set_preference("reader.color_scheme.values", "[\"dark\",\"auto\",\"light\"]")

    # Whether to use a vertical or horizontal toolbar.
    fp.set_preference("reader.toolbar.vertical", False)

    # Whether or not to display buttons related to reading list in reader view.
    fp.set_preference("browser.readinglist.enabled", True)

    # Telemetry settings.
    # Whether to use the unified telemetry behavior, requires a restart.
    fp.set_preference("toolkit.telemetry.unified", False)

    # Unified AccessibleCarets (touch-caret and selection-carets).
    fp.set_preference("layout.accessiblecaret.enabled", False)
    # Android generates long tap (mouse) events.
    fp.set_preference("layout.accessiblecaret.use_long_tap_injector", False)

    # Android tries to maintain extended visibility of the AccessibleCarets
    # during Selection change notifications generated by Javascript,
    # or misc internal events.
    fp.set_preference("layout.accessiblecaret.extendedvisibility", True)

    # Optionally provide haptic feedback on longPress selection events.
    fp.set_preference("layout.accessiblecaret.hapticfeedback", True)

    # Disable sending console to logcat on release builds.
    fp.set_preference("consoleservice.logcat", False)

    # Enable Cardboard VR on mobile, assuming VR at all is enabled
    fp.set_preference("dom.vr.cardboard.enabled", True)

    # Enable VR on mobile, making it enable by default.
    fp.set_preference("dom.vr.enabled", True)

    fp.set_preference("browser.tabs.showAudioPlayingIcon", True)

    # The remote content URL where FxAccountsWebChannel messages originate.  Must use HTTPS.
    fp.set_preference("identity.fxaccounts.remote.webchannel.uri", "https://accounts.firefox.com")

    # The remote URL of the Firefox Account profile server.
    fp.set_preference("identity.fxaccounts.remote.profile.uri", "https://profile.accounts.firefox.com/v1")

    # The remote URL of the Firefox Account oauth server.
    fp.set_preference("identity.fxaccounts.remote.oauth.uri", "https://oauth.accounts.firefox.com/v1")

    # Token server used by Firefox Account-authenticated Sync.
    fp.set_preference("identity.sync.tokenserver.uri", "https://token.services.mozilla.com/1.0/sync/1.5")
