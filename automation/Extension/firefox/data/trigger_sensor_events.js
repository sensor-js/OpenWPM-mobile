function getPageScript() {
  // return a string

  return "(" + function() {
    // Triggering sensor events every second after page load
    setInterval(trigger_sensor_events, 1000);

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
        'max': 5,  // ga: max is 100 for my Moto G5 plus
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
        'alpha': 43.1234,
        'beta': 32.9876,
        'gamma': 21.6543,
        'bubbles': true,
        'cancelable': true
      });
      window.dispatchEvent(deviceorientation_event)
    }

    function trigger_devicemotion_event(){
      var devicemotion_event = new DeviceMotionEvent('devicemotion', {
        'acceleration':{
          'x':0.1256,
          'y':-0.1234,
          'z':-0.1845
        },
        'accelerationIncludingGravity':{
          'x':0.0256,
          'y':0.1234,
          'z':9.7568
        },
        'rotationRate':{
          'alpha':0.0005,
          'beta':0.0034,
          'gamma':-0.0048
        },
        'interval': 16.6660,
        'bubbles': true,
        'cancelable': true
      });
      window.dispatchEvent(devicemotion_event)
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
