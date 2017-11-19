function getPageScript() {
  // return a string

  return "(" + function() {
    // Triggering sensor events every second after page load
    setInterval(trigger_sensor_events, 20);

    function trigger_sensor_events(){
      trigger_devicelight_event();
      // setTimeout(trigger_lightlevel_event, 100);
      setTimeout(trigger_deviceproximity_event, 200);
      setTimeout(trigger_userproximity_event, 400);
      setTimeout(trigger_deviceorientation_event, 600);
      setTimeout(trigger_devicemotion_event, 800);
    }

    function trigger_devicelight_event(){
      var devicelight_event = new DeviceLightEvent('devicelight', {
        'value': 987, 
        'bubbles': true,
        'cancelable': true
      });
      window.dispatchEvent(devicelight_event)
    }

    function trigger_lightlevel_event(){
      // This is not supported and causes JS error on Firefox
      // Let's not use it
      var lightlevel_event = new LightLevelEvent('lightlevel', {
        'value': "bright",
        'bubbles': true,
        'cancelable': true
      });
      // window.dispatchEvent(lightlevel_event)
    }

    function trigger_deviceproximity_event(){
      // Firefox and Chrome on Android don't seem to support this event
      var deviceproximity_event = new DeviceProximityEvent('deviceproximity', {
        'min': 0,
        'max': 100,
        'value': 3,
        'bubbles': true,
        'cancelable': true
      });
      window.dispatchEvent(deviceproximity_event)
    }

    function trigger_userproximity_event(){
      var userproximity_event = new UserProximityEvent('userproximity', {
        'near': true,
        'bubbles': true,
        'cancelable': true
      });
      window.dispatchEvent(userproximity_event)
    }

    function trigger_deviceorientation_event(){
      var deviceorientation_event = new DeviceOrientationEvent('deviceorientation', {
        'alpha': 43.1234 + random_fraction(),
        'beta': 32.9876 + random_fraction(),
        'gamma': 21.6543 + random_fraction(),
        'bubbles': true,
        'cancelable': true
      });
      window.dispatchEvent(deviceorientation_event)
    }

    function trigger_devicemotion_event(){
      var devicemotion_event = new DeviceMotionEvent('devicemotion', {
        'acceleration':{
          'x':0.1256 + random_fraction(),
          'y':-0.1234 + random_fraction(),
          'z':-0.1845 + random_fraction()
        },
        'accelerationIncludingGravity':{
          'x':0.0256 + random_fraction(),
          'y':0.1234 + random_fraction(),
          'z':9.7568 + random_fraction()
        },
        'rotationRate':{
          'alpha':0.0005 + random_fraction(),
          'beta':0.0034 + random_fraction(),
          'gamma':-0.0048 + random_fraction()
        },
        'interval': 16.6660 + random_fraction(),
        'bubbles': true,
        'cancelable': true
      });
      window.dispatchEvent(devicemotion_event)
    }

    function random_fraction(leading_zeroes){
      var leading_zeroes = leading_zeroes || 5;
      return Math.random() / Math.pow(10, leading_zeroes);
    }

    console.log("Fake sensor events will be dispatched!");

  } + "());";
}


function insertScript(text) {
  var parent = document.documentElement,
    script = document.createElement('script');
  script.text = text;
  script.async = false;

  parent.insertBefore(script, parent.firstChild);
  parent.removeChild(script);
}
insertScript(getPageScript());
